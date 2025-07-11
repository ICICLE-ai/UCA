import uuid
from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection

from src.database.cyber_infra.config import DB_NAME, MONGO_URI
from src.database.cyber_infra.cyber_infra_entity import NodeConfig, QueueToNodeConfig
from src.model_commons.patra.validator import Validator


class CyberInfraClient:
    def __init__(
        self,
        uri: Optional[str] = None,
        db_name: Optional[str] = None
    ):
        self._uri = uri or MONGO_URI
        Validator.validate(self._uri, "str")
        if not self._uri:
            raise ValueError("MONGO_URI is required and must be a non-empty string")

        self._db_name = db_name or DB_NAME
        Validator.validate(self._db_name, "str")
        if not self._db_name:
            raise ValueError("DB_NAME is required and must be a non-empty string")

        self._client = MongoClient(self._uri)
        self.db = self._client[self._db_name]

    def _col(self, name: str) -> Collection:
        Validator.validate(name, "str")
        return self.db[name]

    # -- QUEUE_TO_NODE_CONFIG --------------------------------------------------

    def insert_queue_configs(
        self,
        configs: List[QueueToNodeConfig]
    ) -> int:
        Validator.validate(configs, "list")
        for cfg in configs:
            if not isinstance(cfg, QueueToNodeConfig):
                raise TypeError(f"All items must be QueueToNodeConfig, got {type(cfg)}")

        docs = [cfg.to_dict() for cfg in configs]
        result = self._col("QUEUE_TO_NODE_CONFIG").insert_many(docs)
        return len(result.inserted_ids)

    def list_queue_configs(self, filter_query: dict = None) -> List[QueueToNodeConfig]:
        cursor = self._col("QUEUE_TO_NODE_CONFIG").find(filter_query or {})
        results = []
        for doc in cursor:
            # dropping Mongo's internal _id
            doc.pop("_id", None)
            results.append(QueueToNodeConfig.from_dict(doc))
        return results

    # -- NODE_CONFIG --------------------------------------------------

    def insert_node_configs(
        self,
        configs: List[NodeConfig]
    ) -> int:
        Validator.validate(configs, "list")
        for cfg in configs:
            if not isinstance(cfg, NodeConfig):
                raise TypeError(...)
        docs = [cfg.to_dict() for cfg in configs]
        return len(self._col("NODE_CONFIG").insert_many(docs).inserted_ids)

    def list_node_configs(
        self,
        filter_query: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        if filter_query is not None:
            Validator.validate(filter_query, "dict")
        return list(self._col("NODE_CONFIG").find(filter_query or {}))

    # -- SC_TO_CLUSTERS --------------------------------------------------

    def insert_sc_clusters(
        self,
        record: Dict[str, Any]
    ) -> str:
        Validator.validate(record, "dict")
        record["UUID"] = record.get("UUID") or str(uuid.uuid4())
        self._col("SC_TO_CLUSTERS").insert_one(record)
        return record["UUID"]

    def list_sc_clusters(
        self,
        filter_query: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        if filter_query is not None:
            Validator.validate(filter_query, "dict")
        return list(self._col("SC_TO_CLUSTERS").find(filter_query or {}))

    # -- BILLING_AND_COST --------------------------------------------------

    def insert_billing_and_cost(
        self,
        record: Dict[str, Any]
    ) -> str:
        Validator.validate(record, "dict")
        record["UUID"] = record.get("UUID") or str(uuid.uuid4())
        Validator.validate(record.get("supercomputer_center_name"), "str")
        Validator.validate(record.get("service_type"), "str")
        Validator.validate(record.get("cost"), "number")

        col = self._col("BILLING_AND_COST")
        col.insert_one(record)
        return record["UUID"]

    def list_billing_and_cost(
        self,
        filter_query: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        if filter_query is not None:
            Validator.validate(filter_query, "dict")
        return list(self._col("BILLING_AND_COST").find(filter_query or {}))

    # -- TACC_BILLING_INFO --------------------------------------------------

    def insert_tacc_billing(
        self,
        entries: List[Dict[str, Any]]
    ) -> int:
        Validator.validate(entries, "list")
        valid = []
        for e in entries:
            try:
                Validator.validate(e, "dict")
            except (TypeError, ValueError):
                continue
            e["UUID"] = e.get("UUID") or str(uuid.uuid4())
            valid.append(e)

        if not valid:
            return 0

        result = self._col("TACC_BILLING_INFO").insert_many(valid)
        return len(result.inserted_ids)

    def list_tacc_billing(
        self,
        filter_query: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        if filter_query is not None:
            Validator.validate(filter_query, "dict")
        return list(self._col("TACC_BILLING_INFO").find(filter_query or {}))
