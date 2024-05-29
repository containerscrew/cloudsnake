from typing_extensions import List, Dict


def parse_filters(filters: List[str]) -> List[Dict[str, List[str]]]:
    """Parse filters passed in commands like cloudsnake ec2 describe-instances --filters Name=instance-state-name,
    Values=running"""
    parsed_filters = []
    for filter_str in filters:
        filter_parts = filter_str.split(",")
        filter_dict = {"Name": "", "Values": []}
        for part in filter_parts:
            key, value = part.split("=")
            if key == "Name":
                filter_dict["Name"] = value
            elif key == "Values":
                filter_dict["Values"].append(value)
        parsed_filters.append(filter_dict)
    return parsed_filters
