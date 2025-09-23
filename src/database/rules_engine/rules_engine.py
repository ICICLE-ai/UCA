from __future__ import annotations
from typing import Any, Dict, List, Optional
import requests

from .config import Config


class RulesEngine:
    """
    Thin client for the UCA Rules Engine API.
    - base_url comes strictly from Config.BASE_URL (loaded from config.yaml)
    - User supplies a Tapis access token to authorize calls
    """

    def __init__(
        self,
        tapis_token: str,
        *,
        use_query_token: bool = False,
        timeout: float = 30.0,
        session: Optional[requests.Session] = None,
    ):
        self.base_url = Config.BASE_URL.rstrip("/")
        self.tapis_token = tapis_token
        self.s = session or requests.Session()
        self.use_query_token = use_query_token
        self.timeout = timeout

    # ---------- plumbing ----------
    def _headers(self) -> Optional[Dict[str, str]]:
        if self.use_query_token:
            return None
        return {"Authorization": f"Bearer {self.tapis_token}"}

    def _params(self, extra: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        params: Dict[str, Any] = {}
        if self.use_query_token:
            params["tapis_token"] = self.tapis_token
        if extra:
            params.update(extra)
        return params or None

    @staticmethod
    def _raise_if_error(r: requests.Response) -> None:
        if r.status_code >= 400:
            try:
                detail = r.json()
            except Exception:
                detail = r.text
            raise requests.HTTPError(f"{r.status_code}: {detail}", response=r)

    def _get(self, path: str, **kw):
        r = self.s.get(
            f"{self.base_url}{path}",
            headers=self._headers(),
            params=self._params(kw.pop("params", None)),
            timeout=self.timeout,
            **kw,
        )
        self._raise_if_error(r)
        return r.json()

    def _post(self, path: str, **kw):
        r = self.s.post(
            f"{self.base_url}{path}",
            headers=self._headers(),
            params=self._params(kw.pop("params", None)),
            timeout=self.timeout,
            **kw,
        )
        self._raise_if_error(r)
        return r.json()

    def _patch(self, path: str, **kw):
        r = self.s.patch(
            f"{self.base_url}{path}",
            headers=self._headers(),
            params=self._params(kw.pop("params", None)),
            timeout=self.timeout,
            **kw,
        )
        self._raise_if_error(r)
        return r.json()

    def _delete(self, path: str, **kw):
        r = self.s.delete(
            f"{self.base_url}{path}",
            headers=self._headers(),
            params=self._params(kw.pop("params", None)),
            timeout=self.timeout,
            **kw,
        )
        self._raise_if_error(r)
        return r.json()

    # ---------- public API ----------
    def health(self) -> Dict[str, Any]:
        return self._get("/health")

    def create_rule(self, rule: Dict[str, Any]) -> str:
        out = self._post("/rules", json=rule)
        return out["Rule_UUID"]

    def list_rules(self) -> List[Dict[str, Any]]:
        out = self._get("/rules")
        return out.get("items", [])

    def get_rule(self, rule_uuid: str) -> Dict[str, Any]:
        return self._get(f"/rules/{rule_uuid}")

    def update_rule(self, rule_uuid: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        return self._patch(f"/rules/{rule_uuid}", json={"updates": updates})

    def delete_rule(self, rule_uuid: str) -> Dict[str, Any]:
        return self._delete(f"/rules/{rule_uuid}")