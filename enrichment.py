import requests
from bs4 import BeautifulSoup
from functools import lru_cache


@lru_cache(maxsize=200)
def scrape_website(url):
    try:
        if not url.startswith("http"):
            url = "https://" + url

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        res = requests.get(url, timeout=4, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.title.string.strip() if soup.title else ""

        meta_desc = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta:
            meta_desc = meta.get("content", "").strip()

        text = soup.get_text(" ", strip=True)[:500]

        return {
            "title": title,
            "meta_description": meta_desc,
            "content": text
        }

    except Exception:
        return {
            "title": "",
            "meta_description": "",
            "content": ""
        }
