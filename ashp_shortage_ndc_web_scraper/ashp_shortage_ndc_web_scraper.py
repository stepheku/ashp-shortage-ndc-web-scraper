"""
ashp_drug_shortage_ndcs.py
~~~~~~~~~~~~~~~~~~~~
This module is a web scraper of ASHP's current-shortages website. We're using
this web-scraping route because ASHP (or University of Utah) used to have
the information as an RSS feed, but recently has changed to an API model
"""


from time import sleep
import requests
import re
import random
from datetime import datetime
import csv
from bs4 import BeautifulSoup
from pathlib import Path

BASE_URL = "https://www.ashp.org/drug-shortages/current-shortages"


def ashp_page_meds_table_to_list(page: str) -> list:
    """
    Given a page under "current-shortages/drug-shortage-list", this will
    request the page and read the first table (which hopefully contains all
    of the impacted medications and their links)

    Args:
        page (str): Valid page name (CurrentShortages or ResolvedShortages)

    Returns:
        list: List of dictionaries to go into a spreadsheet
    """

    url = f"{BASE_URL}/drug-shortages-list"

    url += f"?page={page}"

    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")

    table_of_meds = soup.find_all("table")[0]

    output_list = []

    for row in table_of_meds.tbody.find_all("tr"):
        # Find data for each column of the row
        columns = row.find_all("td")

        if columns:
            drug = columns[0].text.strip()
            link = columns[0].find("a")["href"]
            date = datetime.strptime(columns[1].text.strip(), "%b %d, %Y")

            output_list.append(
                {
                    "drug": drug,
                    "link": link,
                    "date": date,
                }
            )

    return output_list


def current_shortages_meds_table_to_list() -> list:
    """
    Returns a list of dictionaries off of the table read on the
    CurrentShortages page

    Returns:
        list: List of dictionaries to go into a spreadsheet
    """
    return ashp_page_meds_table_to_list(page="CurrentShortages")


def resolved_shortages_meds_table_to_list() -> list:
    """
    Returns a list of dictionaries off of the table read on the
    ResolvedShortages page

    Returns:
        list: List of dictionaries to go into a spreadsheet
    """
    return ashp_page_meds_table_to_list(page="ResolvedShortages")


def detail_page_to_dict(url: str) -> dict:
    """
    Reads page contents for a drug-shortage-detail page and converts the list
    contents contained in any h3 tag into a dictionary of lists

    Args:
        url (str): Valid page url (drug-shortage-detail.aspx)

    Returns:
        dict: Dictionary of lists
    """

    url = f"{BASE_URL}/{url}"

    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")

    # For each page, each section is denoted as an h3 tag
    headers = soup.find_all("h3")

    output_dict = {}

    for header in headers:

        # Find sublings from the same level
        lists = header.find_next_sibling()

        if lists:
            header_text = header.text
            output_dict[header_text] = []

            list_elements = lists.find_all("li")
            for list_element in list_elements:

                # Ignore any list element with a span tag. For whatever reason, the
                # span tag concatenates all of the list elements into a single
                # element at the beginning
                if not list_element.find_all("span"):
                    output_dict[header_text].append(list_element.text)

    return output_dict


def find_ndcs_in_str(s: str) -> list:
    """
    Using regular expressions, find any NDCs (with dashes) within a string. 
    Looks for padded 5-4-2 formats, or any non-padded formats

    Args:
        s (str): Valid string possibly containing NDCs

    Returns:
        list: List of regex matches
    """
    ndc_regex = r"\d{4,5}-\d{3,4}-\d{1,2}"
    return re.findall(ndc_regex, s)


def output_to_csv(l: list, output_csv_path: Path) -> None:
    with open(output_csv_path, "w", newline="") as f:
        """
        Headers:
        Drug, Link, Date, Header (Impacted Products, etc), Value, NDCs
        """

        fieldnames = [
            "drug","link","date","header","value","ndc"
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in l:
            drug = row.get("drug")
            link = row.get("link")
            date = row.get("date")

            for k, values in row.items():
                if k in ["drug","link","date"]:
                    continue
                
                header = k
                
                for row in values:
                    ndc = find_ndcs_in_str(row)
                    value = row
                    writer.writerow(
                        {
                            "drug":drug,
                            "link":link,
                            "date":date,
                            "header":header,
                            "value":value,
                            "ndc":ndc,
                        }
                    )


if __name__ == "__main__":
    l = current_shortages_meds_table_to_list()

    output_list = []

    for idx, row in enumerate(l):
        # if idx > 10:
            # break

        shortage_detail_page = row.get("link")

        sleep(random.uniform(0.0, 1.5))
        d = detail_page_to_dict(url=shortage_detail_page)

        d.update(row)

        if d:
            output_list.append(d)

    output_to_csv(output_list, Path("./output.csv"))