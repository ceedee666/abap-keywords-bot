import json
import logging
import re

import click
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/"
INDEX_PAGE = "ABENABAP_INDEX.html"


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def abap_keyword_pages():
    logger.info("Getting list of ABAP keyword pages from index")

    r = requests.get(BASE_URL + INDEX_PAGE)
    r.raise_for_status()

    # Find the script containing the oModel data
    soup = BeautifulSoup(r.text, "html.parser")
    scripts = soup.find_all("script")

    raw_data = ""
    for script in scripts:
        if script.string and "new sap.ui.model.json.JSONModel" in script.string:
            raw_data = script.string
            break

    if not raw_data:
        logger.error("Could not find the JavaScript model data on the page.")
        return []

    # Extract HTML fragments from the JS Model
    # These are stored as keys: ul1, ul2, par1 etc. followed by HTML in quotes
    # The regex captures the content between the double quotes for these keys
    html_fragments = re.findall(r'(?:ul\d+|par\d+)\s*:\s*"(.*?)"', raw_data)

    unique_hrefs = set()

    for fragment in html_fragments:
        clean_html = fragment.replace('\\"', '"').replace("\\ ", "")

        frag_soup = BeautifulSoup(clean_html, "html.parser")

        links = frag_soup.find_all("a", attrs={"target": "_parent"})

        for link in links:
            href = link.get("href")
            if href:
                unique_hrefs.add(href)

    logger.info(f"Found {len(unique_hrefs)} unique keyword pages")
    return list(unique_hrefs)


def parse_keyword_page(path, base_url=BASE_URL):
    logger.info(f"Parsing keyword page: {path}")

    url = base_url + path
    try:
        r = requests.get(url)
        r.raise_for_status()

        keyword_page = BeautifulSoup(r.text, "html.parser")

        title_tag = keyword_page.find("title")
        if title_tag:
            full_title = title_tag.get_text().strip()
            title = full_title.split("|")[0].strip()
            logger.info(f"Found title: {title} at {url}")
            return title, url
        else:
            logger.warning(f"Could not find title on page: {url}")
            return None, None

    except Exception as e:
        logger.error(f"Error parsing {path}: {e}")
        return None, None


@click.command()
@click.option("--output", "-o", default="keywords.json")
@click.option("--verbose", "-v", is_flag=True)
def build_keyword_list(output, verbose):
    if verbose:
        logger.setLevel(logging.DEBUG)

    logger.info("Starting keyword list build")

    keyword_pages = abap_keyword_pages()

    keyword_list = []
    for page in keyword_pages:
        title, url = parse_keyword_page(page)
        if title is not None:
            keyword_list.append({"title": title, "url": url})

    with open(output, "w") as f:
        logger.info("Writing keyword list to file")
        json.dump(keyword_list, f)

    logger.info("Finished keyword list build")


if __name__ == "__main__":
    build_keyword_list()
