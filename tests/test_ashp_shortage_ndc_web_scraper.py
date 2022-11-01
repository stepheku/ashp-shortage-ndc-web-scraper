import pytest
from ashp_shortage_ndc_web_scraper import ashp_shortage_ndc_web_scraper


@pytest.fixture()
def current_shortages_meds_list():
    """
    Fixture for the current_shortages_meds_list to be used across multiple tests
    """
    return ashp_shortage_ndc_web_scraper.current_shortages_meds_table_to_list()


def test_current_shortages_meds_table_to_list_len_greater_than_0(
    current_shortages_meds_list,
):
    assert len(current_shortages_meds_list) > 0


def test_current_shortages_meds_table_to_list_returns_list(
    current_shortages_meds_list,
):
    assert isinstance(current_shortages_meds_list, list)


@pytest.fixture()
def resolved_shortages_meds_list():
    """
    Fixture for the resolved_shortages_meds_list to be used across multiple tests
    """
    return ashp_shortage_ndc_web_scraper.resolved_shortages_meds_table_to_list()


def test_resolved_shortages_meds_table_to_list_len_greater_than_0(
    resolved_shortages_meds_list,
):
    assert len(resolved_shortages_meds_list) > 0


def test_resolved_shortages_meds_table_to_list_returns_list(
    resolved_shortages_meds_list,
):
    assert isinstance(resolved_shortages_meds_list, list)