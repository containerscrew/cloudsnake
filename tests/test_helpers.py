from datetime import datetime
import os
import pytest
from cloudsnake.helpers import (
    ensure_directory_exists,
    ensure_is_valid_dir,
    parse_filters,
    serialize_datetime,
)


"""Testing function parse_filters"""


def test_parse_filters_single_value():
    filters = "Name=instance-state-name,Values=running"
    expected_output = [{"Name": "instance-state-name", "Values": ["running"]}]
    assert parse_filters(filters) == expected_output


def test_parse_filters_multiple_values():
    filters = "Name=instance-state-name,Values=running|stopped"
    expected_output = [
        {"Name": "instance-state-name", "Values": ["running", "stopped"]}
    ]
    assert parse_filters(filters) == expected_output


def test_parse_filters_no_values():
    filters = "Name=instance-state-name"
    expected_output = [{"Name": "instance-state-name", "Values": []}]
    assert parse_filters(filters) == expected_output


def test_parse_filters_invalid_format():
    filters = "Name=instance-state-name,Value=running"
    with pytest.raises(ValueError):
        parse_filters(filters)


def test_parse_filters_unexpected_key():
    filters = "Name=instance-state-name,InvalidKey=running"
    with pytest.raises(ValueError):
        parse_filters(filters)


def test_parse_filters_empty_values():
    filters = "Name=instance-state-name,Values="
    expected_output = [{"Name": "instance-state-name", "Values": [""]}]
    assert parse_filters(filters) == expected_output


"""Testing function serialize_datetime"""


def test_serialize_datetime():
    # Test para asegurarse de que una instancia de datetime se serializa correctamente.
    dt = datetime(2024, 6, 8, 12, 0, 0)
    result = serialize_datetime(dt)
    assert result == "2024-06-08T12:00:00"


def test_serialize_non_datetime():
    # Test para asegurarse de que un objeto que no es datetime lanza un TypeError.
    with pytest.raises(TypeError, match="Type not serializable"):
        serialize_datetime("2024-06-08T12:00:00")


@pytest.fixture(scope="function")
def mock_directory(tmpdir):
    """Fixture that creates a temporary directory."""
    return str(tmpdir.mkdir("test_dir"))


def test_ensure_is_valid_dir():
    """Test that ensure_directory_exists raises an error if directory doesn't exist."""
    with pytest.raises(NotADirectoryError):
        ensure_is_valid_dir("invalid_directory.txt")


def test_ensure_directory_exists(mock_directory):
    """Test that ensure_directory_exists raises an error if directory doesn't exist."""
    filepath = os.path.join(mock_directory, "test_file.txt")
    with pytest.raises(FileNotFoundError):
        ensure_directory_exists(filepath)
