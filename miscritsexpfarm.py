import pyautogui
import time
import pygame  # Using pygame for sound looping
import tkinter as tk
import keyboard

# Initialize pygame for sound handling
pygame.init()

# Image paths for detecting the battle screen, Close button, and multiple Search areas
BATTLE_SCREEN_IMAGES = ['battleS.png', 'battle10.png', 'battle.png', 'fight.png', 'battle (3).png']  # List of battle screen images
CLOSE_BUTTON_IMAGE = 'close.png'
SEARCH_AREAS = ['zapzap.png', 'lzap2.png', 'lzap.png', 'lzap2.png']
WIN_SCREEN_IMAGE = 'win (2).png'
READY_TO_TRAIN_IMAGE = 'readytotrain.png'
TARGET_MISCRIT_IMAGE = 'lightzap2.png'

# Fixed coordinates for buttons (replace with actual coordinates)
ATTACK_BUTTON_COORDS = (643, 947)
CLOSE_BUTTON_COORDS = (902, 816)
TRAIN_BUTTON_COORDS = (563, 78)
MISCRIT_TO_TRAIN_COORDS = (606, 307)
TRAIN_NOW_BUTTON_COORDS = (938, 194)
CONTINUE_BUTTON_COORDS = (1074, 900)
CONTINUE_BUTTON_COORDS2 = (895, 663)
CLOSE_TRAIN_BUTTON_COORDS = (1332, 158)

running = False

def search_for_miscrit():
    """Step 1: Clicks on one of the available locations to search for Miscrits."""
    print("Searching for a Miscrit...")
    for search_area in SEARCH_AREAS:
        print(f"Attempting to locate search area: {search_area}")
        try:
            search_area_location = pyautogui.locateOnScreen(search_area, confidence=0.8)
            if search_area_location:
                print(f"Search area found: {search_area}. Clicking to search for Miscrit...")
                search_area_center = pyautogui.center(search_area_location)
                pyautogui.click(search_area_center)
                time.sleep(2)
                pyautogui.screenshot(f'search_for_miscrit_{search_area}.png')
                return True
            else:
                print(f"Search area not found: {search_area}")
        except pyautogui.ImageNotFoundException:
            print(f"Error: {search_area} not found on screen.")
            pyautogui.screenshot('search_error.png')
    return False

def is_battle_found():
    """Step 2: Checks if any of the battle screen images are detected."""
    print("Checking for battle screen...")
    try:
        region = (0, 0, 1920, 1080)
        for battle_image in BATTLE_SCREEN_IMAGES:
            print(f"Trying to locate battle screen image: {battle_image}")
            battle_screen_location = pyautogui.locateOnScreen(battle_image, confidence=0.8, region=region)
            if battle_screen_location:
                print(f"Battle screen detected using image: {battle_image}")
                return True
        # Only print this after trying all images
        print("Battle screen not found.")
        return False
    except pyautogui.ImageNotFoundException:
        print("Error: Battle screen not found.")
        pyautogui.screenshot('battle_screen_check_error.png')
        return False

def locate_win_screen():
    """Locate the win screen after the battle."""
    print("Checking for win screen...")
    try:
        win_screen_location = pyautogui.locateOnScreen(WIN_SCREEN_IMAGE, confidence=0.9)
        if win_screen_location:
            print("Win screen detected!")
            return True
        else:
            print("Win screen not found.")
            return False
    except pyautogui.ImageNotFoundException:
        print("Error: Win screen not found.")
        pyautogui.screenshot('win_screen_check_error.png')
        return False

def detect_ready_to_train():
    """Detect if there is a Miscrit ready to train."""
    print("Checking for ready-to-train Miscrit...")
    try:
        ready_to_train_location = pyautogui.locateOnScreen(READY_TO_TRAIN_IMAGE, confidence=0.8)
        if ready_to_train_location:
            print("Ready to train Miscrit detected!")
            return True
        return False
    except pyautogui.ImageNotFoundException:
        print("Error: Ready to train Miscrit not found.")
        return False

def show_alert():
    """Display an alert window with an 'Okay' button to stop the alarm."""
    # Load and play the sound in an infinite loop
    pygame.mixer.music.load('alarm.mp3')
    pygame.mixer.music.play(-1)  # -1 for infinite loop

    alert = tk.Tk()
    alert.title("Target Miscrit Detected!")
    alert.geometry("300x100")
    alert.attributes("-topmost", True)  # Keep the window on top

    label = tk.Label(alert, text="Target Miscrit detected! Click OK to stop the alarm.")
    label.pack(pady=10)
    
    def stop_alarm():
        pygame.mixer.music.stop()  # Stop the alarm sound
        alert.destroy()            # Close the alert window

    button = tk.Button(alert, text="Okay", command=stop_alarm)
    button.pack(pady=10)
    alert.mainloop()

def detect_target_miscrit():
    """Check if the target Miscrit appears on screen and show alert if found."""
    print("Checking for target Miscrit...")
    try:
        target_location = pyautogui.locateOnScreen(TARGET_MISCRIT_IMAGE, confidence=0.8)
        if target_location:
            print("Target Miscrit detected! Showing alert.")
            show_alert()
            return True
        return False
    except pyautogui.ImageNotFoundException:
        print("Error: Target Miscrit not found.")
        return False

def detect_evolved_text():
    """Detect if the 'evolved' text is visible on the screen."""
    print("Checking for 'evolved' text...")
    try:
        evolved_location = pyautogui.locateOnScreen('evolved.png', confidence=0.8)
        if evolved_location:
            print("'Evolved' text detected!")
            return True
        return False
    except pyautogui.ImageNotFoundException:
        print("Error: 'Evolved' text not found.")
        return False

def fight_miscrit():
    """Step 3: Engages in the fight by clicking the Attack button until the battle ends."""
    print("Entering battle loop...")
    while is_battle_found():
        print("Battle detected! Attacking Miscrit...")
        while not locate_win_screen():
            if detect_target_miscrit():
                print("Pausing attack due to target Miscrit.")
                time.sleep(5)
                continue
            print("Clicking Attack button...")
            pyautogui.click(ATTACK_BUTTON_COORDS)
            print(f"Clicked on Attack button at {ATTACK_BUTTON_COORDS}")
            time.sleep(1)
        print("Win screen detected!")
        time.sleep(2)
        pyautogui.click(CLOSE_BUTTON_COORDS)
        if detect_ready_to_train():
            pyautogui.click(CLOSE_BUTTON_COORDS)
            handle_training()

        print("Returning to search for next encounter...")
        break

def handle_training():
    """Handles the training sequence for the Miscrit."""
    print("Starting the training sequence...")
    time.sleep(1)
    pyautogui.click(TRAIN_BUTTON_COORDS)
    time.sleep(1)
    pyautogui.click(MISCRIT_TO_TRAIN_COORDS)
    time.sleep(1)
    pyautogui.click(TRAIN_NOW_BUTTON_COORDS)
    time.sleep(1)
    pyautogui.click(CONTINUE_BUTTON_COORDS2)
    time.sleep(1)
    pyautogui.click(CONTINUE_BUTTON_COORDS)
    time.sleep(1)
    pyautogui.click(CONTINUE_BUTTON_COORDS2)
    time.sleep(1)
    if detect_evolved_text():
        pyautogui.click((898, 824))
        time.sleep(1)
        pyautogui.click((898, 764))
    pyautogui.click(CLOSE_TRAIN_BUTTON_COORDS)
    time.sleep(1)

    # Click the Close Train button
    pyautogui.click(CLOSE_TRAIN_BUTTON_COORDS)
    time.sleep(1)

def toggle_running_state():
    """Toggle the running state of the script based on Enter key press."""
    global running
    running = not running
    if running:
        print("Script started. Press Enter again to stop.")
    else:
        print("Script stopped. Press Enter to start again.")

def main_loop():
    """Main loop that runs while the script is in the running state."""
    global running
    while True:
        # Check if the script should stop running
        if not running:
            continue

        try:
            if search_for_miscrit():
                print("Miscrit found! Entering battle...")
                fight_miscrit()
            
            if is_battle_found():
                print("Battle detected! Fighting...")
                fight_miscrit()

            else:
                print("No available search areas or no battle detected. Waiting...")
                time.sleep(1)
            print("Returning to search for next encounter...")
            time.sleep(1)
        except KeyboardInterrupt:
            print("Script stopped by user.")
            break

# Bind the Enter key to toggle the running state and Backspace to exit the program
keyboard.add_hotkey('enter', toggle_running_state)
keyboard.add_hotkey('backspace', lambda: exit(0))  # Exit the program on Backspace

# Start listening for key events
print("Press Enter to start or stop the script. Press Backspace to exit.")
main_loop()