import logging

import boto3


def aws_session(profile_name: str, region: str, logger: logging.Logger) -> boto3.Session:
    logger.debug(f"Starting AWS boto3 session")
    logger.debug(f"Profile: {profile_name}")
    logger.debug(f"Region: {region}")
    return boto3.Session(region_name=region, profile_name=profile_name)


def ssm_client(session):
    return session.client("ssm")


def ec2_client(session):
    return session.client("ec2")
