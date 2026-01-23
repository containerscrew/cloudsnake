from __future__ import annotations

import logging
import time
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

    def _parse_time_str(self, time_str: str) -> int:
        """
        Parses a time string (e.g., '1h', '2d', '30m') into a Unix timestamp in milliseconds.
        """
        now_ms = int(time.time() * 1000)

        # Clean string: remove "ago" or spaces if present (e.g. "1h ago" -> "1h")
        clean_str = time_str.lower().replace("ago", "").strip()

        if not clean_str:
            return 0

        # Extract unit and value
        try:
            unit = clean_str[-1]
            # Handle cases where user might type just "100" (assume minutes or handle error)
            if unit.isdigit():
                value = int(clean_str)
                unit = "m"  # Default to minutes if no unit provided
            else:
                value = int(clean_str[:-1])
        except ValueError:
            self.log.warning(f"Could not parse time '{time_str}', defaulting to 1h ago")
            value = 1
            unit = "h"

        multiplier = 1000  # Seconds
        if unit == "m":  # Minutes
            multiplier *= 60
        elif unit == "h":  # Hours
            multiplier *= 3600
        elif unit == "d":  # Days
            multiplier *= 86400
        elif unit == "w":  # Weeks
            multiplier *= 604800

        delta_ms = value * multiplier
        return now_ms - delta_ms
