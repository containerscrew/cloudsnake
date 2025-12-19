import logging
from typing import List

from cloudsnake.sdk.aws import App


class SSOWrapper(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log = logging.getLogger("cloudsnake.sso")

    @property
    def client_name(self) -> str:
        return "sso"

    def list_accounts(self, token: str) -> dict:
        try:
            response = self.client.list_accounts(maxResults=123, accessToken=token)
            return response
        except Exception as e:
            self.log.error(f"Couldn't list accounts: {str(e)}")
            raise

    def list_account_roles(self, account_id: str, token: str) -> dict:
        try:
            response = self.client.list_account_roles(
                accountId=account_id, accessToken=token
            )
            return response
        except Exception as e:
            self.log.error(f"Couldn't list account roles: {str(e)}")
            raise

    def get_role_credentials(self, account_id: str, role_name: str, token: str) -> dict:
        try:
            response = self.client.get_role_credentials(
                accountId=account_id, roleName=role_name, accessToken=token
            )
            return response["roleCredentials"]
        except Exception as e:
            self.log.error(f"Couldn't get role credentials: {str(e)}")
            raise

    def get_credentials_by_role(
        self, account_id: str, role_name: str, token: str
    ) -> dict:
        role_credentials = self.get_role_credentials(account_id, role_name, token)
        credentials = {
            "AccessKeyId": role_credentials["accessKeyId"],
            "SecretAccessKey": role_credentials["secretAccessKey"],
            "SessionToken": role_credentials["sessionToken"],
            "Expiration": role_credentials["expiration"],
        }
        return credentials

    def get_credentials(
        self, account_id: str, account_name: str, token: str
    ) -> List[dict]:
        roles = self.list_account_roles(account_id, token)
        all_credentials = []
        for role in roles.get("roleList", []):
            role_name = role["roleName"]
            credentials = self.get_credentials_by_role(account_id, role_name, token)
            credentials_info = {
                "AccountId": account_id,
                "AccountName": account_name,
                "RoleName": role_name,
                "Credentials": credentials,
            }
            all_credentials.append(credentials_info)
        return all_credentials
