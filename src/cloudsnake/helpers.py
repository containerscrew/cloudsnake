import contextlib
from datetime import datetime
import os
import signal
import sys

from typing_extensions import List, Dict


def parse_filters(filters: str) -> List[Dict[str, List[str]]]:
    """Parse filters passed in commands like cloudsnake ec2 describe-instances --filters Name=instance-state-name,
    Values=running"""
    parsed_filters = []
    filter_parts = filters.split(",")

    # Check if the filter format is correct
    # if any("=" not in part for part in filter_parts):
    #     raise ValueError("Filter string is not in the correct format")

    filter_dict = {"Name": "", "Values": []}
    for part in filter_parts:
        key, value = part.split("=")
        if key == "Name":
            filter_dict["Name"] = value
        elif key == "Values":
            if "|" in value:
                values = value.split("|")
                for value in values:
                    filter_dict["Values"].append(value)
            else:
                filter_dict["Values"].append(value)
        else:
            raise ValueError(f"Unexpected key: {key}")
    parsed_filters.append(filter_dict)
    return parsed_filters


def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


is_windows = sys.platform == "win32"


@contextlib.contextmanager
def ignore_user_entered_signals():
    """
    Ignores user entered signals to avoid process getting killed.
    """
    if is_windows:
        signal_list = [signal.SIGINT]
    else:
        signal_list = [signal.SIGINT, signal.SIGQUIT, signal.SIGTSTP]
    actual_signals = []
    for user_signal in signal_list:
        actual_signals.append(signal.signal(user_signal, signal.SIG_IGN))
    try:
        yield
    finally:
        for sig, user_signal in enumerate(signal_list):
            signal.signal(user_signal, actual_signals[sig])


def ensure_directory_exists(dirpath):
    """
    Ensure that the specified directory exists.

    Args:
        dirpath (str): The path of the directory to check.

    Raises:
        FileNotFoundError: If the directory does not exist.

    """
    if not os.path.exists(dirpath):
        raise FileNotFoundError(f"Directory '{dirpath}' does not exist.")


def ensure_is_valid_dir(dirpath):
    """
    Ensure that the given directory path is valid.

    Args:
        dirpath (str): The directory path to check.

    Raises:
        NotADirectoryError: If the given path is not a directory.

    """
    if not os.path.isdir(dirpath):
        raise NotADirectoryError(f"'{dirpath}' is not a directory.")
