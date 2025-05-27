#!/usr/bin/env python3
import re
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

LIST_URL  = "https://nuforc.org/ndx/?id=post"
BASE_URL  = "https://nuforc.org"
OUT_CSV   = "nuforc_scraped.csv"
MAX_ROWS  = 1000 # row limit
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; ARM64 Mac OS X 15_4) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/116.0.5845.97 Safari/537.36"
    )
}

def get_monthly_urls():
    resp = requests.get(LIST_URL, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    urls = {
        urljoin(BASE_URL, a["href"])
        for a in soup.find_all("a", href=True)
        if a["href"].startswith("/subndx/?id=p") and re.search(r"p\d{6}$", a["href"])
    }
    return sorted(urls, reverse=True)  # newest first

def parse_page(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    rows = []

    table = soup.find("table", class_="wpDataTable")
    if table:
        for tr in table.find("tbody").find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) != 10:
                continue
            link = tds[0].find("a", href=True)
            detail = urljoin(page_url, link["href"]) if link else ""
            fields = [td.get_text(" ", strip=True) for td in tds[1:8]]
            media_txt = tds[8].get_text(" ", strip=True)
            if not media_txt and tds[8].contents:
                media_txt = "Y"
            fields.append(media_txt)
            fields.append(tds[9].get_text(" ", strip=True))
            rows.append([detail] + fields)
        return rows

    pre = soup.find("pre")
    if pre:
        for a in pre.find_all("a", href=re.compile(r"^/sighting/\?id=")):
            if not a.get_text(strip=True).startswith("Open"):
                continue
            detail = urljoin(page_url, a["href"])
            raw = a.next_sibling or ""
            line = raw.strip()
            cols = re.split(r"\s{2,}", line, maxsplit=8)
            if len(cols) < 9:
                cols += [""] * (9 - len(cols))
            rows.append([detail] + cols)
    return rows

def main():
    months = get_monthly_urls()
    header = [
        "Detail URL","Occurred","City","State",
        "Country","Shape","Summary","Date Reported","Media","Explanation"
    ]

    total = 0
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)

        for idx, url in enumerate(months, 1):
            print(f"[{idx}/{len(months)}] Fetching {url}")
            resp = requests.get(url, headers=HEADERS)
            resp.raise_for_status()
            page_rows = parse_page(resp.text, url)

            for row in page_rows:
                w.writerow(row)
                total += 1
            #     if total >= MAX_ROWS:
            #         print(f"Reached {MAX_ROWS} rows stopping test.")
            #         return
            # if idx > 20:
            #     break

    print(f"Wrote {total} rows to {OUT_CSV}")

if __name__ == "__main__":
    main()