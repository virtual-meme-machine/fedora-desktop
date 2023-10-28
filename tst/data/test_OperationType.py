import pytest

from data import OperationType


def test_importable():
    """
    Tests that the module can be imported
    :return: None
    """
    import data.OperationType  # noqa: F401


def test_from_string_valid():
    """
    Tests from_string() with the following use cases:
    - Valid string input returns a Category value
    :return: None
    """
    valid_string = "flatpak"

    category = OperationType.from_string(valid_string)
    assert category is OperationType.OperationType.FLATPAK
    assert category.value == valid_string


def test_from_string_invalid():
    """
    Tests from_string() with the following use cases:
    - Invalid string input raises exception
    :return: None
    """
    invalid_string = "not_valid"

    with pytest.raises(ValueError, match=f"Invalid OperationType: '{invalid_string}'"):
        OperationType.from_string(invalid_string)
