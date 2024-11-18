# Unity Screenshot Automation Tool

A Python script to automate capturing screenshots of the Unity application on macOS. The tool captures screenshots at specified intervals only when Unity is the active (frontmost) application and saves them in the desired image format.

## Features

- **Automated Screenshots:** Capture screenshots of the Unity window at regular intervals.
- **Active Window Detection:** Only captures screenshots when Unity is the frontmost application.
- **Customizable Settings:** Set the screenshot interval and choose between PNG and JPEG formats.
- **Organized Storage:** Saves screenshots in a dedicated `Screenshots` directory relative to the script.

## Requirements

- **Operating System:** macOS
- **Python Version:** Python 3.6 or higher
- **Python Libraries:**
    - `Pillow`

## Usage

Run the script with the following command:
```sh
python Scripts/unity_screenshot_automation.py [--interval INTERVAL] [--format FORMAT]
```

### Command-Line Arguments

- `--interval`:
    - **Type:** int
    - **Default:** 5
    - **Description:** Sets the interval between screenshots in seconds.

- `--format`:
    - **Type:** str
    - **Choices:** PNG, JPEG
    - **Default:** PNG
    - **Description:** Chooses the image format for the screenshots.

### Examples

- Set the interval to 10 seconds:
    ```sh
    python Scripts/unity_screenshot_automation.py --interval 10
    ```

- Set the format to JPEG:
    ```sh
    python Scripts/unity_screenshot_automation.py --format JPEG
    ```

- Set the interval to 15 seconds and format to PNG:
    ```sh
    python Scripts/unity_screenshot_automation.py --interval 15 --format PNG
    ```