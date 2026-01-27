import pyautogui
import time

# --- Configuration ---
# The folder containing your videos
VIDEO_FOLDER = r"D:\1"
# How long the script should wait before closing VLC (in seconds)
TOTAL_PLAYBACK_TIME = 10 

def automate_vlc_foolproof():
    # Fail-safe: Slam mouse to top-left to stop
    pyautogui.FAILSAFE = True
    # Pause slightly between all actions for stability
    pyautogui.PAUSE = 1.0

    try:
        print("Step 1: Opening Windows Run Dialog...")
        pyautogui.hotkey('win', 'r')
        time.sleep(4)

        # Step 2: Write the command to launch VLC with the folder as an argument
        # The quotes around the path are vital in case there are spaces
        launch_command = f'vlc "{VIDEO_FOLDER}"'
        print(f"Step 2: Sending command: {launch_command}")
        pyautogui.write(launch_command)
        time.sleep(3)
        pyautogui.press('enter')
        time.sleep(5)

        # Step 3: Wait for VLC to launch and load the folder
        print("Step 3: Waiting for VLC to load the playlist...")
        time.sleep(5)

        # Step 4: Optional - Ensure it is in Fullscreen
        # 'f' is the VLC shortcut for fullscreen
        print("Step 4: Setting Fullscreen...")
        pyautogui.press('f')

        # Step 5: Wait for the duration of the videos
        print(f"Step 5: Playback started. Waiting {TOTAL_PLAYBACK_TIME} seconds...")
        # We use a loop here so we can see the countdown in the terminal
        for i in range(TOTAL_PLAYBACK_TIME, 0, -10):
            print(f"Time remaining: {i} seconds...")
            time.sleep(10)

        # Step 6: Close VLC
        print("Step 6: Closing VLC Player...")
        pyautogui.hotkey('alt', 'f4')
        print("Automation Complete.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("--- STARTING FOOLPROOF AUTOMATION ---")
    print("Ensure VLC is closed before starting.")
    time.sleep(3)
    automate_vlc_foolproof()