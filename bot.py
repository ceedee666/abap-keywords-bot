import json
import logging
import os
from random import choice

import requests

ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
API_URL = os.environ["API_URL"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def toot_text():
    with open("data/keywords.json", "r") as f:
        keywords = json.load(f)

    keyword = choice(keywords)

    return f"The next random #ABAP keyword is: \n\n   {keyword['heading']} \n\nWant to learn more? See: {keyword['url']}."


def toot():
    logger.info("Trying to toot...")

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    status = toot_text()

    r = requests.post(API_URL, headers=headers, data={"status": status})

    if r.status_code != 200:
        logger.error(f"Could not toot: {r.text}")
    else:
        logger.info(f"Tooted successfully: {status}")

    return r.status_code, r.text

if __name__ == '__main__': 
    toot()
