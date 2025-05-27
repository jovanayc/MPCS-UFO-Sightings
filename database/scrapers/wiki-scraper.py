import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

WIKI_URL = "https://en.wikipedia.org/wiki/List_of_reported_UFO_sightings"
OUT_CSV  = "wiki_sightings.csv"

def build_reference_map(soup):
    ref_map = {}
    for li in soup.find_all("li", id=re.compile(r"cite_note-")):
        anchor_id = li["id"]
        externals = [
            a["href"] for a in li.find_all("a", href=True)
            if a["href"].startswith("http")
        ]
        if externals:
            ref_map[anchor_id] = externals
    return ref_map

def parse_wikitable(tbl, page_url, ref_map):
    header_cells = tbl.find("tr").find_all(["th","td"])
    cols = [cell.get_text(strip=True) for cell in header_cells]
    headers = ["Detail URL"] + cols + ["Citation Links"]

    rows = []
    for tr in tbl.find_all("tr")[1:]:
        tds = tr.find_all("td")
        if len(tds) != len(header_cells):
            continue

        detail_a   = tr.find("a", string="Open !")
        detail_url = urljoin(page_url, detail_a["href"]) if detail_a else ""

        cite_ids = [
            a["href"].lstrip("#")
            for sup in tr.find_all("sup", class_="reference")
            for a in sup.find_all("a", href=True)
            if a["href"].startswith("#")
        ]

        external = []
        for cid in cite_ids:
            external += ref_map.get(cid, [])
        citation_cell = ";".join(external)

        for sup in tr.find_all("sup", class_="reference"):
            sup.decompose()

        texts = [td.get_text(" ", strip=True) for td in tds]
        rows.append([detail_url] + texts + [citation_cell])

    return headers, rows

def main():
    resp = requests.get(WIKI_URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # build reference map
    ref_map = build_reference_map(soup)

    # scrape wikitables
    all_rows = []
    headers  = None
    for tbl in soup.find_all("table", class_="wikitable"):
        hdrs, rows = parse_wikitable(tbl, WIKI_URL, ref_map)
        if headers is None:
            headers = hdrs
        all_rows.extend(rows)

    # put in pandas
    df = pd.DataFrame(all_rows, columns=headers)

    # split citation links into 4 columnts
    cit_df = (
        df
        .pop("Citation Links")
        .str.split(";", n=3, expand=True)   # n=3 -> max 4 pieces
        .fillna("")
    )
    cit_df.columns = ["Citation_1", "Citation_2", "Citation_3", "Citation_4"]
    df = pd.concat([df, cit_df], axis=1)
    df.drop(columns=["Detail URL"], inplace=True)

   
    df.to_csv(OUT_CSV, index=False, encoding="utf-8")
    print(f"Wrote {len(df)} rows to {OUT_CSV}")

if __name__ == "__main__":
    main()