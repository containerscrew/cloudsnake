from dataclasses import dataclass
from enum import Enum
import boto3


@dataclass
class Common:
    session: boto3.Session
    profile: str
    region: str


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
