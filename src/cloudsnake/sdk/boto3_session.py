import logging
import os
import boto3


class SessionWrapper:
    """Encapsulates AWS boto3 Session operations"""

    def __init__(self, profile: str | None = None, region: str = "us-east-1"):
        """
        :param profile: AWS credentials profile (defaults to value in AWS_PROFILE).
        :param region: AWS region.
        """
        self.log = logging.getLogger("cloudsnake.session")

        self.profile = profile or os.getenv("AWS_PROFILE")
        self.region = region

        if not self.profile:
            self.log.warning("No AWS profile provided. Using environment default.")

        self.log.debug(
            f"SessionWrapper initialized with profile={self.profile} region={self.region}"
        )

    def with_local_session(self) -> boto3.Session:
        """Return a boto3 Session using ~/.aws/credentials"""
        self.log.debug("Using local AWS credentials via ~/.aws/credentials")
        return boto3.Session(
            profile_name=self.profile,
            region_name=self.region,
        )

    def with_sts_assume_role_session(self, role_arn: str) -> boto3.Session:
        """Return a boto3 Session via STS AssumeRole"""
        self.log.debug(f"Assuming role via STS: {role_arn}")

        base_session = boto3.Session(
            profile_name=self.profile,
            region_name=self.region,
        )
        sts = base_session.client("sts")

        response = sts.assume_role(
            RoleArn=role_arn,
            RoleSessionName="cloudsnake-session",
        )

        creds = response["Credentials"]

        assumed = boto3.Session(
            aws_access_key_id=creds["AccessKeyId"],
            aws_secret_access_key=creds["SecretAccessKey"],
            aws_session_token=creds["SessionToken"],
            region_name=self.region,
        )

        self.log.debug("AssumeRole session created successfully")
        return assumed
