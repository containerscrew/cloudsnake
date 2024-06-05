import logging
from botocore.config import Config

class SSO_OIDC:
    def __init__(self, session, **kwargs):
        self.log = logging.getLogger("cloudsnake")
        self.sso_client = self.create_sso_oidc_client(session)
        self.kwargs = kwargs

    @staticmethod
    def create_sso_oidc_client(session):
        config = Config(retries={"max_attempts": 10, "mode": "standard"})
        return session.client("sso-oidc", config=config)
    
class SSOWrapper(SSO_OIDC):
    def __init__(self, session, **kwargs):
        # Inheriting the properties of parent class
        super().__init__(session, **kwargs)


    def device_registration(self, client_name: str = "sso-client", client_type:str = "public") -> None:
        try:
            response_client_registration = self.sso_client.register_client(
                clientName= client_name,
                clientType= client_type,
            )
            return response_client_registration
        except Exception as e:
            self.log.error(f"Failed to register the device! {e}")
