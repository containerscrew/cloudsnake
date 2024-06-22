import logging
import os
import boto3


class SessionWrapper:
    """Encapsulates Amazon boto3 Session operations"""

    def __init__(
        self, profile: str = os.getenv("AWS_PROFILE"), region: str = "us-east-1"
    ):
        """
        :param profile: AWS credentials profile to be used. Check your ~/.aws/credentials
        :param region: AWS region to operate.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html
        """
        self.log = logging.getLogger("cloudsnake")
        self.region = region
        self.profile = profile

    def with_local_session(self) -> boto3.Session:
        self.log.debug(
            "Starting boto3 session using local credentials located in ~/.aws/credentials"
        )
        return boto3.Session(region_name=self.region, profile_name=self.profile)

    def with_sts_assume_role_session(self, role_arn) -> boto3.Session:
        self.log.debug("Starting boto3 session with sts assume role")
        session = boto3.Session(region_name=self.region, profile_name=self.profile)
        sts = session.client("sts")
        response = sts.assume_role(
            RoleArn=role_arn, RoleSessionName="custom-session-using-role"
        )
        new_session = boto3.Session(
            aws_access_key_id=response["Credentials"]["AccessKeyId"],
            aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
            aws_session_token=response["Credentials"]["SessionToken"],
        )

        return new_session
