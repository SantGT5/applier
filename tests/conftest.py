import os
import sys

import pytest
from lxml import html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

FIXTURES = os.path.join(ROOT, "tests", "fixtures")


@pytest.fixture
def search_page():
    """Parsed LinkedIn /jobs/search-results/ page (lxml uses XPath 1.0, same as Selenium)."""
    with open(
        os.path.join(FIXTURES, "search_results_page.html"), encoding="utf-8"
    ) as file:
        return html.fromstring(file.read())
