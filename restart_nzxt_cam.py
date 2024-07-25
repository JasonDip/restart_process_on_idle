import psutil
import subprocess
import time


def kill_process_by_name(process_name):
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == process_name:
            proc.kill()


def start_process_hidden(executable_path):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0  # SW_HIDE
    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    subprocess.Popen(
        executable_path, startupinfo=startupinfo, creationflags=creationflags
    )


def main():
    process_name = "NZXT CAM.exe"
    executable_path = r"C:\Program Files\NZXT CAM\NZXT CAM.exe"

    # Kill the process if it is running
    print(f"About to kill the process: {process_name}")
    kill_process_by_name(process_name)

    print("Finished killing the process. Waiting 10 seconds...")
    time.sleep(10)

    # Start the process in hidden mode and immediately return
    print(f"Starting process: {executable_path}")
    start_process_hidden(executable_path)

    time.sleep(10)


if __name__ == "__main__":
    main()
