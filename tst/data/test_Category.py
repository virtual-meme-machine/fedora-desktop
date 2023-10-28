import pytest

from data import Category


def test_importable():
    """
    Tests that the module can be imported
    :return: None
    """
    import data.Category  # noqa: F401


def test_from_string_valid():
    """
    Tests from_string() with the following use cases:
    - Valid string matching value[0] returns a Category value
    - Valid string matching value[1] returns a Category value
    - Category values loaded from value[0] and value[1] are the same
    :return: None
    """
    valid_string_value_0 = "application"
    valid_string_value_1 = "Install Applications"

    category_string_value_0 = Category.from_string(valid_string_value_0)
    assert category_string_value_0 is Category.Category.APPLICATION
    assert category_string_value_0.value[0] == valid_string_value_0
    assert category_string_value_0.value[1] == valid_string_value_1

    category_string_value_1 = Category.from_string(valid_string_value_1)
    assert category_string_value_1 is Category.Category.APPLICATION
    assert category_string_value_1.value[0] == valid_string_value_0
    assert category_string_value_1.value[1] == valid_string_value_1

    assert category_string_value_0 == category_string_value_1


def test_from_string_invalid():
    """
    Tests from_string() with the following use cases:
    - Invalid string input raises exception
    :return: None
    """
    invalid_string = "not_a_category"

    with pytest.raises(ValueError, match=f"Invalid Category: '{invalid_string}'"):
        Category.from_string(invalid_string)
