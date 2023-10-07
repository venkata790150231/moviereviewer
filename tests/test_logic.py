# from streamlit_app import do_something
import asyncio

from dotenv import load_dotenv
from langchain.document_loaders import AsyncHtmlLoader
from langchain.document_transformers import Html2TextTransformer, BeautifulSoupTransformer

from core.util import news_post_download
from core.util import download, find_selector

load_dotenv()

def do_something(x):
    return x + 5


class TestLogic:
    """Test backend logic"""

    async def demo(self, document):
        from langchain.document_transformers import DoctranTextTranslator
        qa_translator = DoctranTextTranslator(language="english")
        return asyncio.run(await qa_translator.atransform_documents(document))
    def test_something(self):
        from langchain.schema import Document
        html2text = Html2TextTransformer()
        urls = ["https://www.eenadu.net/"]
        loader = AsyncHtmlLoader(urls)
        html = loader.load()
        bs_transformer = BeautifulSoupTransformer()
        docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["a"])
        #docs_transformed = html2text.transform_documents(docs, ignore_links=True, ignore_images=True)
        print(docs_transformed[0].page_content)
