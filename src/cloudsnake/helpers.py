from datetime import datetime

from typing_extensions import List, Dict


def parse_filters(filters: str) -> List[Dict[str, List[str]]]:
    """Parse filters passed in commands like cloudsnake ec2 describe-instances --filters Name=instance-state-name,
    Values=running"""
    parsed_filters = []
    filter_parts = filters.split(",")

    # Check if the filter format is correct
    if any("=" not in part for part in filter_parts):
        raise ValueError("Filter string is not in the correct format")

    filter_dict = {"Name": "", "Values": []}
    for part in filter_parts:
        key, value = part.split("=")
        if key == "Name":
            filter_dict["Name"] = value
        elif key == "Values":
            filter_dict["Values"].append(value)
        else:
            raise ValueError(f"Unexpected key: {key}")
    parsed_filters.append(filter_dict)
    return parsed_filters


def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")
