# About

This script is general-use and can be used to restart any process - see `PROCESS_NAME` and `EXECUTABLE_PATH`. The use case outlined in this document is to restart the NZXT CAM application.

NZXT CAM is needed to run the screen on my NZXT AIO. NZXT CAM has a memory leak issue and NZXT is not able to fix it. This script attempts to mitigate the effects of the memory leak by restarting NZXT CAM on occasion; on starting the script and then when the computer has been idle for some time (`IDLE_THRESHOLD`).

I recommend setting the script to automatically run when the workstation is unlocked - see Task Scheduler Settings section below. If you follow this suggestion, then NZXT CAM will restart after idling for `IDLE_THRESHOLD` seconds and when you unlock your workstation.

Use Task Scheduler to run `restart_process_on_idle.py`. Do not set the task to run on idle, the script is already taking care of checking the idle time. The script is designed to stay alive alongside NZXT CAM.

Make sure to go to the settings of NZXT CAM and **DISABLE** it from starting on Windows startup. The script will take care of launching the app.

`restart_process_on_idle.py` logs are stored in `~/Documents/restart_process_on_idle_logs`.

# Requirements

-   Python3
-   psutils module from pypi

# Task Scheduler Settings

General

-   Run only when user is logged on

Triggers

-   On workstation unlock

Actions

-   Use python to run the script, for example: `C:\Users\Jason\AppData\Local\Programs\Python\Python312\pythonw.exe "D:\Projects\restart_process_on_idle\restart_process_on_idle.py"`

Conditions

-   Untick all

Settings

-   Allow task to be run on demand
-   If the running task does not end when requested, force it to stop
