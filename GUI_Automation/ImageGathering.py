#! python 3
import pyautogui, os, sys, time

print('Press Ctrl-C to quit.')

width, height = pyautogui.size()

# TODO: Find images that are needed

lop = []

for file_path in lop:
    if os.path.exists(file_path) is True:
        continue
    else:
        print(f'File Path {file_path} Provided is Not Valid')
        sys.exit()

current_mouse = pyautogui.position()

# Start Timelapse with AmScope Open

capture_button = pyautogui.locateOnScreen('image.png')

if capture_button is None:
    print('Capture_button not found')
    sys.exit()

pyautogui.click(capture_button, button='left')  # Fix for pixels

start_time_lapse_button = pyautogui.locateOnScreen('image.png')

if start_time_lapse_button is None:
    print('start_time_lapse_button not found')
    sys.exit()

pyautogui.click(start_time_lapse_button, button='left')

ok_button = pyautogui.locateOnScreen('image.png')

if ok_button is None:
    print('ok_button not found')
    sys.exit()
