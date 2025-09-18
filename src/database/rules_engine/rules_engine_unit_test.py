# TODO: Look into finding more stable test cases if any

import datetime
import unittest
import uuid
from contextlib import contextmanager
from unittest.mock import patch

from src.database.rules_engine.exceptions import RuleEngineError, RuleNotFoundError, RuleValidationError
from src.database.rules_engine.rules_engine_client import RuleEngineClient
from src.database.rules_engine.rules_engine_entity import Rule


class DummyToken:
    def __init__(self):
        self.access_token = "fake-token"
        self.claims = {"sub": "fake-uuid", "tapis/username": "alice"}

class DummyTapis:
    def __init__(self, base_url=None, username=None, password=None):
        pass

    def get_tokens(self):
        # Stubbing authentication call
        return None

    @property
    def access_token(self):
        return DummyToken()

class DummyCollection:
    def __init__(self):
        self.storage = {}

    def insert_one(self, doc):
        self.storage[doc["Rule_UUID"]] = doc.copy()

    def find(self, query=None):
        query = query or {}
        for doc in list(self.storage.values()):
            if all(doc.get(k) == v for k, v in query.items()):
                yield {**doc, "_id": None}

    def update_one(self, query, update):
        key = query.get("Rule_UUID")
        if key in self.storage:
            self.storage[key].update(update.get("$set", {}))
            return type("R", (), {"matched_count": 1})()
        return type("R", (), {"matched_count": 0})()

    def delete_one(self, query):
        key = query.get("Rule_UUID")
        if key in self.storage:
            del self.storage[key]
            return type("R", (), {"deleted_count": 1})()
        return type("R", (), {"deleted_count": 0})()

class DummyDB:
    def __init__(self):
        self.user_rules = DummyCollection()

class DummyMongoClient:
    def __init__(self, uri=None):
        self._db = DummyDB()

    def __getitem__(self, name):
        return self._db


# ---- helper to patch Config used inside rules_engine_client ----
@contextmanager
def patched_rules_config(**overrides):
    """
    Patch the Config class referenced by rules_engine_client so tests don't
    depend on real config.yaml values. By default, everything is "unset".
    """
    target = 'src.database.rules_engine.rules_engine_client.Config'
    with patch(target) as C:
        C.TAPIS_URL  = overrides.get('TAPIS_URL', '')
        C.TAPIS_USER = overrides.get('TAPIS_USER', '')
        C.TAPIS_PASS = overrides.get('TAPIS_PASS', '')
        C.MONGO_URI  = overrides.get('MONGO_URI', None)
        yield


class TestRuleEngineClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Patch Tapis and MongoClient used by the client module
        cls.patcher_tapis = patch('src.database.rules_engine.rules_engine_client.Tapis', DummyTapis)
        cls.patcher_mongo = patch('src.database.rules_engine.rules_engine_client.MongoClient', DummyMongoClient)
        cls.patcher_tapis.start()
        cls.patcher_mongo.start()

    @classmethod
    def tearDownClass(cls):
        cls.patcher_tapis.stop()
        cls.patcher_mongo.stop()

    def make_client(self, **kwargs):
        defaults = {
            'tapis_url': 'u',
            'tapis_user': 'u',
            'tapis_pass': 'p',
            'mongo_uri': 'dummy://',
            'db_name': 'IMT_Rule_Engine'
        }
        defaults.update(kwargs)
        return RuleEngineClient(**defaults)

    def test_init_variants(self):
        # 1) Nothing provided; no fallbacks -> should raise (missing creds + mongo)
        with patched_rules_config(MONGO_URI=None, TAPIS_URL='', TAPIS_USER='', TAPIS_PASS=''):
            with self.assertRaises(RuleEngineError):
                RuleEngineClient()

        # 2) Tapis creds provided but no mongo anywhere -> should raise
        with patched_rules_config(MONGO_URI=None):
            with self.assertRaises(RuleEngineError):
                RuleEngineClient(tapis_url='u', tapis_user='u', tapis_pass='p')

        # 3) Only mongo provided; Tapis is stubbed by DummyTapis -> should succeed
        with patched_rules_config(MONGO_URI=None):
            client = RuleEngineClient(mongo_uri='dummy://')
            self.assertIsInstance(client, RuleEngineClient)

        # 4) All provided -> should succeed
        with patched_rules_config(MONGO_URI=None):
            client = RuleEngineClient(
                tapis_url='u', tapis_user='u', tapis_pass='p', mongo_uri='dummy://'
            )
            self.assertIsInstance(client, RuleEngineClient)

    def test_create_rule_missing_fields(self):
        with patched_rules_config(MONGO_URI='dummy://'):
            client = self.make_client()
            with self.assertRaises(RuleValidationError):
                client.create_rule({'CI': 'only_one_field'})

    def test_create_and_list_rule(self):
        with patched_rules_config(MONGO_URI='dummy://'):
            client = self.make_client()
            data = {
                "CI": "OSC",
                "Type": "data",
                "Active_From": "2024-05-06T12:00:00",
                "Active_To": None,
                "Services": ["data-label", "model-train"],
                "Data_Rules": [{
                    "Folder_Path": "/fs/ess/PAS2271/Gautam/Animal_Ecology/output/old/visualized_images",
                    "Type": "count",
                    "Count": 10000,
                    "Apps": ["<TAPIS_APP_ID_1>", "<TAPIS_APP_ID_2>"],
                    "Sample_Images": True,
                    "Wait_Manual": True
                }],
                "Model_Rules": []
            }
            rule_uuid = client.create_rule(data)
            self.assertIsInstance(rule_uuid, str)

            rules = client.list_rules({'Rule_UUID': rule_uuid})
            self.assertEqual(len(rules), 1)
            r = rules[0]
            self.assertIsInstance(r, Rule)
            self.assertEqual(r.Rule_UUID, rule_uuid)
            datetime.datetime.fromisoformat(r.Active_From)

    def test_update_and_delete(self):
        with patched_rules_config(MONGO_URI='dummy://'):
            client = self.make_client()
            data = {'CI': 'c', 'Type': 'model', 'Services': [], 'Data_Rules': []}
            rule_uuid = client.create_rule(data)
            client.update_rule(rule_uuid, {'Active_To': '2099-01-01T00:00:00'})
            updated = client.list_rules({'Rule_UUID': rule_uuid})[0]
            self.assertEqual(updated.Active_To, '2099-01-01T00:00:00')
            client.delete_rule(rule_uuid)
            self.assertEqual(client.list_rules({'Rule_UUID': rule_uuid}), [])

    def test_update_not_found(self):
        with patched_rules_config(MONGO_URI='dummy://'):
            client = self.make_client()
            with self.assertRaises(RuleNotFoundError):
                client.update_rule(str(uuid.uuid4()), {})

    def test_delete_not_found(self):
        with patched_rules_config(MONGO_URI='dummy://'):
            client = self.make_client()
            with self.assertRaises(RuleNotFoundError):
                client.delete_rule(str(uuid.uuid4()))

    def test_list_empty(self):
        with patched_rules_config(MONGO_URI='dummy://'):
            client = self.make_client()
            self.assertEqual(client.list_rules(), [])


if __name__ == '__main__':
    unittest.main()