from __future__ import annotations

import boto3
import logging
import os
from typing import Optional


class SessionWrapper:
    def __init__(self, profile: Optional[str] = None, region: str = "us-east-1"):
        self.log = logging.getLogger("cloudsnake.session")
        self.profile = profile or os.getenv("AWS_PROFILE")
        self.region = region

        if not self.profile:
            self.log.debug(
                "No AWS profile provided, falling back to environment defaults"
            )

        self.log.debug(f"SessionWrapper(profile={self.profile}, region={self.region})")

    def with_local_session(self) -> boto3.Session:
        self.log.debug("Creating local boto3.Session using ~/.aws/credentials")
        return boto3.Session(profile_name=self.profile, region_name=self.region)

    def with_sts_assume_role_session(self, role_arn: str) -> boto3.Session:
        self.log.debug(f"Assuming role via STS: {role_arn}")

        base = boto3.Session(profile_name=self.profile, region_name=self.region)
        sts = base.client("sts")

        res = sts.assume_role(RoleArn=role_arn, RoleSessionName="cloudsnake-session")
        creds = res["Credentials"]

        session = boto3.Session(
            aws_access_key_id=creds["AccessKeyId"],
            aws_secret_access_key=creds["SecretAccessKey"],
            aws_session_token=creds["SessionToken"],
            region_name=self.region,
        )

        self.log.debug("STS assumed role session created")
        return session
