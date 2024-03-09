from typing import List
import yaml
from bs4 import BeautifulSoup as Soup
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from in_recursive_url_loader import INRecursiveUrlLoader


def embed_all_urls(embedding_folder="index"):
    """Read URLs from a list and index them
    """
    search_index = None
    source_chunks: List = None

    # Get all urls and create an index from them
    with open(file='url\\urls.yml', mode='r', encoding='utf-8') as file_handle:
        data = yaml.load(stream=file_handle, Loader=yaml.SafeLoader)
        include_urls: list = data['include']
        exclude_urls = data['exclude']
        for url in include_urls:
            loader = INRecursiveUrlLoader(url=url.strip(),
                                          max_depth=10,
                                          timeout=60,
                                          exclude_dirs=exclude_urls,
                                          extractor=lambda x: Soup(x, "html.parser").text)
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                           chunk_overlap=200)
            print(f'Downloaded {len(docs)} urls in url: {url.strip()}.')
            if source_chunks is None:
                source_chunks = text_splitter.split_documents(docs)
            else:
                chunks = text_splitter.split_documents(list(docs))
                for d in chunks:
                    source_chunks.append(d)

    print('Creating index')
    search_index = FAISS.from_documents(source_chunks, OpenAIEmbeddings())
    print('Saving index to file')

    search_index.save_local(
        folder_path=embedding_folder, index_name="urls.index"
    )
