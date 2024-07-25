import psutil
import subprocess
import time
import ctypes
import os
import logging
from logging.handlers import RotatingFileHandler


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


def kill_process_by_name(process_name):
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == process_name:
            proc.kill()


def start_process_hidden(executable_path):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0  # SW_HIDE

    subprocess.Popen(executable_path, startupinfo=startupinfo)


def main():
    # Get the path to the current user's Documents folder
    documents_folder = os.path.join(
        os.path.expanduser("~"), "Documents", "restart_nzxt_cam_on_idle"
    )
    log_file_path = os.path.join(documents_folder, "restart_nzxt_cam_on_idle.log")

    # Ensure the directory exists
    log_directory = os.path.dirname(log_file_path)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Configure logging with RotatingFileHandler
    handler = RotatingFileHandler(
        log_file_path,
        maxBytes=1024,  # 1 KB
        backupCount=2,  # Number of backup files
    )

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[handler],
    )

    process_name = "NZXT CAM.exe"
    executable_path = r"C:\Program Files\NZXT CAM\NZXT CAM.exe"
    idle_threshold = 2 * 3600  # 2 hours in seconds

    logging.critical("=== Starting script ===")
    logging.debug(f"idle_threshold={idle_threshold/3600} hours")

    while True:
        idle_time = get_idle_duration()
        logging.debug(f"idle_time={idle_time/3600} hours")

        # Reset NZXT CAM only while idle
        if idle_time >= idle_threshold:
            logging.info(f"Idle threshold reached: {idle_time}/{idle_threshold}")
            # Kill the process if it is running
            logging.debug("Killing NZXT Cam...")
            kill_process_by_name(process_name)

            logging.debug("NZXT Cam was killed, sleeping for 10 seconds...")
            time.sleep(10)

            # Start the process in hidden mode and immediately return
            logging.debug("Starting NZXT Cam...")
            start_process_hidden(executable_path)

            # Wait some time before allowing another potential reset
            sleep_after_restart = 3 * 3600
            time.sleep(sleep_after_restart)
            logging.info(f"CAM restarted. Sleeping {sleep_after_restart/3600} hours")
        else:
            # Check idle time again in 10 minutes
            time.sleep(600)


if __name__ == "__main__":
    main()
