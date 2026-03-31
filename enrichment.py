import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        if not url.startswith("http"):
            url = "https://" + url
            
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.title.string if soup.title else ""

        meta_desc = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta:
            meta_desc = meta.get("content", "")

        text = soup.get_text()[:2000]

        return {
            "title": title,
            "meta_description": meta_desc,
            "content": text
        }

    except Exception as e:
        return {
            "title": "",
            "meta_description": "",
            "content": ""
        }