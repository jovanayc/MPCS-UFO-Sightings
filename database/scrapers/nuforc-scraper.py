#!/usr/bin/env python3
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

INDEX_URL = "https://nuforc.org/subndx/?id=all"
OUT_CSV    = "nuforc_all_reports_table.csv"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; ARM64 Mac OS X 15_4) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/116.0.5845.97 Safari/537.36"
    )
}

def scrape_table(url):
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table", class_="wpDataTable")
    if not table:
        raise RuntimeError("Could not find the data table")

    rows = []
    for tr in table.find("tbody").find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) != 10:
            continue

        link = tds[0].find("a", href=True)
        detail_url = urljoin(url, link["href"]) if link else ""

        fields = [td.get_text(" ", strip=True) for td in tds[1:8]]

        media_td = tds[8]
        media_txt = media_td.get_text(" ", strip=True)
        if not media_txt:
            non_text = [
                c for c in media_td.contents
                if getattr(c, "name", None) or str(c).strip()
            ]
            media_txt = "Y" if non_text else ""
        fields.append(media_txt)

        fields.append(tds[9].get_text(" ", strip=True))

        rows.append([detail_url] + fields)

    return rows

def main():
    headers = [
        "Detail URL",
        "Occurred",
        "City",
        "State",
        "Country",
        "Shape",
        "Summary",
        "Date Reported",
        "Media",
        "Explanation",
    ]

    data = scrape_table(INDEX_URL)
    print(f"Found {len(data)} rows (page 1).")


    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"Wrote {len(data)} rows to {OUT_CSV}")

if __name__ == "__main__":
    main()