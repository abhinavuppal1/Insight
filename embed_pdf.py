import os
from langchain_community.document_loaders import PagedPDFSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


def embed_document(file_name, file_folder="pdf", embedding_folder="index"):
    file_path = f"{file_folder}/{file_name}"
    loader = PagedPDFSplitter(file_path)
    source_pages = loader.load_and_split()
    with open(file=f'{file_name}.txt', mode='w', encoding='utf-8') as file_handle:
        for page in source_pages:
            file_handle.write(f'{os.linesep} ----------------------------------- {os.linesep}')
            file_handle.write(f'Page Num: {page.metadata["page"]}{os.linesep}')
            file_handle.write(page.page_content)

    embedding_func = OpenAIEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
        separators=["\n\n", "\n", " ", ""],
    )
    source_chunks = text_splitter.split_documents(source_pages)
    search_index = FAISS.from_documents(source_chunks, embedding_func)
    search_index.save_local(
        folder_path=embedding_folder, index_name=file_name + ".index"
    )


def embed_all_pdf_docs():
    # Define the directory path
    pdf_directory = "pdf"

    # Check if the directory exists
    if os.path.exists(pdf_directory):
        # List all PDF files in the directory
        pdf_files = [
            file for file in os.listdir(pdf_directory) if file.endswith(".pdf")
        ]

        if pdf_files:
            for pdf_file in pdf_files:
                print(f"Embedding {pdf_file}...")
                embed_document(file_name=pdf_file, file_folder=pdf_directory)
                print("Done!")
        else:
            raise Exception("No PDF files found in the directory.")
    else:
        raise Exception(f"Directory '{pdf_directory}' does not exist.")


def get_all_index_files() -> list:
    # Define the directory path
    index_directory = "index"

    # Check if the directory exists
    if os.path.exists(index_directory):
        postfix = ".index.faiss"
        index_files = [
            file.replace(postfix, "")
            for file in os.listdir(index_directory)
            if file.endswith(postfix)
        ]

        if index_files:
            return index_files
        else:
            print("No index files found in the directory.")
            return None
    else:
        raise Exception(f"Directory '{index_directory}' does not exist.")
