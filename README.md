# About

NZXT Cam is needed to run the screen on my NZXT Kraken Elite AIO. Annoyingly, it has a memory leak issue and NZXT is not able to fix it. This script is used to (during idle) restart NZXT Cam to release the memory.

Use Task Scheduler to run `restart_nzxt_cam_on_idle.py` when you log into your system. Do not set the task to run on idle, the script is already taking care of checking the idle time. The script is designed to stay alive because when you restart NZXT Cam, it is attached to the script's process. I wasn't able to detach it; I think the issue is related to how Cam does its logs.

`restart_nzxt_cam_on_idle.py` logs are stored in `~/Documents/restart_nzxt_cam_on_idle`.

# Requirements

-   Python3
-   psutils module from pypi

# Task Scheduler Settings

General

-   Run only when user is logged on
    -   Probably set it to your own user

Triggers

-   At log on

Actions

-   C:\Users\Jason\AppData\Local\Programs\Python\Python312\pythonw.exe "D:\Projects\restart_nzxt_cam\restart_nzxt_cam_on_idle.py"

Conditions

-   Untick all

Settings

-   Allow task to be run on demand
-   If the running task does not end when requested, force it to stop
