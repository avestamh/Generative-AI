
#--------------------------
# written by Sadra Avestan
# Oct 2023
#------------------------
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader
# from langchain.agents import create_csv_agent
# from langchain_experimental.agents.agent_toolkits import create_csv_agent
import csv
import streamlit as st
import os
import glob
import csv
import codecs
# Multiple PDFs

def get_text(input_docs):
    text = ""

    for file in input_docs:

        if file.name.endswith('.pdf'):
            text += get_pdf_text(file)
        elif file.name.endswith('.csv'):
            text += get_csv_text(file)
        elif file.name.endswith('.txt'):
            text += get_txt_text(file)
        elif file.name.endswith('.md'):
            text += get_md_text(file)


        # Add more conditions for other file types if needed

    return text

# Single PDF
def get_pdf_text(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_csv_text(csv_file):
    text = ""
    decoded_csv_file = codecs.iterdecode(csv_file, 'utf-8')
    csv_reader = csv.reader(decoded_csv_file)
    for row in csv_reader:
        text += ','.join(row) + '\n'
    return text

def get_txt_text(txt_file):
    text = ""
    decoded_txt_file = codecs.iterdecode(txt_file, 'utf-8')
    for line in decoded_txt_file:
        text += line
    return text

def get_md_text(md_file):
    text = ""
    decoded_md_file = codecs.iterdecode(md_file, 'utf-8')
    for line in decoded_md_file:
        text += line
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

