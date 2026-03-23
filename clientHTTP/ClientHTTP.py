from __future__ import annotations

from typing import Any

import requests

STUDENT_ID = "MILLOT_CHALON"

class ClientHTTPError(Exception):
    """Raised when the HTTP client cannot complete a valid request."""


class ClientHTTP:
    def __init__(self, base_url: str = "https://tsp-sra0.onrender.com", timeout: int = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def list_instances(self) -> dict[str, Any]:
        """GET /instances"""
        return self._request("GET", "/instances")

    def get_instance(self, instance_id: str) -> dict[str, Any]:
        """GET /instances/{instance_id}"""
        return self._request("GET", f"/instances/{instance_id}")

    def submit_solution(
        self,
        instance_id: str,
        tour: list[int],
    ) -> dict[str, Any]:
        """POST /submit"""
        payload = {
            "student_id": STUDENT_ID,
            "instance_id": instance_id,
            "tour": tour,
        }
        return self._request("POST", "/submit", json=payload)

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        except requests.RequestException as exc:
            raise ClientHTTPError(f"Erreur de communication avec le serveur: {exc}") from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise ClientHTTPError(
                f"Réponse invalide du serveur (code HTTP {response.status_code})"
            ) from exc

        if response.ok:
            return data

        detail = data.get("detail") if isinstance(data, dict) else None
        message = detail or f"Erreur HTTP {response.status_code}"
        raise ClientHTTPError(message)

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> "ClientHTTP":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
