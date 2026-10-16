"""
Selectors and parsers for LinkedIn's AI-powered jobs search page (/jobs/search-results/).

CSS class names on this page are randomized per build, so everything here keys off
stable attributes instead: `componentkey`, `data-testid`, `aria-label`, and element
ids that embed the job id. Covered by tests/test_linkedin_ui.py.
"""

import re

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# < Job list
JOB_CARD_KEY_PREFIX = "job-card-component-ref-"
JOB_CARDS_XPATH = (
    f"//div[@role='button' and starts-with(@componentkey, '{JOB_CARD_KEY_PREFIX}')]"
)


def job_card_xpath(job_id: str) -> str:
    return f"//div[@role='button' and @componentkey='{JOB_CARD_KEY_PREFIX}{job_id}']"


def job_id_from_card_key(componentkey: str) -> str:
    return componentkey.removeprefix(JOB_CARD_KEY_PREFIX)


# Relative to a job card. The title <p> also holds a screen-reader-only copy, so take the visible span.
CARD_TITLE_XPATH = "(.//div[@data-display-contents='true']/p/span[@aria-hidden='true'])[1]"
CARD_COMPANY_XPATH = (
    "(.//div[@data-display-contents='true'][p])[1]/following-sibling::div[1]/p"
)
CARD_LOCATION_XPATH = (
    "(.//div[@data-display-contents='true'][p])[1]/following-sibling::p[1]"
)
CARD_APPLIED_XPATH = ".//p[normalize-space()='Applied']"


def split_work_location(text: str) -> tuple[str, str]:
    """
    "United States (Remote)" -> ("United States", "Remote"); "Toronto, ON" -> ("Toronto, ON", "")
    """
    text = text.strip()
    match = re.fullmatch(r"(.*?)\s*\(([^()]*)\)", text)
    if match:
        return match.group(1), match.group(2)
    return text, ""


# >


# < Job details panel
JOB_DETAILS_XPATH = (
    "//div[@data-sdui-screen='com.linkedin.sdui.flagshipnav.jobs.SemanticJobDetails']"
)
# Relative to the job details panel. The first "... ago" text is the posted date in the header.
TIME_POSTED_XPATH = "(.//*[contains(text(), ' ago')])[1]"
EASY_APPLY_BUTTON_XPATH = "//button[@aria-label='Easy Apply to this job']"
# Relative to the hiring team link.
HIRER_NAME_XPATH = "(.//p)[1]"


def job_details_loaded_xpath(job_id: str) -> str:
    return f"{JOB_DETAILS_XPATH}//a[contains(@href, '/jobs/view/{job_id}/')]"


def about_job_xpath(job_id: str) -> str:
    # The whole section, since the description isn't always in an expandable text box.
    # Its "About the job" heading is removed by `clean_description`.
    return f"//div[@id='JobDetails_AboutTheJob_{job_id}']"


def about_company_xpath(job_id: str) -> str:
    return f"//div[@id='JobDetails_AboutTheCompany_{job_id}']"


def hiring_team_link_xpath(job_id: str) -> str:
    # The same slot also lists "People you can reach out to"; only take people after the hiring team heading.
    return (
        f"(//div[@id='JobDetailsPeopleWhoCanHelpSlot_{job_id}']"
        "//a[contains(@href, '/in/')][preceding::*[normalize-space()='Meet the hiring team']])[1]"
    )


def clean_description(text: str) -> str:
    """
    Removes the "About the job" heading and the trailing "… more" expand button text.
    """
    text = re.sub(r"^\s*About the job(?![a-z])\s*", "", text)
    return re.sub(r"\s*…\s*more\s*$", "", text).strip()


# >


# < Easy Apply dialog
EASY_APPLY_MODAL_XPATH = (
    "//dialog[.//*[@data-sdui-screen='com.linkedin.sdui.flagshipnav.jobs.easyapply.EasyApply']]"
)
# LinkedIn sometimes shows "This job may not be the best fit" before the Easy Apply form.
APPLY_INTERCEPT_CONTINUE_XPATH = (
    "//dialog[.//*[@data-sdui-screen='com.linkedin.sdui.flagshipnav.jobs.ApplyInterceptModal']]"
    "//a[normalize-space()='Continue applying']"
)
# Relative to the dialog. A question is a <fieldset> (option groups), a <div> holding a
# <label for> (contact fields), or an "easyApplyFieldFocus" wrapper without a label
# (screening questions). Some fields carry that marker themselves, so take their parent.
FORM_QUESTIONS_XPATH = (
    ".//fieldset[not(ancestor::fieldset)]"
    " | .//div[label[@for]][not(ancestor::fieldset)]"
    " | .//div[starts-with(@componentkey, 'easyApplyFieldFocus')]"
    "[not(.//label[@for])][not(ancestor::fieldset)]"
    " | .//*[self::input or self::select or self::textarea]"
    "[starts-with(@componentkey, 'easyApplyFieldFocus')][not(ancestor::fieldset)]/.."
)
# Relative to a question.
FORM_TEXT_INPUT_XPATH = (
    ".//input[not(@type) or @type='text' or @type='tel' or @type='email' or @type='number' or @type='url']"
)
EASY_APPLY_PROGRESS_XPATH = ".//*[@role='progressbar']"
# Relative to the dialog. The form page's title, e.g. "Contact info".
EASY_APPLY_PAGE_TITLE_XPATH = "(.//div[@data-testid='lazy-column']//p)[1]"

# Relative to a radio question. Each option is a role="radio" element whose aria-label is the
# question and whose text is the option; its <label> is empty.
RADIO_OPTIONS_XPATH = ".//*[@role='radio']"
# Relative to a radio <input>.
RADIO_OPTION_OF_INPUT_XPATH = "ancestor::*[@role='radio'][1]"


def radio_option_xpath(answer: str) -> str:
    return f".//*[@role='radio'][normalize-space()='{answer}']"


def form_page_key(modal: WebElement) -> tuple[str | None, str | None]:
    """
    Identifies the Easy Apply form page shown, by its progress and title, to tell whether
    clicking Next or Review moved on. Unanswered required fields keep the form on its page.
    """

    def read(get_value):
        try:
            return get_value()
        except (NoSuchElementException, StaleElementReferenceException):
            return None

    return (
        read(
            lambda: modal.find_element(By.XPATH, EASY_APPLY_PROGRESS_XPATH).get_attribute(
                "aria-valuenow"
            )
        ),
        read(lambda: modal.find_element(By.XPATH, EASY_APPLY_PAGE_TITLE_XPATH).text),
    )


def question_label_text(text: str) -> str:
    """
    "Email address*" -> "Email address". Required fields end with "*".
    """
    return text.strip().removesuffix("*").strip()


def question_label(question: WebElement, control: WebElement) -> str:
    """
    A form question's text: its <label>, else the field's aria-label (screening questions),
    else the question's first paragraph (e.g. the location typeahead).
    """
    for get_text in (
        lambda: question.find_element(By.XPATH, ".//label[@for]").text,
        lambda: control.get_attribute("aria-label"),
        lambda: question.find_element(By.XPATH, ".//p").text,
    ):
        try:
            text = question_label_text(get_text() or "")
        except NoSuchElementException:
            continue
        if text:
            return text
    return "Unknown"


# >


# < Pagination
PAGINATION_XPATH = "//ul[@data-testid='pagination-controls-list']"
# Relative to the pagination list.
CURRENT_PAGE_XPATH = ".//button[@aria-current='true']"
NEXT_PAGE_BUTTON_XPATH = "//button[@data-testid='pagination-controls-next-button-visible']"


def page_button_xpath(page: int) -> str:
    return f"{PAGINATION_XPATH}//button[@aria-label='Page {page}']"


# >
