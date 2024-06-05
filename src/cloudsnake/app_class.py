"""
Main class with some globals
Encapsulate some redundant logic for each Wrapper
"""

import logging
from botocore.config import Config


class App:
    def __init__(self, session, client, **kwargs):
        self.log = logging.getLogger("cloudsnake")
        self.kwargs = kwargs
        self.client = self.create_client(session, client)

    @staticmethod
    def create_client(session, client):
        config = Config(retries={"max_attempts": 10, "mode": "standard"})
        return session.client(client, config=config)