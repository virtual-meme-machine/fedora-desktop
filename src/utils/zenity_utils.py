import getpass
import subprocess

USE_CLI_PROMPTS: bool = False
ZENITY_EXEC: str = "/usr/bin/zenity"


def __input_prompt_cli(prompt_text: str, use_getpass: bool = False) -> str or None:
    """
    Prompts the user to input text via the CLI
    :param prompt_text: Prompt text that describes what the user should enter
    :param use_getpass: Get CLI input from getpass instead of input
    :return: String containing the text that was entered by the user, or None if cancelled
    """
    text_input = (input, getpass.getpass)[use_getpass](f"{prompt_text} (enter 'cancel' to cancel): ")
    if text_input == "cancel":
        print("Input cancelled")
        return None
    else:
        return text_input


def __input_prompt_gui(zenity_args: list[str],
                       title: str,
                       prompt_text: str,
                       cancel_label: str = "Cancel",
                       ok_label: str = "Submit") -> str or None:
    """
    Prompts the user to input text via the GUI
    :param zenity_args: List of arguments that should be passed to zenity
    :param title: Title of the prompt window
    :param prompt_text: Prompt text that describes what the user should enter
    :param cancel_label: Label for the cancel button
    :param ok_label: Label for the ok button
    :return: String containing the text that was entered by the user, or None if cancelled
    """
    try:
        print(f"{prompt_text} in the prompt window")
        return subprocess.run([ZENITY_EXEC,
                               "--modal",
                               f"--title={title}",
                               f"--text={prompt_text}",
                               f"--cancel-label={cancel_label}",
                               f"--ok-label={ok_label}"] + zenity_args,
                              capture_output=True,
                              check=True,
                              text=True).stdout.strip()
    except subprocess.CalledProcessError as err:
        if err.returncode == 1:
            print("Input cancelled")
            return None


def prompt_form(title: str,
                prompt_text: str,
                prompt_fields: list[str]) -> list[str] or None:
    """
    Prompts the user to enter multiple lines of text via a form
    :param title: Title of the prompt window
    :param prompt_text: Prompt text that describes what the user should enter
    :param prompt_fields: List of fields that the form should contain
    :return: List of strings containing the text that was entered by the user, or None if cancelled
    """
    # CLI
    if USE_CLI_PROMPTS:
        input_list = []
        print(prompt_text)
        for prompt in prompt_fields:
            cli_input = __input_prompt_cli(prompt_text=prompt)
            if cli_input is None:
                return None
            else:
                input_list.append(cli_input)
        return input_list

    # GUI
    form = __input_prompt_gui(zenity_args=["--forms"] + list(map(lambda field: f"--add-entry={field}", prompt_fields)),
                              title=title,
                              prompt_text=prompt_text)
    if form is None:
        return None
    else:
        return form.split("|")


def prompt_info(title: str,
                gui_text: str,
                cli_text: str,
                ok_label: str) -> bool:
    """
    Prompts the user with an info dialog window
    :param title: Title of the prompt window
    :param gui_text: Message that should be displayed in the GUI
    :param cli_text: Message that should be displayed in the CLI
    :param ok_label: Label for the ok button
    :return: True if prompt was presented, False if failed to present or cancelled
    """
    # CLI
    if USE_CLI_PROMPTS:
        print(title)
        print(cli_text)
        return True

    # GUI
    try:
        print(cli_text)
        subprocess.run([ZENITY_EXEC,
                        "--info",
                        "--modal",
                        f"--title={title}",
                        f"--text={gui_text}",
                        f"--ok-label={ok_label}"], check=True)
        return True
    except subprocess.CalledProcessError as err:
        if err.returncode == 1:
            return False


def prompt_password(title: str = "Authentication Required",
                    prompt_text: str = "Please enter your password") -> str or None:
    """
    Prompts the user to enter their password in a secure field
    :param title: Title of the prompt window
    :param prompt_text: Prompt text that describes what the user should enter
    :return: String containing the password that was entered by the user, or None if cancelled
    """
    # CLI
    if USE_CLI_PROMPTS:
        return __input_prompt_cli(prompt_text=prompt_text, use_getpass=True)

    # GUI
    return __input_prompt_gui(zenity_args=["--password"],
                              title=title,
                              prompt_text=prompt_text)


def prompt_text_entry(title: str,
                      prompt_text: str) -> str or None:
    """
    Prompts the user to enter some text
    :param title: Title of the prompt window
    :param prompt_text: Prompt text that describes what the user should enter
    :return: String containing the text that was entered by the user, or None if cancelled
    """
    # CLI
    if USE_CLI_PROMPTS:
        return __input_prompt_cli(prompt_text=prompt_text)

    # GUI
    return __input_prompt_gui(zenity_args=["--entry"],
                              title=title,
                              prompt_text=prompt_text)


def set_use_cli_prompts(value: bool):
    """
    Sets the value of USE_CLI_PROMPTS
    If USE_CLI_PROMPTS is True CLI prompts will be used instead of zenity
    :param value: New value for USE_CLI_PROMPTS
    :return: None
    """
    global USE_CLI_PROMPTS
    USE_CLI_PROMPTS = value
