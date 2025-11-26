from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Optional, Any

import boto3
from botocore.config import Config


class App(ABC):
    def __init__(
        self,
        session: Optional[boto3.Session] = None,
        region: Optional[str] = None,
        profile: Optional[str] = None,
        filters: Optional[dict] = None,
        query: Optional[Any] = None,
        retries: int = 10,
        **kwargs,
    ):
        self.log = logging.getLogger(self.__class__.__name__)
        self.filters = filters
        self.query = query
        self.session = session
        self.profile = profile
        self.region = region
        self.retries = retries
        self._client = None

    @property
    @abstractmethod
    def client_name(self) -> str:
        pass

    @property
    def client(self):
        if self._client is None:
            if not self.session:
                raise RuntimeError("No boto3 session available")
            self._client = self._create_client()
        return self._client

    def _create_client(self):
        if not self.region and self.session.region_name:
            self.region = self.session.region_name
        if not self.profile and getattr(self.session, "profile_name", None):
            self.profile = self.session.profile_name

        cfg = Config(retries={"max_attempts": self.retries, "mode": "standard"})
        return self.session.client(self.client_name, config=cfg)
