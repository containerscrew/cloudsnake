from dataclasses import dataclass
from enum import Enum
import boto3


@dataclass
class Common:
    session: boto3.Session
    profile: str
    region: str


@dataclass
class DeviceRegistration:
    client_id: str
    client_secret: str


@dataclass
class DeviceCode:
    device_code: str
    user_code: str
    verification_uri_complete: str


class OutputMode(str, Enum):
    json = "json"
    table = "table"
    text = "text"


class LoggingLevel(str, Enum):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
