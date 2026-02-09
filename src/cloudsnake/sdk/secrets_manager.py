import logging

from cloudsnake.cli.dto import PasswordOptions
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

    def generate_random_password(self, options: PasswordOptions):
        try:
            response = self.client.get_random_password(
                PasswordLength=options.password_length,
                ExcludeCharacters=options.exclude_characters,
                ExcludeNumbers=options.exclude_numbers,
                ExcludePunctuation=options.exclude_punctuation,
                ExcludeUppercase=options.exclude_uppercase,
                ExcludeLowercase=options.exclude_lowercase,
                IncludeSpace=options.include_space,
                RequireEachIncludedType=options.require_each_included_type,
            )
            return response["RandomPassword"]
        except Exception as err:
            self.log.error(
                "Couldn't generate random password from Secrets Manager: %s",
                err,
            )
            raise
