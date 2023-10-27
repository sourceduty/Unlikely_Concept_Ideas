# Limit your Steam gaming time.

import psutil
import time
import os

def is_steam_running():
    """Check if Steam is running."""
    for process in psutil.process_iter():
        try:
            if "steam" in process.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def send_notification(message):
    """Send a notification to the user."""
    # This uses the 'notify-send' command available on Linux. 
    # For Windows, you might want to use a library like 'plyer' for notifications.
    os.system(f'notify-send "{message}"')

def get_user_input():
    """Get user input for maximum play time and grace period."""
    try:
        max_play_time = int(input("Enter the maximum play time in minutes: ")) * 60  # Convert to seconds
        grace_period = int(input("Enter the grace period in minutes after reaching the maximum play time: ")) * 60  # Convert to seconds
        return max_play_time, grace_period
    except ValueError:
        print("Please enter a valid number.")
        return get_user_input()

def main():
    MAX_PLAY_TIME, GRACE_PERIOD = get_user_input()

    total_play_time = 0

    while True:
        if is_steam_running():
            total_play_time += 1
            if total_play_time == MAX_PLAY_TIME:
                send_notification(f"You've been playing for {MAX_PLAY_TIME//60} minutes. Time to take a break!")
            elif total_play_time > MAX_PLAY_TIME + GRACE_PERIOD:
                for process in psutil.process_iter():
                    try:
                        if "steam" in process.name().lower():
                            process.terminate()
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
                total_play_time = 0  # Reset the timer
        else:
            total_play_time = 0  # Reset the timer if Steam is not running

        time.sleep(1)  # Check every second

if __name__ == "__main__":
    main()
