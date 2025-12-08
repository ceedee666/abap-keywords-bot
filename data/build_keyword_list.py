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
    page = BeautifulSoup(r.text, "html.parser")

    elements = page.find_all("a", href=re.compile("call_link"))

    elements = set(elements)
    logger.info(f"Found {len(elements)} unique keywords")

    return [e["href"].split("'")[1] for e in elements]


def parse_keyword_page(path, base_url=BASE_URL):
    logger.info(f"Parsing keyword page: {path}")

    url = base_url + path
    r = requests.get(url)
    keyword_page = BeautifulSoup(r.text, "html.parser")

    h1 = keyword_page.find("span", "h1")

    if h1 is None:
        logger.warning(f"Could not find h1 on page: {url}")
        return None, None
    else:
        heading = h1.get_text().strip()
        logger.info(f"Found heading: {heading} at {url}")
        return heading, url


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
        heading, url = parse_keyword_page(page)
        if heading is not None:
            keyword_list.append({"heading": heading, "url": url})

    with open(output, "w") as f:
        logger.info("Writing keyword list to file")
        json.dump(keyword_list, f)

    logger.info("Finished keyword list build")


if __name__ == "__main__":
    build_keyword_list()
