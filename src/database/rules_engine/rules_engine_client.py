# TODO: Need to write ReadMe file with end to end explaination
from pymongo import MongoClient
from tapipy.tapis import Tapis
import uuid
import datetime

from src.model_commons.patra.validator import Validator
from src.database.rules_engine.rules_engine_entity import Rule
from src.database.rules_engine.exceptions import RuleEngineError, RuleValidationError, RuleNotFoundError
from src.database.rules_engine.config import Config

class RuleEngineClient:
    def __init__(
        self,
        tapis_url: str = None,
        tapis_user: str = None,
        tapis_pass: str = None,
        mongo_uri: str = None,
        db_name: str = "IMT_Rules_engine_database"
    ):
        # Initializing and authenticatingd Tapis client
        self.tapis = Tapis(
            base_url=tapis_url or Config.TAPIS_URL,
            username=tapis_user or Config.TAPIS_USER,
            password=tapis_pass or Config.TAPIS_PASS
        )
        try:
            self.tapis.get_tokens()
        except Exception as e:
            raise RuleEngineError(f"Failed to authenticate to TAPIS: {e}")
        
        # MongoDB connection
        uri = mongo_uri or Config.MONGO_URI
        if not uri:
            raise RuleEngineError("`mongo_uri` must be provided")
        self.db = MongoClient(uri)[db_name]

    def create_rule(self, rule_data: dict) -> str:
        try:
            Validator.Validate(rule_data, "dict", error_type=RuleValidationError)
            Validator.ValidateDict(
                rule_data,
                keys_mandatory=["CI", "Type", "Services", "Data_Rules"],
                keys_mandatory_types=["str", "str", "list", "list"]
            )
        except ValueError as ve:
            raise RuleValidationError(str(ve))

        # TODO: Future work to validate the list types
        # Validator.Validate(rule_data["Services"],    "list[str]", error_type=RuleValidationError)
        # Validator.Validate(rule_data["Data_Rules"], "list[dict]", error_type=RuleValidationError)

        if rule_data["Type"] not in ("data", "model"):
            raise RuleValidationError("`Type` must be 'data' or 'model'")

        token  = self.tapis.access_token.access_token
        claims = self.tapis.access_token.claims

        data = rule_data.copy()
        data.update({
            "TapisToken":    token,
            "TAPIS_UUID":    claims.get("sub"),
            "Tapis_UserName":claims.get("tapis/username")
        })

        data["Rule_UUID"]   = str(uuid.uuid4())
        data["Active_From"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        data.setdefault("Active_To", None)

        # persist and return
        self.db.user_rules.insert_one(data)
        return data["Rule_UUID"]

    def list_rules(self, filter_query: dict = None) -> list[Rule]:
        cursor = self.db.user_rules.find(filter_query or {})
        results = []
        for doc in cursor:
            doc.pop("_id", None)
            doc.pop("Model_Rules", None)
            results.append(Rule(**doc))
        return results

    def update_rule(self, rule_uuid: str, updates: dict) -> None:
        res = self.db.user_rules.update_one(
            {"Rule_UUID": rule_uuid},
            {"$set": updates}
        )
        if res.matched_count == 0:
            raise RuleNotFoundError(f"Rule {rule_uuid} not found")

    def delete_rule(self, rule_uuid: str) -> None:
        res = self.db.user_rules.delete_one({"Rule_UUID": rule_uuid})
        if res.deleted_count == 0:
            raise RuleNotFoundError(f"Rule {rule_uuid} not found")
