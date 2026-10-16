from selenium.common.exceptions import ElementClickInterceptedException

from modules.clickers_and_finders import click_displayed


class FakeElement:
    def __init__(self, displayed=True, click_error=None):
        self.displayed = displayed
        self.click_error = click_error
        self.clicked = False

    def is_displayed(self):
        return self.displayed

    def click(self):
        if self.click_error:
            raise self.click_error
        self.clicked = True


class FakeDriver:
    def __init__(self, elements):
        self.elements = elements
        self.scripts = []

    def find_elements(self, by, value):
        return self.elements

    def execute_script(self, script, *args):
        self.scripts.append((script, args))


def test_returns_false_without_a_match():
    assert click_displayed(FakeDriver([]), "//button") is False


def test_returns_false_when_every_match_is_hidden():
    hidden = FakeElement(displayed=False)
    assert click_displayed(FakeDriver([hidden]), "//button") is False
    assert not hidden.clicked


def test_clicks_the_displayed_match():
    hidden, shown = FakeElement(displayed=False), FakeElement()
    driver = FakeDriver([hidden, shown])
    assert click_displayed(driver, "//button") is True
    assert shown.clicked and not hidden.clicked
    # Scrolled into view first, without smooth-scroll animation.
    assert driver.scripts[0][1] == (shown,) and "instant" in driver.scripts[0][0]


def test_clicks_with_javascript_when_something_covers_the_element():
    covered = FakeElement(click_error=ElementClickInterceptedException("header on top"))
    driver = FakeDriver([covered])
    assert click_displayed(driver, "//button") is True
    assert driver.scripts[-1] == ("arguments[0].click();", (covered,))
