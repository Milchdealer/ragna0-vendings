"""
    Scrape ragna0 vendings
"""
import logging
import os
from typing import Iterator

import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import Base, Vending, VendingEntry

SQLITE_DB = os.getenv("RAGNA0_SQLITE_PATH", "/data/ragna0.db")
BASE_URL = "https://www.ragna0.com/vending"
VENDING_URL_FORMAT = BASE_URL + "/?p={page_num}"

def get_page_count(html: str) -> int:
    """ Parses the main page and tries to find the page count. """
    soup = BeautifulSoup(html, "html.parser")
    pages = soup.find("div", class_="pages")

    if not pages:
        raise ValueError("No pages container found!")

    logging.debug("Materialize pages iterator")
    pages = pages.find_all("a", class_="page-num")
    pages = [p for p in pages]

    return int(pages[-1].encode_contents())

def vending_page_scraper(page_num: int, sql_session):
    """ Threaded function which scrapes a vending page. """
    url = VENDING_URL_FORMAT.format(page_num=page_num)
    r = requests.get(url)
    if r.status_code != 200:
        logging.error("Failed to retrieve %s: %s", url, r.status_code)
        raise ValueError("Failed to retrieve %s" % url)

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", class_="horizontal-table")
    table = table.find("tbody")
    rows = table.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        columns = [c for c in columns]
        v_id, v_name, title, m, x, y, gender = columns
        v_id = v_id.find("a")

        vending = Vending(
            v_id=v_id.decode_contents(),
            v_name=v_name.decode_contents().strip(),
            title=title.find("a").decode_contents().strip(),
            m=m.decode_contents().strip(),
            x=x.decode_contents(),
            y=y.decode_contents(),
            gender=gender.decode_contents().strip(),
        )
        sql_session.add(vending)
        sql_session.commit()
        for entry in vending_entry_scraper(vending.id, v_id["href"]):
            sql_session.add(entry)
        sql_session.commit()


def vending_entry_scraper(vending_id: int, url: str) -> Iterator[VendingEntry]:
    """ Scrapes all the entries for a vending. """
    r = requests.get("https://www.ragna0.com" + url)
    if r.status_code != 200:
        logging.error("Failed to retrieve %s: %s", url, r.status_code)
        return

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", class_="horizontal-table")
    table = table.find("tbody")
    rows = table.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        columns = [c for c in columns]
        (
            item_id,
            name,
            refine,
            slot,
            card0,
            card1,
            card2,
            card3,
            option0,
            option1,
            option2,
            option3,
            option4,
            price,
            amount
        ) = columns

        # Refine
        refine = refine.find("strong")
        if refine:
            refine = refine.decode_contents().strip()
        # Slots
        slot = slot.decode_contents().strip().lstrip("[").rstrip("]")
        # Cards
        exists = card0.find("a")
        if exists:
            card0 = card0.find("a").decode_contents().strip()
        else:
            card0 = None
        exists = card1.find("a")
        if exists:
            card1 = card1.find("a").decode_contents().strip()
        else:
            card1 = None
        exists = card2.find("a")
        if exists:
            card2 = card2.find("a").decode_contents().strip()
        else:
            card2 = None
        exists = card3.find("a")
        if exists:
            card3 = card3.find("a").decode_contents().strip()
        else:
            card3 = None
        # Options
        exists = option0.find("strong")
        if exists:
            option0 = option0.find("strong").find("a").decode_contents().strip()
        else:
            option0 = None
        exists = option1.find("strong")
        if exists:
            option1 = option1.find("strong").find("a").decode_contents().strip()
        else:
            option1 = None
        exists = option2.find("strong")
        if exists:
            option2 = option2.find("strong").find("a").decode_contents().strip()
        else:
            option2 = None
        exists = option3.find("strong")
        if exists:
            option3 = option3.find("strong").find("a").decode_contents().strip()
        else:
            option3 = None
        exists = option4.find("strong")
        if exists:
            option4 = option4.find("strong").find("a").decode_contents().strip()
        else:
            option4 = None
        # Price
        price = price.decode_contents().replace("z", "").replace(" ", "").strip()

        v_entry = VendingEntry(
            vending_id=vending_id,
            item_id=item_id.find("a").decode_contents(),
            name=name.find("a").decode_contents(),
            refine=refine,
            slot=slot,
            card0=card0,
            card1=card1,
            card2=card2,
            card3=card3,
            option0=option0,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            price=price,
            amount=amount.decode_contents(),
        )
        yield v_entry

if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    engine = create_engine('sqlite:///%s' % SQLITE_DB)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    
    r = requests.get(BASE_URL)
    if r.status_code != 200:
        logging.error("Failed to retrieve %s", BASE_URL)
        exit(1)

    page_count = get_page_count(r.text)
    logging.info("Pages Count: %s", page_count)

    for page in range(page_count):
        logging.info("Scraping page %s", page + 1)
        vending_page_scraper(page + 1, Session())
