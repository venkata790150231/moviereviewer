from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

selector_dict = {
    "gulte": ".entry",
    "greatandhra": ".great_andhra_main_body_container .page_news .unselectable",
    "m9": ".main-content.single-page-content",
    "123telugu": ".post-content",
    "sakshi": ".fullstory .offset-tb1",
    "eenadu": ".fullstory .text-justify",
    "prajasakti": ".body .text-align-justify",
    "vaartha": ".article-content .entry-content",
    "andhrajyothy": ".category_desc",
    "telugubulletin": ".tdc-zone .tdb_single_content",
}


def find_selector(url) -> str:
    # Parse the URL
    parsed_url = urlparse(url)

    # Get the domain name
    domain_name = parsed_url.netloc

    # Split the domain name by periods (.)
    parts = domain_name.split(".")

    # Check if there's a subdomain (www)
    if len(parts) > 2:
        website_name = parts[1]
    else:
        website_name = parts[0]
    return selector_dict[website_name]


def movie_review_download(url: str) -> str:
    return download(url, find_selector(url))


def news_post_download(url: str) -> str:
    return download(url, find_selector(url))


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"


def download(url: str, selector: str) -> str:
    headers = {
        "User-Agent": USER_AGENT
    }
    response = requests.get(url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the element containing the movie review (You may need to inspect the page's HTML to identify the
        # appropriate element)
        review_element = soup.select_one(selector)

        if review_element:
            # Extract and print the movie review text
            return review_element.get_text()
        else:
            return ""
    else:
        raise Exception(
            f"Failed to download review from url: {url} code: {response.status_code}"
        )

# Create a new user and add it to the database
