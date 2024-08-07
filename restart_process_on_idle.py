import psutil
import subprocess
import time
import ctypes
import os
import logging
from logging.handlers import RotatingFileHandler


# Set the restart settings
PROCESS_NAME = "NZXT CAM.exe"  # The process to be killed
EXECUTABLE_PATH = r"C:\Program Files\NZXT CAM\NZXT CAM.exe"  # The executable to be ran
IDLE_THRESHOLD = 2 * 3600  # Time in seconds to idle before restarting

# Set the logging settings
log_folder = os.path.join(os.path.expanduser("~"), "Documents", "restart_process_on_idle_logs")
log_file_path = os.path.join(log_folder, "restart_process_on_idle.log")
logging_level = logging.DEBUG


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]


def get_idle_duration():
    # Returns idle time in seconds
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0
    else:
        return 0


def kill_process_by_name(PROCESS_NAME):
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == PROCESS_NAME:
            proc.kill()


def start_process_hidden(EXECUTABLE_PATH):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0  # SW_HIDE
    subprocess.Popen(EXECUTABLE_PATH, startupinfo=startupinfo)


def main():
    # Ensure the directory exists
    log_directory = os.path.dirname(log_file_path)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Configure logging with RotatingFileHandler
    handler = RotatingFileHandler(
        log_file_path,
        maxBytes=100 * 1024,  # 100 KB
        backupCount=2,  # Number of backup files
    )

    # Configure logging
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[handler],
    )

    logging.critical("--- Starting script ---")
    logging.debug(f"IDLE_THRESHOLD={round(IDLE_THRESHOLD/3600, 2)} hours")

    first_run = True

    while True:
        idle_time = get_idle_duration()
        logging.debug(f"idle_time={round(idle_time/3600, 2)} hours")

        # Reset NZXT CAM only while idle
        if idle_time >= IDLE_THRESHOLD or first_run:
            if first_run:
                logging.info(f"first_run={first_run}")
                first_run = False
            else:
                logging.info(f"Idle threshold reached: {idle_time}/{IDLE_THRESHOLD}")

            # Kill the process if it is running
            logging.debug("Killing {PROCESS_NAME}...")
            kill_process_by_name(PROCESS_NAME)

            logging.debug("{PROCESS_NAME} was killed, sleeping for 10 seconds...")
            time.sleep(10)

            # Start the process
            logging.debug(f"Starting '{EXECUTABLE_PATH}'...")
            start_process_hidden(EXECUTABLE_PATH)

            # Wait some time before allowing another reset
            logging.info(f"{PROCESS_NAME} restarted. Sleeping {round(IDLE_THRESHOLD/3600, 2)} hours")
            time.sleep(IDLE_THRESHOLD)
        else:
            # Check idle time again in 10 minutes
            time.sleep(600)


if __name__ == "__main__":
    main()
