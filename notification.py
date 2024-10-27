import subprocess
import os

# Function to run terminal command
def run_terminal_command(text, title):
    # Set environment variables and open the Automator app
    env = os.environ.copy()
    env["NOTIFICATION_TEXT"] = text
    env["NOTIFICATION_TITLE"] = title
    
    # Open the Automator application with the updated environment
    subprocess.run(["open", "-a", "AddedToPlaylist"], env=env)