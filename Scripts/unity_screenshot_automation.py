import os
import time
import argparse
import subprocess
from datetime import datetime
from PIL import ImageGrab

# ---------------------- Configuration ----------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(SCRIPT_DIR, "Screenshots")
APP_NAME = "Unity"

def parse_arguments():
    parser = argparse.ArgumentParser(description='Unity Screenshot Automation Tool')
    parser.add_argument('--interval',
                        type=int,
                        default=5,
                        help='Screenshot interval in seconds (default: 5)')
    parser.add_argument('--format',
                        type=str,
                        default='JPEG',
                        choices=['PNG', 'JPEG'],
                        help='Screenshot image format (default: PNG)')
    return parser.parse_args()

def get_frontmost_app():
    script = '''
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
    end tell
    return frontApp
    '''
    args = ['osascript', '-e', script]
    try:
        output = subprocess.check_output(args)
        front_app = output.decode('utf-8').strip()
        return front_app
    except Exception as e:
        print(f"Error getting frontmost application: {e}")
        return None

def get_window_bounds(app_name):
    script = f'''
    tell application "System Events"
        try
            set app_process to first process whose name is "{app_name}"
            tell app_process
                set the_window to front window
                set win_position to position of the_window
                set win_size to size of the_window
                set x to item 1 of win_position
                set y to item 2 of win_position
                set w to item 1 of win_size
                set h to item 2 of win_size
                return (x as string) & "," & (y as string) & "," & (w as string) & "," & (h as string)
            end tell
        on error
            return "ERROR"
        end try
    end tell
    '''
    args = ['osascript', '-e', script]
    try:
        output = subprocess.check_output(args)
        output = output.decode('utf-8').strip()
        if output == "ERROR":
            return None
        else:
            x_str, y_str, w_str, h_str = output.split(',')
            x = int(float(x_str))
            y = int(float(y_str))
            w = int(float(w_str))
            h = int(float(h_str))
            # Return bounding box as (left, top, right, bottom)
            return (x, y, x + w, y + h)
    except Exception as e:
        print(f"Error getting window bounds: {e}")
        return None

def take_screenshot(image_format):
    front_app = get_frontmost_app()
    if front_app != APP_NAME:
        print(f"{APP_NAME} is not the frontmost application. Skipping screenshot.")
        return False
    bounds = get_window_bounds(APP_NAME)
    if bounds:
        try:
            # Capture screenshot of specified region
            screenshot = ImageGrab.grab(bbox=bounds)
            # Create screenshots directory
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if image_format == 'JPEG':
                filename = os.path.join(SCREENSHOT_DIR, f'unity_screenshot_{timestamp}.jpg')
                # Convert RGBA to RGB if needed
                if screenshot.mode == 'RGBA':
                    screenshot = screenshot.convert('RGB')
                # Save screenshot
                screenshot.save(filename, 'JPEG', quality=90)
            else:
                filename = os.path.join(SCREENSHOT_DIR, f'unity_screenshot_{timestamp}.png')
                # Save screenshot as PNG
                screenshot.save(filename, 'PNG')
            print(f"Screenshot saved: {filename}")
            return True
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return False
    else:
        print(f"{APP_NAME} window not found. Skipping screenshot.")
        return False

def main():
    args = parse_arguments()
    print(f"Screenshot interval set to {args.interval} seconds")
    print(f"Screenshots will be saved to: {SCREENSHOT_DIR}")
    print(f"Image format set to: {args.format}")

    try:
        while True:
            take_screenshot(args.format)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nScreenshot automation stopped")

if __name__ == "__main__":
    main()