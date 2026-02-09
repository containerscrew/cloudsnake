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
    pretty = "pretty"
    ndjson = "ndjson"


class LoggingLevel(str, Enum):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class PasswordOptions:
    password_length: int
    exclude_characters: str
    exclude_numbers: bool
    exclude_punctuation: bool
    exclude_uppercase: bool
    exclude_lowercase: bool
    include_space: bool
    require_each_included_type: bool
