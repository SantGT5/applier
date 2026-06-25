'''
Author:     Sai Vignesh Golla
LinkedIn:   https://www.linkedin.com/in/saivigneshgolla/

Copyright (C) 2024 Sai Vignesh Golla

License:    GNU Affero General Public License
            https://www.gnu.org/licenses/agpl-3.0.en.html
            
GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn

Support me: https://github.com/sponsors/GodsScion

version:    26.01.20.5.08
'''

from modules.helpers import get_default_temp_profile, make_directories
from config.settings import run_in_background, stealth_mode, disable_extensions, safe_mode, file_name, failed_file_name, logs_folder_path, generated_resume_path
from config.questions import default_resume_path
if stealth_mode:
    import undetected_chromedriver as uc
else: 
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    # from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from modules.helpers import (
    find_default_profile_directory,
    get_installed_chrome_major_version,
    get_undetected_chromedriver_cache_path,
    is_chrome_running,
    is_patched_undetected_chromedriver,
    critical_error_log,
    print_lg,
)
from selenium.common.exceptions import SessionNotCreatedException

def _apply_chrome_stability_options(options) -> None:
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-popup-blocking")


def _create_undetected_chrome(options, *, force_download: bool = False):
    chrome_major = get_installed_chrome_major_version()
    chrome_kwargs = {"options": options}
    if chrome_major:
        chrome_kwargs["version_main"] = chrome_major

    if not force_download:
        cached_driver = get_undetected_chromedriver_cache_path()
        if cached_driver and is_patched_undetected_chromedriver(cached_driver):
            print_lg("Using cached ChromeDriver (skipping download)")
            chrome_kwargs["driver_executable_path"] = cached_driver
            return uc.Chrome(**chrome_kwargs)

    print_lg("Downloading ChromeDriver... first run or Chrome update may take a minute.")
    if chrome_major:
        print_lg(f"Matching ChromeDriver to installed Chrome {chrome_major}")
    return uc.Chrome(**chrome_kwargs)


def createChromeSession(isRetry: bool = False, force_driver_download: bool = False):
    make_directories([file_name,failed_file_name,logs_folder_path+"/screenshots",default_resume_path,generated_resume_path+"/temp"])
    # Set up WebDriver with Chrome Profile
    options = uc.ChromeOptions() if stealth_mode else Options()
    if run_in_background:   options.add_argument("--headless")
    if disable_extensions:  options.add_argument("--disable-extensions")
    _apply_chrome_stability_options(options)

    print_lg("IF YOU HAVE MORE THAN 10 TABS OPENED, PLEASE CLOSE OR BOOKMARK THEM! Or it's highly likely that application will just open browser and not do anything!")
    if is_chrome_running():
        print_lg("Google Chrome is already running. Quit Chrome completely before starting the bot to avoid crashes and slow startup.")

    profile_dir = find_default_profile_directory()
    if isRetry:
        print_lg("Will login with a guest profile, browsing history will not be saved in the browser!")
    elif profile_dir and not safe_mode:
        options.add_argument(f"--user-data-dir={profile_dir}")
    else:
        print_lg("Logging in with a guest profile, Web history will not be saved!")
        options.add_argument(f"--user-data-dir={get_default_temp_profile()}")
    if stealth_mode:
        driver = _create_undetected_chrome(options, force_download=force_driver_download)
    else:
        driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 5)
    actions = ActionChains(driver)
    return options, driver, actions, wait

try:
    options, driver, actions, wait = None, None, None, None
    options, driver, actions, wait = createChromeSession()
except SessionNotCreatedException as e:
    critical_error_log("Failed to create Chrome Session, retrying with guest profile", e)
    try:
        driver.quit()
    except Exception:
        pass
    options, driver, actions, wait = createChromeSession(True, force_driver_download=True)
except Exception as e:
    msg = 'Seems like Google Chrome is out dated. Update browser and try again! \n\n\nIf issue persists, try Safe Mode. Set, safe_mode = True in config.py \n\nPlease check GitHub discussions/support for solutions https://github.com/GodsScion/Auto_job_applier_linkedIn \n                                   OR \nReach out in discord ( https://discord.gg/fFp7uUzWCY )'
    if isinstance(e,TimeoutError): msg = "Couldn't download Chrome-driver. Set stealth_mode = False in config!"
    print_lg(msg)
    critical_error_log("In Opening Chrome", e)
    from modules.helpers import safe_alert
    safe_alert(msg, "Error in opening chrome")
    try: driver.quit()
    except NameError: exit()
    
