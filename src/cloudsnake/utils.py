import configparser
import webbrowser
from typing import List, Dict, Optional


def open_browser_url(url: str) -> str | None:
    """Open a URL in the default web browser."""
    try:
        webbrowser.open(url)
    except Exception as e:
        return f"Failed to open browser: {str(e)}. Open the URL manually {url}"


def parse_key_val_list(values: Optional[List[str]]) -> Dict[str, str]:
    parsed: Dict[str, str] = {}
    if not values:
        return parsed

    for item in values:
        for part in item.split(","):
            if "=" not in part:
                raise ValueError(
                    f"Invalid override format '{part}', expected key=value"
                )
            key, value = part.split("=", 1)
            parsed[key] = value

    return parsed


def write_config_file(
    path: str,
    credentials: List[dict],
    region: str,
    account_overrides: Dict[str, str],
    role_overrides: Dict[str, str],
) -> None:
    """Write content to a configuration file."""
    config = configparser.ConfigParser()

    for cred in credentials:
        account_name = cred["AccountName"].replace(" ", "")
        role_name = cred["RoleName"]

        account_part = account_overrides.get(account_name, account_name)

        override_val = role_overrides.get(role_name)
        if override_val is not None and override_val == "":
            profile_name = account_part
        elif override_val is not None:
            profile_name = override_val
        else:
            profile_name = f"{account_part}@{role_name}"

        config[profile_name] = {
            "aws_access_key_id": cred["Credentials"]["AccessKeyId"],
            "aws_secret_access_key": cred["Credentials"]["SecretAccessKey"],
            "aws_session_token": cred["Credentials"]["SessionToken"],
            "region": region,
        }

    with open(path, "w") as config_file:
        config.write(config_file)
