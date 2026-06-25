"""
Author:     Sai Vignesh Golla
LinkedIn:   https://www.linkedin.com/in/saivigneshgolla/

Copyright (C) 2024 Sai Vignesh Golla

License:    GNU Affero General Public License
            https://www.gnu.org/licenses/agpl-3.0.en.html

GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn

Support me: https://github.com/sponsors/GodsScion

version:    26.01.20.5.08
"""

# Imports

import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pprint import pprint
from random import randint
from time import sleep

from config.settings import logs_folder_path

#### Common functions ####


# < Directories related
def make_directories(paths: list[str]) -> None:
    """
    Function to create missing directories
    """
    for path in paths:
        path = os.path.expanduser(path)  # Expands ~ to user's home directory
        path = path.replace("//", "/")

        # If path looks like a file path, get the directory part
        if "." in os.path.basename(path):
            path = os.path.dirname(path)

        if not path:  # Handle cases where path is empty after dirname
            continue

        try:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)  # exist_ok=True avoids race condition
        except Exception as e:
            print(f'Error while creating directory "{path}": ', e)


def get_default_temp_profile() -> str:
    # Thanks to https://github.com/vinodbavage31 for suggestion!
    home = pathlib.Path.home()
    if sys.platform.startswith("win"):
        return "C:\\temp\\auto-job-apply-profile"
    return str(home / ".auto-job-apply-profile")


def get_undetected_chromedriver_cache_path() -> str | None:
    """
    Path to undetected-chromedriver's cached patched binary, if it exists.
    Reusing this avoids re-downloading ChromeDriver on every run.
    """
    home = pathlib.Path.home()
    if sys.platform == "darwin":
        data_path = home / "Library" / "Application Support" / "undetected_chromedriver"
    elif sys.platform.startswith("win"):
        data_path = home / "AppData" / "Roaming" / "undetected_chromedriver"
    else:
        data_path = home / ".local" / "share" / "undetected_chromedriver"

    exe_name = (
        "undetected_chromedriver.exe"
        if sys.platform.startswith("win")
        else "undetected_chromedriver"
    )
    cached = data_path / exe_name
    return str(cached) if cached.is_file() else None


def is_patched_undetected_chromedriver(path: str) -> bool:
    try:
        with open(path, "rb") as fh:
            return fh.read().find(b"undetected chromedriver") != -1
    except OSError:
        return False


def is_chrome_running() -> bool:
    try:
        if sys.platform == "darwin":
            subprocess.check_call(
                ["pgrep", "-x", "Google Chrome"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        if sys.platform.startswith("win"):
            out = subprocess.check_output(
                'tasklist /FI "IMAGENAME eq chrome.exe"',
                shell=True,
                text=True,
                stderr=subprocess.DEVNULL,
            )
            return "chrome.exe" in out.lower()
        subprocess.check_call(
            ["pgrep", "-x", "chrome"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (subprocess.CalledProcessError, OSError):
        return False


def tkinter_available() -> bool:
    try:
        import tkinter  # noqa: F401

        return True
    except ImportError:
        return False


def safe_alert(text: str = "", title: str = "", button: str = "OK") -> str:
    """
    Shows a GUI alert when Tkinter is available; otherwise logs and waits at the terminal.
    """
    if tkinter_available():
        try:
            from pyautogui import alert

            return alert(text, title, button)
        except AssertionError:
            pass
    header = f"[{title}]" if title else "[Alert]"
    print(f"\n{header}\n{text}\n")
    try:
        with open(__logs_file_path, "a+", encoding="utf-8") as file:
            file.write(f"{header}\n{text}\n")
    except Exception:
        pass
    try:
        input(f"Press Enter to continue ({button})... ")
    except EOFError:
        pass
    return button


def safe_confirm(
    text: str = "",
    title: str = "",
    buttons: tuple | list = ("OK", "Cancel"),
) -> str | None:
    """
    Shows a GUI confirm dialog when Tkinter is available; otherwise prompts in the terminal.
    """
    if isinstance(buttons, list):
        buttons = tuple(buttons)
    if tkinter_available():
        try:
            from pyautogui import confirm

            return confirm(text, title, buttons)
        except AssertionError:
            pass
    header = f"[{title}]" if title else "[Confirm]"
    print(f"\n{header}\n{text}\n")
    for i, label in enumerate(buttons, 1):
        print(f"  {i}. {label}")
    try:
        with open(__logs_file_path, "a+", encoding="utf-8") as file:
            file.write(f"{header}\n{text}\n")
    except Exception:
        pass
    try:
        choice = input(f"Choose 1-{len(buttons)} (default 1): ").strip()
        if not choice:
            return buttons[0]
        idx = int(choice) - 1
        if 0 <= idx < len(buttons):
            return buttons[idx]
    except (EOFError, ValueError):
        pass
    return buttons[0]


def get_installed_chrome_major_version() -> int | None:
    """
    Returns the major version of the installed Google Chrome (e.g. 148), or None.
    Used so undetected-chromedriver downloads a matching ChromeDriver build.
    """
    candidates: list[str] = []
    if sys.platform == "darwin":
        candidates.append(
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        )
    elif sys.platform.startswith("win"):
        for env_var in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"):
            base = os.environ.get(env_var)
            if base:
                candidates.append(
                    os.path.join(base, "Google", "Chrome", "Application", "chrome.exe")
                )
    else:
        for name in (
            "google-chrome",
            "google-chrome-stable",
            "chromium",
            "chromium-browser",
        ):
            found = shutil.which(name)
            if found:
                candidates.append(found)

    for exe in candidates:
        if not os.path.isfile(exe):
            continue
        try:
            out = subprocess.check_output(
                [exe, "--version"],
                stderr=subprocess.STDOUT,
                text=True,
                timeout=10,
            )
            match = re.search(r"(\d+)\.", out)
            if match:
                return int(match.group(1))
        except (OSError, subprocess.SubprocessError, ValueError):
            continue
    return None


def find_default_profile_directory() -> str | None:
    """
    Dynamically finds the default Google Chrome 'User Data' directory path
    across Windows, macOS, and Linux, regardless of OS version.

    Returns the absolute path as a string, or None if the path is not found.
    """

    home = pathlib.Path.home()

    # Windows
    if sys.platform.startswith("win"):
        paths = [
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data"),
            os.path.expandvars(r"%USERPROFILE%\AppData\Local\Google\Chrome\User Data"),
            os.path.expandvars(
                r"%USERPROFILE%\Local Settings\Application Data\Google\Chrome\User Data"
            ),
        ]
    # Linux
    elif sys.platform.startswith("linux"):
        paths = [
            str(home / ".config" / "google-chrome"),
            str(
                home
                / ".var"
                / "app"
                / "com.google.Chrome"
                / "data"
                / ".config"
                / "google-chrome"
            ),
        ]
    # MacOS ## For some reason, opening with profile in MacOS is not creating a session for undetected-chromedriver!
    # elif sys.platform == 'darwin':
    #     paths = [
    #         str(home / "Library" / "Application Support" / "Google" / "Chrome")
    #     ]
    else:
        return None

    # Check each potential path and return the first one that exists
    for path_str in paths:
        if os.path.exists(path_str):
            return path_str

    return None


# >


# < Logging related
def critical_error_log(possible_reason: str, stack_trace: Exception) -> None:
    """
    Function to log and print critical errors along with datetime stamp
    """
    print_lg(possible_reason, stack_trace, datetime.now(), from_critical=True)


def get_log_path():
    """
    Function to replace '//' with '/' for logs path
    """
    try:
        path = logs_folder_path + "/log.txt"
        return path.replace("//", "/")
    except Exception as e:
        critical_error_log(
            "Failed getting log path! So assigning default logs path: './logs/log.txt'",
            e,
        )
        return "logs/log.txt"


__logs_file_path = get_log_path()


def print_lg(
    *msgs: str | dict,
    end: str = "\n",
    pretty: bool = False,
    flush: bool = False,
    from_critical: bool = False,
) -> None:
    """
    Function to log and print. **Note that, `end` and `flush` parameters are ignored if `pretty = True`**
    """
    try:
        for message in msgs:
            pprint(message) if pretty else print(message, end=end, flush=flush)
            with open(__logs_file_path, "a+", encoding="utf-8") as file:
                file.write(str(message) + end)
    except Exception as e:
        trail = (
            f'Skipped saving this message: "{message}" to log.txt!'
            if from_critical
            else "We'll try one more time to log..."
        )
        safe_alert(
            f"log.txt in {logs_folder_path} is open or is occupied by another program! Please close it! {trail}",
            "Failed Logging",
        )
        if not from_critical:
            critical_error_log("Log.txt is open or is occupied by another program!", e)


# >


def buffer(speed: int = 0) -> None:
    """
    Function to wait within a period of selected random range.
    * Will not wait if input `speed <= 0`
    * Will wait within a random range of
      - `0.6 to 1.0 secs` if `1 <= speed < 2`
      - `1.0 to 1.8 secs` if `2 <= speed < 3`
      - `1.8 to speed secs` if `3 <= speed`
    """
    if speed <= 0:
        return
    elif speed <= 1 and speed < 2:
        return sleep(randint(6, 10) * 0.1)
    elif speed <= 2 and speed < 3:
        return sleep(randint(10, 18) * 0.1)
    else:
        return sleep(randint(18, round(speed) * 10) * 0.1)


def manual_login_retry(is_logged_in: callable, limit: int = 2) -> None:
    """
    Function to ask and validate manual login
    """
    count = 0
    while not is_logged_in():
        print_lg("Seems like you're not logged in!")
        button = "Confirm Login"
        message = (
            'After you successfully Log In, please click "{}" button below.'.format(
                button
            )
        )
        if count > limit:
            button = "Skip Confirmation"
            message = 'If you\'re seeing this message even after you logged in, Click "{}". Seems like auto login confirmation failed!'.format(
                button
            )
        count += 1
        if safe_alert(message, "Login Required", button) and count > limit:
            return


DATE_POSTED_F_TPR = {
    "Past month": "r2592000",
    "Past week": "r604800",
    "Past 24 hours": "r86400",
}

SORT_BY_URL = {
    "Most recent": "DD",
    "Most relevant": "R",
}


def build_jobs_search_url(
    keywords: str, *, date_posted: str = "", sort_by: str = ""
) -> str:
    """
    Build a LinkedIn jobs search URL with date and sort filters applied via query params.
    """
    from urllib.parse import urlencode

    query: dict[str, str] = {"keywords": keywords}
    tpr = DATE_POSTED_F_TPR.get((date_posted or "").strip())
    if tpr:
        query["f_TPR"] = tpr
    sort = SORT_BY_URL.get((sort_by or "").strip())
    if sort:
        query["sortBy"] = sort
    return "https://www.linkedin.com/jobs/search/?" + urlencode(query)


def calculate_date_posted(time_string: str) -> datetime | None | ValueError:
    """
    Function to calculate date posted from string.
    Returns datetime object | None if unable to calculate | ValueError if time_string is invalid
    Valid time string examples:
    * 10 seconds ago
    * 15 minutes ago
    * 2 hours ago
    * 1 hour ago
    * 1 day ago
    * 10 days ago
    * 1 week ago
    * 1 month ago
    * 1 year ago
    """
    import re

    time_string = time_string.strip()
    now = datetime.now()

    match = re.search(
        r"(\d+)\s+(second|minute|hour|day|week|month|year)s?\s+ago",
        time_string,
        re.IGNORECASE,
    )

    if match:
        try:
            value = int(match.group(1))
            unit = match.group(2).lower()

            if "second" in unit:
                return now - timedelta(seconds=value)
            elif "minute" in unit:
                return now - timedelta(minutes=value)
            elif "hour" in unit:
                return now - timedelta(hours=value)
            elif "day" in unit:
                return now - timedelta(days=value)
            elif "week" in unit:
                return now - timedelta(weeks=value)
            elif "month" in unit:
                return now - timedelta(days=value * 30)  # Approximation
            elif "year" in unit:
                return now - timedelta(days=value * 365)  # Approximation
        except (ValueError, IndexError):
            # Fallback for cases where parsing fails
            pass

    # If regex doesn't match, or parsing failed, return None.
    # This will skip jobs where the date can't be determined, preventing crashes.
    return None


def convert_to_lakhs(value: str) -> str:
    """
    Converts str value to lakhs, no validations are done except for length and stripping.
    Examples:
    * "100000" -> "1.00"
    * "101,000" -> "10.1," Notice ',' is not removed
    * "50" -> "0.00"
    * "5000" -> "0.05"
    """
    value = value.strip()
    l = len(value)
    if l > 0:
        if l > 5:
            value = value[: l - 5] + "." + value[l - 5 : l - 3]
        else:
            value = "0." + "0" * (5 - l) + value[:2]
    return value


def convert_to_json(data) -> dict:
    """
    Function to convert data to JSON, if unsuccessful, returns `{"error": "Unable to parse the response as JSON", "data": data}`
    """
    try:
        result_json = json.loads(data)
        return result_json
    except json.JSONDecodeError:
        return {"error": "Unable to parse the response as JSON", "data": data}


def truncate_for_csv(
    data, max_length: int = 131000, suffix: str = "...[TRUNCATED]"
) -> str:
    """
    Function to truncate data for CSV writing to avoid field size limit errors.
    * Takes in `data` of any type and converts to string
    * Takes in `max_length` of type `int` - maximum allowed length (default: 131000, leaving room for suffix)
    * Takes in `suffix` of type `str` - text to append when truncated
    * Returns truncated string if data exceeds max_length
    """
    try:
        # Convert data to string
        str_data = str(data) if data is not None else ""

        # If within limit, return as-is
        if len(str_data) <= max_length:
            return str_data

        # Truncate and add suffix
        truncated = str_data[: max_length - len(suffix)] + suffix
        return truncated
    except Exception as e:
        return f"[ERROR CONVERTING DATA: {e}]"
