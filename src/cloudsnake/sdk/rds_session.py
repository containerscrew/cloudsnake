import errno
import os
import subprocess
import jmespath
import requests
from cloudsnake.helpers import (
    ensure_directory_exists,
    ignore_user_entered_signals,
    parse_filters,
)
from cloudsnake.sdk.aws import App
from rich import print
from botocore.exceptions import ClientError


MYSQL_CLIENT__ERROR_MESSAGE = (
    "Mysql binary client not found",
    "Please refer to mysql client installation here: ",
    "https://dev.mysql.com/doc/mysql-getting-started/en/#mysql-getting-started-installing",
)


class RDSInstanceConnectWrapper(App):
    """Encapsulates Amazon RDS Instance Connect actions."""

    def __init__(self, client, **kwargs):
        # Call the superclass __init__ method
        super().__init__(client, **kwargs)
        self.db_hostname = kwargs.get("hostname", None)
        self.db_username = kwargs.get("db_username", None)
        self.port = kwargs.get("port", 3306)
        self.region = kwargs.get("region", None)
        self.cert = kwargs.get("cert", None)

    def describe_db_instances(self):
        instances = {}
        if self.filters:
            parsed_filters = parse_filters(self.filters)
        else:
            parsed_filters = []

        self.log.info("Describing RDS instances")
        try:
            paginator = self.client.get_paginator("describe_db_instances")

            for page in paginator.paginate(Filters=parsed_filters):
                instances.update(page)

            if self.query is not None:
                result = jmespath.search(self.query, instances)
                return result
            else:
                return instances
        except ClientError as err:
            self.log.error(
                "Couldn't register device",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def get_db_auth_token(self) -> None:
        """
        Retrieves the authentication token for the database.

        Returns:
            str: The authentication token for the database.

        Raises:
            ClientError: If there is an error while retrieving the authentication token.
        """
        try:
            token = self.client.generate_db_auth_token(
                DBHostname=self.db_hostname,
                Region=self.region,
                DBUsername=self.db_username,
                Port=self.port,
            )
            return token
        except ClientError as err:
            self.log.error(
                "Couldn't get auth device",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def download_cert(self, save_path: str):
        url = f"https://truststore.pki.rds.amazonaws.com/{self.region}/{self.region}-bundle.pem"
        try:
            response = requests.get(url)
            response.raise_for_status()  # This will raise an exception for error HTTP status codes
            ensure_directory_exists(
                save_path
            )  # Create directories if they do not exist
            file_path = os.path.join(save_path, f"rds-cert-{self.region}.pem")
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Certificate downloaded and saved as {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading the certificate: {e}")

    def db_connect(self, token: str):
        """
        Connects to the RDS instance using the provided token.

        Args:
            token (str): The token used for authentication.

        Returns:
            int: Returns 0 if the connection is successful.

        Raises:
            subprocess.CalledProcessError: If there is an error while connecting to the instance.
            ValueError: If the MySQL client is not present in the local system.
            OSError: If there is an OS error.

        """
        try:
            print(
                f"[bold green]Connecting to the RDS instance:[/bold green] {self.db_hostname} [red]Please wait[/red]:) :rocket:"
            )
            print(
                "[bold red]IMPORTANT! For security reasons TLS/SSL is always necessary to connect to the RDS instance. --skip-ssl is not allowed by the moment[/bold red]"
            )
            with ignore_user_entered_signals():
                subprocess.check_call(
                    [
                        "mariadb",
                        f"--host={self.db_hostname}",
                        f"--port={self.port}",
                        f"--ssl-ca={self.cert}",
                        f"--user={self.db_username}",
                        f"--password={token}",
                    ]
                )
            return 0
        except subprocess.CalledProcessError as e:
            self.log.error(f"Failed to connect to the instance {e}", exc_info=True)
            raise
        except OSError as ex:
            if ex.errno == errno.ENOENT:
                self.log.error(
                    "mysql client is not present in your local system",
                    MYSQL_CLIENT__ERROR_MESSAGE,
                    exc_info=True,
                )
                raise ValueError("Mysql client is not present") from ex
            else:
                self.log.error("OS error", exc_info=True)
                raise
