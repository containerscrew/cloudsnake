import logging

from cloudsnake.cli.dto import DeviceRegistration, DeviceCode
from cloudsnake.sdk.aws import App


class SSOOIDCWrapper(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log = logging.getLogger("cloudsnake.sso")

    @property
    def client_name(self) -> str:
        return "sso-oidc"

    def register_device_code(
        self, client_name: str, client_type: str
    ) -> DeviceRegistration:
        try:
            response_client_registration = self.client.register_client(
                clientName=client_name,
                clientType=client_type,
            )
            return DeviceRegistration(
                client_id=response_client_registration["clientId"],
                client_secret=response_client_registration["clientSecret"],
            )
        except Exception as e:
            self.log.error(f"Couldn't register device: {str(e)}")
            raise

    def create_device_code(
        self, client_id: str, client_secret: str, start_url: str
    ) -> DeviceCode:
        try:
            response_device_code = self.client.start_device_authorization(
                clientId=client_id,
                clientSecret=client_secret,
                startUrl=start_url,
            )
            return DeviceCode(
                device_code=response_device_code["deviceCode"],
                user_code=response_device_code["userCode"],
                verification_uri_complete=response_device_code[
                    "verificationUriComplete"
                ],
            )
        except Exception as e:
            self.log.error(f"Couldn't create device code: {str(e)}")
            raise

    def create_token(
        self, client_id: str, client_secret: str, device_code: str, grant_type: str
    ) -> str:
        try:
            response_token = self.client.create_token(
                clientId=client_id,
                clientSecret=client_secret,
                deviceCode=device_code,
                grantType=grant_type,
            )
            return response_token["accessToken"]
        except Exception as e:
            self.log.error(f"Couldn't create token: {str(e)}")
            raise
