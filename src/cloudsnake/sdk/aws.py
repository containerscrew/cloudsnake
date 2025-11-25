import logging
from botocore.config import Config


class App:
    """
    Common AWS wrapper base class for cloudsnake SDK.
    Provides: logging, client creation, session storage, region/profile propagation.
    """

    def __init__(
        self,
        client=None,
        filters=None,
        query=None,
        profile=None,
        region=None,
        session=None,
        **kwargs,
    ):
        self.log = logging.getLogger("cloudsnake")

        self.filters = filters
        self.query = query
        self.client_name = client
        self.profile = profile
        self.region = region
        self.session = session
        self.client = None


    def create_client(self, session):
        """
        Create a boto3 client using the provided session.
        Stores the session, region, and profile internally.
        """
        self.session = session
        try:
            if not self.region:
                self.region = session.region_name
            if not self.profile and hasattr(session, 'profile_name'):
                self.profile = session.profile_name
        except Exception:
            pass

        config = Config(retries={"max_attempts": 10, "mode": "standard"})

        self.client = session.client(self.client_name, config=config)
        return self.client
