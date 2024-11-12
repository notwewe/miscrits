import pyautogui
import time
from playsound import playsound

# Image paths for detecting the battle screen, Close button, and multiple Search areas
BATTLE_SCREEN_IMAGE = 'battle.png'
CLOSE_BUTTON_IMAGE = 'close.png'
SEARCH_AREAS = ['search1.png', 'search2.png', 'search3.png', 'search4.png', 'search5.png', 'search6.png', 'search7.png']  # List of different search areas
WIN_SCREEN_IMAGE = 'win.png'  # New image for detecting the win screen

# Image for the target Miscrit to avoid
TARGET_MISCRIT_IMAGE = 'target.png'  # Image of the Miscrit you want to avoid

# Define fixed coordinates for the Attack button (replace with actual coordinates)
ATTACK_BUTTON_COORDS = (844, 957)  # Example coordinates for the Attack button

# Define the coordinates for the close button (updated to (902, 816))
CLOSE_BUTTON_COORDS = (902, 816)  # Replace with actual x, y coordinates of the "close" button

def search_for_miscrit():
    """Step 1: Clicks on one of the available locations to search for Miscrits."""
    print("Searching for a Miscrit...")

    for search_area in SEARCH_AREAS:
        print(f"Attempting to locate search area: {search_area}")

        try:
            # Locate the search area on the screen with increased confidence
            search_area_location = pyautogui.locateOnScreen(search_area, confidence=0.8)

            if search_area_location:
                print(f"Search area found: {search_area}. Clicking to search for Miscrit...")
                search_area_center = pyautogui.center(search_area_location)  # Get the center coordinates of the found area
                pyautogui.click(search_area_center)  # Click the center of the search area
                time.sleep(2)  # Wait briefly for any encounter to load
                pyautogui.screenshot(f'search_for_miscrit_{search_area}.png')  # Capture screen after clicking
                return True  # If we found a valid search area and clicked, return True
            else:
                print(f"Search area not found: {search_area}")

        except pyautogui.ImageNotFoundException:
            print(f"Error: {search_area} not found on screen.")
            # Optionally, you can take a screenshot here to debug
            pyautogui.screenshot('search_error.png')  # Capture screen for debugging

    return False  # If no search area was found

def is_battle_found():
    """Step 2: Checks if the battle screen is detected."""
    print("Checking for battle screen...")

    # Capture screen before checking for battle to help with debugging
    pyautogui.screenshot('before_battle_check.png')

    try:
        # Locate the battle screen on the screen with increased confidence and search area limited to a region
        region=(0, 0, 1920, 1080)  # Adjust this region based on where the battle screen appears
        battle_screen_location = pyautogui.locateOnScreen(BATTLE_SCREEN_IMAGE, confidence=0.8, region=region)

        if battle_screen_location:
            print("Battle screen detected!")
            return True
        else:
            print("Battle screen not found.")
            return False
    except pyautogui.ImageNotFoundException:
        print("Error: Battle screen not found.")
        pyautogui.screenshot('battle_screen_check_error.png')  # Capture screen for debugging
        return False

def locate_win_screen():
    """Locate the win screen after the battle."""
    print("Checking for win screen...")
    try:
        # Increase confidence to make detection more lenient
        win_screen_location = pyautogui.locateOnScreen(WIN_SCREEN_IMAGE, confidence=0.9)  # Increase confidence if needed
        if win_screen_location:
            print("Win screen detected!")
            return True
        else:
            print("Win screen not found.")
            return False
    except pyautogui.ImageNotFoundException:
        print("Error: Win screen not found.")
        pyautogui.screenshot('win_screen_check_error.png')  # Capture screen for debugging
        return False

def detect_target_miscrit():
    """Check if the target Miscrit appears on screen."""
    print("Checking for target Miscrit...")

    try:
        # Locate the target Miscrit image on the screen with increased confidence
        target_location = pyautogui.locateOnScreen(TARGET_MISCRIT_IMAGE, confidence=0.8)

        if target_location:
            print("Target Miscrit detected! Alarm triggered.")
            # Play the sound and show the alert at the same time
            playsound('alarm.mp3')
            return True
        else:
            return False
    except pyautogui.ImageNotFoundException:
        print("Error: Target Miscrit not found.")
        return False


def fight_miscrit():
    """Step 3: Engages in the fight by clicking the Attack button until the battle ends."""
    print("Entering battle loop...")
    while True:
        # Step 1: Detect the battle screen (this can be a check before the attack)
        if is_battle_found():
            print("Battle detected! Attacking Miscrit...")

            # Step 2: Keep clicking the Attack button until win screen is found
            while not locate_win_screen():
                # Check if the target Miscrit is on screen
                if detect_target_miscrit():
                    # If the target Miscrit is detected, stop the attack and raise the alarm
                    print("Pausing attack due to target Miscrit.")
                    time.sleep(5)  # Pause for a while before checking again
                    continue  # Continue the loop to check for target Miscrit and pause if needed

                print("Clicking Attack button...")
                pyautogui.click(ATTACK_BUTTON_COORDS)  # Click the fixed coordinates of the Attack button
                print(f"Clicked on Attack button at {ATTACK_BUTTON_COORDS}")
                
                # Small delay to allow attack animation to complete
                time.sleep(1)
            
            # Once the win screen is detected, exit the loop
            print("Win screen detected! Closing win screen...")
            pyautogui.click(CLOSE_BUTTON_COORDS)  # Click the close button to end the win screen
            time.sleep(2)  # Wait briefly before returning to search for next Miscrit
            break  # Exit the battle loop to restart the search for a Miscrit
        else:
            # No battle detected, break out or wait
            print("No battle detected. Waiting for next encounter...")
            time.sleep(5)  # Wait before checking for the next battle

def main():
    try:
        while True:
            # Step 1: Click to search for a Miscrit
            if search_for_miscrit():
                # Step 2: Check if a battle has been found
                if is_battle_found():
                    print("Battle detected! Entering battle...")

                    # Step 3: Fight the Miscrit
                    fight_miscrit()

                    # Step 4: After closing the win screen, return to searching for Miscrits
                else:
                    # If no battle found after search
                    print("No Miscrit found after search. Waiting for cooldown...")
                    time.sleep(1)  # Cooldown time before re-clicking to search again
            else:
                print("No available search areas found. Waiting for cooldown...")
                time.sleep(1)  # Cooldown time if no valid search area found

            # Step 5: Repeat the process
            print("Returning to search for next encounter...")
            time.sleep(2)  # Small delay before repeating the search

    except KeyboardInterrupt:
        print("Script stopped by user.")

if __name__ == "__main__":
    main()
