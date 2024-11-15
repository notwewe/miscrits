import pyautogui
import time
import pygame  # Using pygame for sound looping
import tkinter as tk
import keyboard
from PIL import Image, ImageDraw
import random
import pytesseract
import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize pygame for sound handling
pygame.init()

# Image paths for detecting the battle screen, Close button, and multiple Search areas
CLOSE_BUTTON_IMAGE = 'close.png'
SEARCH_AREAS = ['foilw.png']
WIN_SCREEN_IMAGE = 'win (2).png'
READY_TO_TRAIN_IMAGE = 'readytotrain.png'
#TARGET_MISCRIT_IMAGE = 'lightzap2.png'
MISCRIT_IMAGE = 'battle10.png'  # Path to the image of the Miscrit you're looking for
search_drops = ["gold.png", "potion.png", "potion2.png"]

# Fixed coordinates for buttons (replace with actual coordinates)
ATTACK_BUTTON_COORDS = (643, 947)
CLOSE_BUTTON_COORDS = (902, 816)
TRAIN_BUTTON_COORDS = (563, 78)
MISCRIT_TO_TRAIN_COORDS = (606, 307)
TRAIN_NOW_BUTTON_COORDS = (938, 194)
CONTINUE_BUTTON_COORDS = (1074, 900)
CONTINUE_BUTTON_COORDS2 = (895, 663)
CLOSE_TRAIN_BUTTON_COORDS = (1332, 158)

SEARCH_REGION = (491, 316, 514 - 491, 338 - 316)

running = False

SEARCH_DROP_REGION = (795, 350, 272, 211)  

def check_and_click_search_drop():
    """Check if any search drop is visible in the defined region and click it."""
    print("Checking for search drops in the main region...")
    time.sleep(2)
    for drop_image in search_drops:
        try:
            drop_location = pyautogui.locateOnScreen(drop_image, region=SEARCH_DROP_REGION, confidence=0.7)
            if drop_location:
                print(f"Search drop found: {drop_image}. Clicking...")
                pyautogui.click(pyautogui.center(drop_location))
                time.sleep(2)  # Wait for actions triggered by the click
                return True  # If a search drop is found and clicked, return True
        except pyautogui.ImageNotFoundException:
            print(f"Error: {drop_image} not found on screen.")
    print("No search drops found in the main region.")
    return False  # Return False if no drops are detected
def clear_area_for_visibility():
    print("Clearing the area for visibility...")
    # Click to clear the area (adjust coordinates as necessary)
    pyautogui.click(1040, 540)  
    time.sleep(1.5)  # Wait for area to be cleared

def search_for_miscrit():
    """Step 1: Clicks to clear the area and then searches for Miscrits."""
    print("Searching for a Miscrit...")
    for search_area in SEARCH_AREAS:
        print(f"Attempting to locate search area: {search_area}")
        try:
            search_area_location = pyautogui.locateOnScreen(search_area, confidence=0.8)
            if search_area_location:
                print(f"Search area found: {search_area}. Clicking to search for Miscrit...")
                search_area_center = pyautogui.center(search_area_location)
                pyautogui.click(search_area_center)
                time.sleep(4)  # Wait to ensure the search starts

                # Now check if the Miscrit is found
                if is_miscrit_found():
                    print("Miscrit found! Entering battle...")
                    area_cleared = False  # Reset area cleared flag for the next cycle
                    return True  # Proceed to battle if Miscrit is found
                else:
                    print("Miscrit not found in the search area. Trying next area...")

            else:
                print(f"Search area not found: {search_area}")
        except pyautogui.ImageNotFoundException:
            print(f"Error: {search_area} not found on screen.")
            pyautogui.screenshot('search_error.png')  # Capture an error screenshot for debugging
            continue  # Skip the missing area and move to the next one

    return False  # If no Miscrit was found in any search area, return False

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

from PIL import ImageOps
import concurrent.futures

def preprocess_image_for_ocr(image):
    """Preprocess the image for OCR to enhance text detection."""
    grayscale_image = image.convert('L')  # Convert image to grayscale
    enhanced_image = ImageOps.autocontrast(grayscale_image)  # Enhance contrast
    return enhanced_image

def detect_target_miscrit(target_texts=["Foil Vhisp"]):
    """Detect if any of the target Miscrit texts appear on screen and show alert if found."""
    print("Checking for target Miscrit texts...")

    def ocr_task():
        try:

            search_region = (1219, 71, 109, 26)  # Width = 1328 - 1219, Height = 97 - 71

            screenshot = pyautogui.screenshot(region=search_region)  # Capture region
            screenshot = preprocess_image_for_ocr(screenshot)  # Preprocess image
            text_in_region = pytesseract.image_to_string(screenshot)  # OCR text detection
            return text_in_region
        except Exception as e:
            print(f"Error in OCR: {e}")
            return ""

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(ocr_task)  # Run OCR in a separate thread
        text_in_region = future.result()  # Get OCR result

    # Check if any of the target texts with first letter capitalized are in the detected text
    for target_text in target_texts:
        if target_text in text_in_region:
            print(f"Target Miscrit '{target_text}' detected! Showing alert.")
            show_alert()  # Trigger alert if Miscrit detected
            return True  # Return True when any of the target Miscrits are found

    print("None of the target Miscrit texts were found.")
    return False

def detect_evolved_text():
    """Detect if the 'evolved' text is visible on the screen."""
    print("Checking for 'evolved' text...")
    time.sleep(2)
    try:
        evolved_location = pyautogui.locateOnScreen('evolved.png', confidence=0.8)
        if evolved_location:
            print("'Evolved' text detected!")
            return True
        return False
    except pyautogui.ImageNotFoundException:
        print("Error: 'Evolved' text not found.")
        return False

MAX_BATTLE_TIME = 180  # Maximum battle time in seconds (3 minutes)

def is_miscrit_found():
    """Check if the Miscrit image is on the screen."""
    pyautogui.screenshot('debug_before_fight.png')  # Capture a screenshot right before checking for the Miscrit
    miscrit_location = pyautogui.locateOnScreen(MISCRIT_IMAGE, confidence=0.7)
    return miscrit_location is not None

def fight_miscrit():
    """Step 3: Engages in the fight by clicking the Attack button until the battle ends."""
    print("Entering battle loop...")
    battle_ended = False  # Flag to track if the battle has ended
    start_time = time.time()  # Start time of the battle

    # Verify Miscrit presence before starting the battle loop
    if not is_miscrit_found():
        print("Error: Miscrit not found, skipping battle.")
        return  # Exit function if Miscrit is not found

    while not battle_ended:  # Continue loop until battle ends
        # If target Miscrit is detected, pause the attack
        if detect_target_miscrit():
            print("Target Miscrit detected! Pausing attack.")
            # Allow manual interaction after detecting the target Miscrit
            time.sleep(5)  # You can adjust the sleep time to suit your needs
            continue  # Continue to the next attack phase

        print("Clicking Attack button...")
        pyautogui.click(ATTACK_BUTTON_COORDS)
        time.sleep(3)
        print(f"Clicked on Attack button at {ATTACK_BUTTON_COORDS}")

        # Check for win screen after attacking
        if locate_win_screen():
            print("Win screen detected!")
            time.sleep(2.5)
            if detect_ready_to_train():  # Check if 'Ready to Train' screen is visible
                pyautogui.click(CLOSE_BUTTON_COORDS)  # Close win screen
                print("Ready to Train detected. Proceeding to training...")
                handle_training()  # Proceed to training
            else:
                print("No Ready to Train detected. Closing win screen.")
                pyautogui.click(CLOSE_BUTTON_COORDS)  # Close win screen
            battle_ended = True  # Mark the battle as ended
            break  # Exit battle loop

        # Optional: Check for other failure conditions like timeout
        if time.time() - start_time > MAX_BATTLE_TIME:  # Add max battle time if necessary
            print("Max battle time reached, ending battle.")
            battle_ended = True
            break

    print("Returning to search for next encounter...")

def detect_S():
    """Detects 'S' Miscrit within the selected screen region."""
    try:
        s_image_location = pyautogui.locateOnScreen('S.png', region=SEARCH_REGION, confidence=0.7)
        if s_image_location:
            print("S Miscrit found!")
            return True
        else:
            print("S Miscrit not found.")
            return False
    except Exception as e:
        print(f"Error detecting S Miscrit: {e}")
        return False

def detect_S_plus():
    """Detects 'S+' Miscrit within the selected screen region."""
    try:
        s_plus_image_location = pyautogui.locateOnScreen('S+.png', region=SEARCH_REGION, confidence=0.7)
        if s_plus_image_location:
            return True
        else:
            print("S+ Miscrit not found.")
            return False
    except Exception as e:
        print(f"Error detecting S+ Miscrit: {e}")
        return False

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

    if detect_S() or detect_S_plus():
        pyautogui.click((780, 901))  # Plat train button
        print("Plat train clicked for 'S' or 'S+' Miscrit.")
        time.sleep(1)
        pyautogui.click(CONTINUE_BUTTON_COORDS)
        time.sleep(1)
        pyautogui.click(CONTINUE_BUTTON_COORDS2)
        time.sleep(1)

        # Wait for animation to complete before checking for evolved text
        print("Waiting for evolution animation to complete...")
        time.sleep(2)  # Increased delay to 2 seconds for evolution animation

        # Check for evolved text after plat training
        evolved_detected = False
        for attempt in range(3):  # Increased retries to 3
            if detect_evolved_text():
                evolved_detected = True
                print("Evolved text detected on attempt", attempt + 1)
                pyautogui.click((898, 824))  # Click evolved Miscrit
                time.sleep(1)
                pyautogui.click((898, 764))  # Confirm evolution
                time.sleep(1)
                break
            else:
                print(f"Attempt {attempt + 1}: Evolved text not detected. Retrying...")
                time.sleep(1)  # Delay before retrying

        if not evolved_detected:
            print("Evolved text not detected after retries. Proceeding without evolution action.")
    else:
        # Skip plat train actions if it's not an 'S' or 'S+' Miscrit
        pyautogui.click(CONTINUE_BUTTON_COORDS)
        time.sleep(1)
        pyautogui.click(CONTINUE_BUTTON_COORDS2)
        time.sleep(1)

    # Close the training window
    print("Closing the training window...")
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
def highlight_search_region():

    #search_region = (1219, 71, 109, 26)  # Width = 1328 - 1219, Height = 97 - 71
    search_region = SEARCH_DROP_REGION
    """Highlight the search region in red to indicate the search area."""
    screenshot = pyautogui.screenshot()  # This is already a PIL Image object
    draw = ImageDraw.Draw(screenshot)
    
    # Draw a red rectangle around the search region
    x, y, width, height = search_region
    draw.rectangle([x, y, x + width, y + height], outline="red", width=3)
    
    # Display the highlighted search region (optional)
    screenshot.show()  # Shows the image for debugging purposes

    # If you want to save the highlighted image for later reference
    screenshot.save('highlighted_search_region.png')

def main_loop():
    """Main loop that runs while the script is in the running state."""
    global running
    search_timeout = 30  # Max time (seconds) to search for Miscrits before retrying
    while True:
        if not running:
            continue

        try:
            start_time = time.time()  # Start time for the search

            while time.time() - start_time < search_timeout:  # Limit search time
                if check_and_click_search_drop():
                    print("Search drop clicked. Continuing...")
                    continue  # Proceed to the next step after handling a drop

                #highlight_search_region()
                clear_area_for_visibility()

                if search_for_miscrit():
                    print("Miscrit found! Entering battle...")
                    fight_miscrit()  # Proceed with battle if found
                    break
                else:
                    print("No Miscrit found, retrying search...")
                    #time.sleep(1)

            else:
                print(f"Timeout reached while searching for Miscrit. Retrying...")
            print("Returning to search for next encounter...")
            #time.sleep(1)

        except KeyboardInterrupt:
            print("Script stopped by user.")
            break

# Bind the Enter key to toggle the running state and Backspace to exit the program
keyboard.add_hotkey('enter', toggle_running_state)
keyboard.add_hotkey('backspace', lambda: exit(0))  # Exit the program on Backspace

# Start listening for key events
print("Press Enter to start or stop the script. Press Backspace to exit.")
main_loop()