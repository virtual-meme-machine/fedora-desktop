def print_header(message: str):
    """
    Prints a nice looking header
    :param message: Message that should be displayed in the header
    :return: None
    """
    print(f"\033[94m\033[1m"
          f"=================================================="
          f"\n{message}\n"
          f"=================================================="
          f"\033[0m")
