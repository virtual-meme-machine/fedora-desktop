import pytest

from utils import caffeine_utils


def test_importable():
    """
    Tests that the module can be imported
    :return: None
    """
    import utils.caffeine_utils  # noqa: F401


def test_activate_caffeine(capfd):
    """
    Tests activate_caffeine() with the following use cases:
    - activate_caffeine() when no session is running starts a new one
    - activate_caffeine() when a session is running does nothing
    :param capfd: pytest capture object
    :return: None
    """
    caffeine_utils.activate_caffeine()
    session_cookie = caffeine_utils.CAFFEINE_COOKIE
    assert session_cookie is not None

    caffeine_utils.activate_caffeine()
    assert session_cookie == caffeine_utils.CAFFEINE_COOKIE

    out, err = capfd.readouterr()
    assert out == f"Started caffeine session: {session_cookie}\n"

    # End the caffeine session
    caffeine_utils.deactivate_caffeine()


def test_deactivate_caffeine(capfd):
    """
    Tests deactivate_caffeine() with the following use cases:
    - deactivate_caffeine() when a session is running ends it
    - deactivate_caffeine() when no session is running does nothing
    :param capfd: pytest capture object
    :return: None
    """
    caffeine_utils.activate_caffeine()
    session_cookie = caffeine_utils.CAFFEINE_COOKIE
    assert session_cookie is not None

    caffeine_utils.deactivate_caffeine()
    assert caffeine_utils.CAFFEINE_COOKIE is None

    caffeine_utils.deactivate_caffeine()
    assert caffeine_utils.CAFFEINE_COOKIE is None

    out, err = capfd.readouterr()
    assert out == f"Started caffeine session: {session_cookie}\n" \
                  f"Ended caffeine session: {session_cookie}\n"


def test_deactivate_caffeine_exit(capfd):
    """
    Tests deactivate_caffeine_exit() with the following use cases:
    - deactivate_caffeine_exit() when a session is running ends it and exits
    :param capfd: pytest capture object
    :return: None
    """
    exit_code = 100

    caffeine_utils.activate_caffeine()
    session_cookie = caffeine_utils.CAFFEINE_COOKIE
    assert session_cookie is not None

    with pytest.raises(SystemExit) as system_exit:
        caffeine_utils.deactivate_caffeine_exit(exit_code=exit_code)
        assert system_exit.value.code == exit_code

        out, err = capfd.readouterr()
        assert out == f"Started caffeine session: {session_cookie}\n" \
                      f"Ended caffeine session: {session_cookie}\n"
