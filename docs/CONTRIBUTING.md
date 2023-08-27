# Contributing

Welcome to Fedora Desktop Configurator!

Feel free to contribute pull requests to fix bugs, add new options, etc.

## Adding a New Option

Options are defined by JSON files in the [`resources/options`](../resources/options) directory of this package.

Options are loaded from file on start up and displayed in the selection GUI.

To add a new option:

1. Browse to [`resources/options`](../resources/options) within this package
2. Open the JSON file that best suits the option you wish to add
    1. For example if you wanted to add a game flatpak you would open `game_flatpaks.json`
    2. If no JSON file that suits your use case create a new file at this time
3. Create a new dictionary entry for your option within the JSON file
    1. Note: Entries are sorted alphabetically by name
4. Populate the dictionary with the following items:
    - `"name": "Example Name"` - `string` containing the name of the option
    - `"description": "Example description"` - `string` containing the description of the option
    - `"documentation_link": "[Example](https://fast.com)"` - **Optional** `string` containing option documentation link
    - `"default_state": true` - `bool` that determines if the option should be enabled by default
    - `"category": "example"` - `string` that determines which category the option should be listed under
        - Available Categories:
            - `"application"`
            - `"emulator"`
            - `"game"`
            - `"gnome_extension"`
            - `"setting"`
            - `"system"`
            - `"vpn"`
    - `"operation_type": "example"` - `string` that tells the application which operation to preform for the option
        - Available Operation Types:
            - `"flatpak"` - Installs a flatpak
            - `"gsettings_value"` - Sets a GSettings value
            - `"package_install"` - Installs an RPM package
            - `"package_install_rpmfusion"` - Installs an RPM pacakge from RPM Fusion
            - `"package_remove"` - Removes an RPM package
            - `"script"` - Executes a script, see [Adding a New Script](#adding-a-new-script)
    - `"operation_args": ["args"]` - `list[string]` that tells the operation what to do for the option
        - Argument values vary based on operation type:
            - `"flatpak"` - List of flatpak IDs, example: `["com.bitwarden.desktop"]`
                - `"gsettings_value"` - List of dictionaries containing GSettings data, example:
                    - ```json
                      {
                           "schema": "org.gnome.desktop.calendar",
                           "key": "show-weekdate",
                           "value": "true"
                      }
                      ```
            - `"package_install"` - List of package names, example: `["firefox"]`
            - `"package_install_rpmfusion"` - List of RPM Fusion package names, example: `["steam"]`
            - `"package_remove"` - List of package names, example: `["firefox"]`
            - `"script"` - List of script names, example: `["gnome_extension/ding"]`
5. Example option dictionary:

```json
    {
    "name": "Archive Manager",
    "description": "Advanced archive manager",
    "default_state": true,
    "category": "application",
    "operation_type": "package_install",
    "operation_args": [
        "file-roller"
    ]
}
```

## Adding a New Script

Complicated actions that cannot be achieved by an existing operation type will need to be implemented as scripts.

Scripts are stored in the [`src/scripts`](../src/scripts) directory of this package.

This package includes many utility functions for use in scripts, see [`src/utils`](../src/utils).

1. Create a new option entry for the script following [Adding a New Option](#adding-a-new-option)
2. Create a new script file in the scripts directory
    1. Script file names need to match what is defined in their respective options,
       example: `["example"]` = `example.py`
3. Add a function called `execute()` to the script
4. Implement script logic within the `execute()` function
