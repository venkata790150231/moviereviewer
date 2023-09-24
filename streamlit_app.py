from urllib.parse import urlparse

import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

selector_dict = {
    "gulte": ".entry",
    "greatandhra": ".great_andhra_main_body_container .page_news .unselectable",
    "m9": ".main-content.single-page-content",
    "123telugu": ".post-content",
    "telugubulletin": ".tdc-zone .tdb_single_content"
}
def find_selector(url) -> str:
    # Parse the URL
    parsed_url = urlparse(url)

    # Get the domain name
    domain_name = parsed_url.netloc

    # Split the domain name by periods (.)
    parts = domain_name.split('.')

    # Check if there's a subdomain (www)
    if len(parts) > 2:
        website_name = parts[1]
    else:
        website_name = parts[0]
    return selector_dict[website_name]


def download(url: str) -> str:
    response = requests.get(url)
    print(response.status_code)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the element containing the movie review (You may need to inspect the page's HTML to identify the appropriate element)
        selector = find_selector(url)
        print(selector)
        review_element = soup.select_one(selector)

        if review_element:
            # Extract and print the movie review text
            return review_element.get_text()
        else:
            return ""
    else:
        return ""

num_rows = st.slider('Number of rows', min_value=1, max_value=10)
my_form = st.form(key='form')
grid = my_form.columns(2)

# Function to create a row of widgets (with row number input to assure unique keys)
def add_row(row):
    with grid[0]:
        my_form.text_input('URL', key=f'url{row}')

# Loop to create rows of input widgets
for r in range(num_rows):
    add_row(r)

# Defining submit button
submit_button = my_form.form_submit_button(label='Submit')
if submit_button:
    st.write(st.session_state)
    prompt = ["""
            Can you give me a Chris Stuckmann-style review from various sources in at most 200 words:
            """]
    dict = {}
    print(st.session_state)
    for r in range(num_rows):
        url = st.session_state[f'url{r}']
        if url:
            print(url)
            review = download(url)
            dict[f"review{r+1}"] = review
            prompt.append(f"{r+1}. {{review{r+1}}}")
            st.header(url)
            st.write(review)
    #
    prompt_template = ChatPromptTemplate.from_template("\n".join(prompt))
    openai_api_key = "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"
    chat = ChatOpenAI(temperature=0.0)
    prompt = prompt_template.format_messages(**dict)
    customer_response = chat(prompt)
    if customer_response.content:
        st.header("Summarized Review")
        st.write(customer_response.content)