from typing import Tuple

from botocore.exceptions import ClientError

# @dataclass
# class DeviceAuthorization:
#     verificationUriComplete: str
#     : float
#     lat: float


class SSOIDCWrapper:
    def __init__(self, session, client, **kwargs):
        # Inheriting the properties of parent class
        super().__init__(session, client, **kwargs)

    def device_registration(
        self, client_name: str = "sso-client", client_type: str = "public"
    ) -> Tuple[str, str]:
        try:
            response_client_registration = self.client.register_client(
                clientName=client_name,
                clientType=client_type,
            )
            return response_client_registration[
                "clientId"
            ], response_client_registration["clientSecret"]
        except:
            raise

    def get_auth_device(self, client_id, client_secret, start_url):
        try:
            response_device_authorization = self.client.start_device_authorization(
                clientId=client_id,
                clientSecret=client_secret,
                startUrl=start_url,
            )
            print(response_device_authorization)
            return (
                response_device_authorization["verificationUriComplete"],
                response_device_authorization["deviceCode"],
                response_device_authorization["userCode"],
            )
        except ClientError as err:
            self.log.error(
                "Couldn't get auth device",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
