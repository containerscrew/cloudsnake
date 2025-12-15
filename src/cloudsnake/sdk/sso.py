import logging

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

    def list_account_roles(self, account_id: str) -> dict:
        try:
            response = self.client.list_account_roles(accountId=account_id)
            return response
        except Exception as e:
            self.log.error(f"Couldn't list account roles: {str(e)}")
            raise

    def get_role_credentials(self, account_id: str, role_name: str) -> dict:
        try:
            response = self.client.get_role_credentials(
                accountId=account_id, roleName=role_name
            )
            return response
        except Exception as e:
            self.log.error(f"Couldn't get role credentials: {str(e)}")
            raise
