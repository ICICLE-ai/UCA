import unittest
import uuid
from typing import Any, Dict, List
from unittest.mock import patch

from src.database.cyber_infra.cyber_infra_client import CyberInfraClient
from src.database.cyber_infra.cyber_infra_entity import QueueToNodeConfig, NodeConfig

import src.database.cyber_infra.config as cfg
cfg.MONGO_URI = ""
cfg.DB_NAME   = ""

class DummyCollection:
    def __init__(self):
        self._data = []
    def insert_many(self, docs: List[dict]):
        inserted_ids = []
        for d in docs:
            doc = d.copy()
            doc["_id"] = uuid.uuid4()
            self._data.append(doc)
            inserted_ids.append(doc["_id"])
        return type("R", (), {"inserted_ids": inserted_ids})()
    def find(self, query=None):
        query = query or {}
        for doc in list(self._data):
            if all(doc.get(k) == v for k,v in query.items()):
                yield doc.copy()
    def insert_one(self, doc: dict):
        d = doc.copy()
        d["_id"] = uuid.uuid4()
        self._data.append(d)
        return type("R", (), {"inserted_id": d["_id"]})()

class DummyDB:
    def __init__(self):
        self.QUEUE_TO_NODE_CONFIG = DummyCollection()
        self.NODE_CONFIG            = DummyCollection()
        self.SC_TO_CLUSTERS         = DummyCollection()
        self.BILLING_AND_COST       = DummyCollection()
        self.TACC_BILLING_INFO      = DummyCollection()
    def __getitem__(self, name):
        return getattr(self, name)

class DummyMongoClient:
    def __init__(self, uri=None):
        self._db = DummyDB()
    def __getitem__(self, db_name):
        return self._db

class TestCyberInfraClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mongo_patcher = patch(
            "src.database.cyber_infra.cyber_infra_client.MongoClient",
            DummyMongoClient
        )
        cls.mongo_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.mongo_patcher.stop()

    def test_insert_and_list_queue_configs(self):
        client = CyberInfraClient(uri="u", db_name="db")
        with self.assertRaises(TypeError):
            client.insert_queue_configs("not a list")

        with self.assertRaises(TypeError):
            client.insert_queue_configs([1, 2, 3])

        q1 = QueueToNodeConfig.new("A", max_node=1)
        q2 = QueueToNodeConfig.new("B", max_node=2, sc_to_cluster="C")
        count = client.insert_queue_configs([q1, q2])
        self.assertEqual(count, 2)

        listed = client.list_queue_configs()
        self.assertEqual(len(listed), 2)
        self.assertTrue(all(isinstance(x, QueueToNodeConfig) for x in listed))
        self.assertCountEqual([x.queue_name for x in listed], ["A","B"])

    def test_insert_and_list_node_configs(self):
        client = CyberInfraClient(uri="u", db_name="db")
        with self.assertRaises(TypeError):
            client.insert_node_configs("nope")   # not a list

        with self.assertRaises(TypeError):
            client.insert_node_configs([{"foo":"bar"}, 123])

        n1 = NodeConfig.new(
            system_name="n1", SC_name="S", cluster_name="C",
            node_type="t", total_compute_nodes=1,
            processor_type="p", processor_cores=4,
            processor_clock_speed=2.5, memory_size_GB=8,
            processor_model="m", processor_architecture="a",
            sockets_count=1
        )
        count = client.insert_node_configs([n1])
        self.assertEqual(count, 1)

        listed = client.list_node_configs()
        self.assertEqual(len(listed), 1)
        self.assertIsInstance(listed[0], dict)
        self.assertEqual(listed[0]["system_name"], "n1")

    def test_insert_and_list_sc_clusters(self):
        client = CyberInfraClient(uri="u", db_name="db")
        with self.assertRaises(TypeError):
            client.insert_sc_clusters("nope")

        rec = {"cluster_name":"X","SC_name":"Y","is_active":True}
        uid = client.insert_sc_clusters(rec)
        self.assertIsInstance(uid, str)

        listed = client.list_sc_clusters()
        self.assertEqual(listed[0]["UUID"], uid)
        self.assertEqual(listed[0]["cluster_name"], "X")

    def test_insert_and_list_billing_and_cost(self):
        client = CyberInfraClient(uri="u", db_name="db")
        with self.assertRaises(TypeError):
            client.insert_billing_and_cost(123)

        rec = {
            "supercomputer_center_name":"Z",
            "service_type":"GPU",
            "cost":0.5
        }
        uid = client.insert_billing_and_cost(rec)
        self.assertIsInstance(uid, str)

        listed = client.list_billing_and_cost()
        self.assertEqual(listed[0]["supercomputer_center_name"], "Z")
        self.assertEqual(listed[0]["cost"], 0.5)

    def test_insert_and_list_tacc_billing(self):
        client = CyberInfraClient(uri="u", db_name="db")
        with self.assertRaises(TypeError):
            client.insert_tacc_billing("nope")

        entries = [
            {"supercomputer_center_name":"A","service_type":"t","cost":1.0},
            ["not a dict"],
            {"service_type":"t"}
        ]
        count = client.insert_tacc_billing(entries)
        self.assertEqual(count, 2)

        listed = client.list_tacc_billing()
        self.assertEqual(len(listed), 2)

    def test_queue_model_roundtrip(self):
        orig = QueueToNodeConfig.new("Q", max_node=5, sc_to_cluster="C")
        as_dict = orig.to_dict()
        copy = QueueToNodeConfig.from_dict(as_dict)
        self.assertEqual(copy, orig)

    def test_node_model_roundtrip(self):
        orig = NodeConfig.new(
            system_name="n1", SC_name="S", cluster_name="C",
            node_type="t", total_compute_nodes=1,
            processor_type="p", processor_cores=4,
            processor_clock_speed=2.5, memory_size_GB=8,
            processor_model="m", processor_architecture="a",
            sockets_count=1
        )
        as_dict = orig.to_dict()
        copy = NodeConfig.from_dict(as_dict)
        self.assertEqual(copy, orig)