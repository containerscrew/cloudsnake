import logging

from cloudsnake.sdk.aws import App


class SecretsManagerWrapper(App):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.secrets = []
        self.log = logging.getLogger("cloudsnake.secrets_manager")

    @property
    def client_name(self) -> str:
        return "secretsmanager"

    def list_secrets(self):
        try:
            paginator = self.client.get_paginator("list_secrets")
            self.secrets = []
            for page in paginator.paginate(SortBy="created-date"):
                if "SecretList" in page:
                    self.secrets.extend(page["SecretList"])
            return self.secrets

        except Exception as err:
            self.log.error(
                "Couldn't list secrets from Secrets Manager: %s",
                err,
            )
            raise

    def get_secret_value_by_name(self, name: str):
        try:
            response = self.client.get_secret_value(SecretId=name)
            return response["SecretString"]
        except Exception as err:
            self.log.error(
                "Couldn't get secret value from Secrets Manager: %s",
                err,
            )
            raise
