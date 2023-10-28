from data import Info


def test_importable():
    """
    Tests that the module can be imported
    :return: None
    """
    import data.Info  # noqa: F401


def test_get_application_version_valid_package_root():
    """
    Tests get_application_version() with the following use cases:
    - Valid package root returns application version with git commit appended
    :return: None
    """
    application_version = Info.get_application_version()

    assert f"{Info.APPLICATION_VERSION}-git-" in application_version


def test_get_application_version_invalid_package_root():
    """
    Tests get_application_version() with the following use cases:
    - Valid package root returns hardcoded application version
    :return: None
    """
    application_version = Info.get_application_version(package_root="/dev/null")

    assert application_version == Info.APPLICATION_VERSION
