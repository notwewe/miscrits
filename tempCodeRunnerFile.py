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
            print("S+ Miscrit found!")
            return True
        else:
            print("S+ Miscrit not found.")
            return False
    except Exception as e:
        print(f"Error detecting S+ Miscrit: {e}")
        return False