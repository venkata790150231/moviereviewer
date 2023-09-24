import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

from core.util import news_post_download

st.set_page_config(page_title="Translate Telugu News")
st.sidebar.header("News Translator")
my_form = st.form(key='form')
input = my_form.text_input('URL', key='url', placeholder="https://www.eenadu.net/telugu-news/india/sudha-murty-files-complaint-over-misuse-of-her-name-for-event-promotion-in-us/0700/123177262")
submit = my_form.form_submit_button(label='Submit')


def get_data():
    # Make an asynchronous call to an API or database
    result = news_post_download(input)
    print(result)
    chat = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k-0613")
    response_schemas = [
        ResponseSchema(name="post", description="new york times style news article"),
        ResponseSchema(name="title", description="title of news article")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    template = """
       Your reporter assisting to write news article complete below tasks
       1. Translate text in backticks to english
       2. Rewrite translated text in new york times tone with less than 200 words
       3. Suggest Huffington Post style headline for the article
       {format_instructions}
       ```{docs}```
       """
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(template)],
        input_variables=["docs"],
        partial_variables={"format_instructions": format_instructions}
    )

    _input = prompt.format_prompt(docs=result)
    output = chat(_input.to_messages())
    result = output_parser.parse(output.content)
    # Return the data
    return result


if submit:
    result = get_data()
    st.header(result["title"])
    st.write(result["post"])
