#--------------------------
# written by Sadra Avestan
# Jan 2024
#------------------------

import streamlit as st
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os

import openai
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub

from htmlTemplates import css, bot_template, user_template

# from textFunctions import get_pdf_text, get_csv_text, get_text_chunks, get_text
from textFunctions import get_text, get_text_chunks
from vizFunctions import roberta_barchat, vaders_barchart
from prompts import set_prompt


def init_ses_states():
    session_states = {
        "conversation": None,
        "chat_history": None,
        "file_analytics_enabled": False,
        "display_char_count": False,
        "display_word_count": False,
        "display_vaders": False,
        "api_authenticated": False
    }
    for state, default_value in session_states.items():
        if state not in st.session_state:
            st.session_state[state] = default_value


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(temperature="1.0", model_name="gpt-3.5-turbo")
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
    )
    return conversation_chain


def handle_userinput(user_question, prompt):
    response = st.session_state.conversation({'question': (prompt+user_question)})
    st.session_state.chat_history = response['chat_history']
    with st.spinner('Generating response...'):
        display_convo(prompt)
        

def display_convo(prompt):
    with st.container():
        for i, message in enumerate(reversed(st.session_state.chat_history)):
            if i % 2 == 0:
                st.markdown(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.markdown(user_template.replace("{{MSG}}", message.content[len(prompt):]), unsafe_allow_html=True)


def process_docs(input_docs):
    st.session_state["conversation"] = None
    st.session_state["chat_history"] = None
    st.session_state["user_question"] = ""

    # raw_text = get_files_text(input_docs)
    # raw_text = get_pdfs_text(input_docs)
    raw_text = get_text(input_docs)
    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(text_chunks)

    st.session_state.conversation = get_conversation_chain(vectorstore)
    st.session_state.file_processed = True


def pdf_analytics(input_docs):
    all_text = ""
    if st.session_state.file_analytics_enabled:
        with st.expander("PDF Analytics", expanded=False):
            for doc in input_docs:
                st.subheader(str(secure_filename(doc.name)))
                text = get_text(doc)
                all_text += text

                if st.session_state.display_word_count:
                    st.markdown(f'<p class="small-font"># of Words: {len(text.split())}</p>', unsafe_allow_html=True)

                if st.session_state.display_char_count:
                    st.markdown(f'<p class="small-font"># of Characters: {len(text)}</p>', unsafe_allow_html=True)

                if st.session_state.display_vaders:
                    vaders_barchart(text, name=str(secure_filename(doc.name)))

            if len(input_docs) > 1:
                if any([st.session_state.display_word_count, st.session_state.display_char_count, st.session_state.display_vaders]):
                    st.subheader("Collective Summary:")
                    if st.session_state.display_word_count:
                        st.markdown(f'<p class="small-font"># of Words: {len(all_text.split())}</p>', unsafe_allow_html=True)

                    if st.session_state.display_char_count:
                        st.markdown(f'<p class="small-font"># of Characters: {len(all_text)}</p>', unsafe_allow_html=True)

                    if st.session_state.display_vaders:
                        vaders_barchart(all_text, name=str(secure_filename(input_docs[-1].name)))


class OpenAIAuthenticator:
    @staticmethod
    def authenticate(api_key):
        if not api_key: return False

        os.environ['OPENAI_API_KEY'] = 'your OpenAI Key'
        try:
            llm = OpenAI()
            if llm("hi"): return True
            else: return False
        except Exception:
            return False


def api_authentication():
    if not st.session_state.api_authenticated:
        openai_key = st.text_input("OpenAI API Key:", type="password")
        if not openai_key:
            st.info("Please enter your API Key.")
            return
        authenticator = OpenAIAuthenticator()
        if authenticator.authenticate(openai_key):
            st.session_state.api_authenticated = True
        elif not authenticator.authenticate(openai_key):
            st.session_state.api_authenticated = False
        
        if st.session_state.api_authenticated:
            st.success("Authentication Successful!")
        else:
            st.error("Invalid API Key. Please try again.")
    else:
        st.success("Authentication Successful!")


def sidebar():
    global input_docs
    with st.sidebar:
        with st.expander("OpenAI API Authentication", expanded=True):
            api_authentication()
     
        with st.expander("Your Documents", expanded=True):
            input_docs = st.file_uploader("Upload your files here",
                                         type =['pdf', 'txt', 'csv', 'md'],
                                         accept_multiple_files=True,
                                         )
            if st.button("Process Files + New Chat"):
                if input_docs:
                    with st.spinner("Processing"):
                        process_docs(input_docs)
                else: 
                    st.caption("Please Upload At Least 1 PDF")
                    st.session_state.file_processed = False



def main():
    st.set_page_config(page_title="Q&A Chat Bot", page_icon=":apple:")
    st.write(css, unsafe_allow_html=True)
    global input_docs
    init_ses_states()
    st.title(":apple: ASK KROJI :banana: :banana:")
    st.subheader("Powered by the R&D AI Team")
    sidebar()
    if st.session_state.get("file_processed") and st.session_state.api_authenticated:
        prompt = set_prompt("general assistant")
        pdf_analytics(input_docs)
        with st.form("user_input_form"):
            user_question = st.text_input("Ask a question about your documents:")
            send_button = st.form_submit_button("Send")
            if send_button and user_question:
                handle_userinput(user_question, prompt)
                if not st.session_state.get("file_processed"): 
                    st.caption("Please Upload Atleast 1 PDF Before Proceeding")
                    if not st.session_state.api_authenticated:
                        st.caption("Please Authenticate OpenAI API Before Proceeding")
    


if __name__ == '__main__':
    main()

