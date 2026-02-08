import os
import time

import boto3
import pytest
from moto import mock_aws

from cloudsnake.sdk.cloudwatch import CloudWatchLogsWrapper


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def mocked_session(aws_credentials):
    """
    Creates a mocked boto3 Session.
    The context 'with mock_aws():' must wrap the session creation.
    """
    with mock_aws():
        yield boto3.Session(region_name="us-east-1")


def test_list_log_groups(mocked_session):
    client = mocked_session.client("logs")
    client.create_log_group(logGroupName="/aws/lambda/test-group-1")
    client.create_log_group(logGroupName="/aws/lambda/test-group-2")

    wrapper = CloudWatchLogsWrapper(session=mocked_session)
    groups = wrapper.list_log_groups()

    assert len(groups) == 2
    names = [g["logGroupName"] for g in groups]
    assert "/aws/lambda/test-group-1" in names


def test_get_historical_logs_pagination(mocked_session):
    # Setup
    client = mocked_session.client("logs")
    log_group = "my-group"
    client.create_log_group(logGroupName=log_group)
    client.create_log_stream(logGroupName=log_group, logStreamName="stream-1")

    # Use current time so it falls within the '1h' window
    now_ms = int(time.time() * 1000)

    client.put_log_events(
        logGroupName=log_group,
        logStreamName="stream-1",
        logEvents=[{"timestamp": now_ms, "message": "Hello World"}],
    )

    wrapper = CloudWatchLogsWrapper(session=mocked_session)
    logs = list(wrapper.get_historical_logs(log_group_arn=log_group, since="1h"))

    assert len(logs) == 1
    assert logs[0]["message"] == "Hello World"
