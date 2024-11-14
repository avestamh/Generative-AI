
#--------------------------
# written by Sadra Avestan
# Jan 2024
#------------------------

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import openai
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

# load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_DEPLOYMENT_ENDPOINT = os.getenv("OPENAI_DEPLOYMENT_ENDPOINT")
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
OPENAI_DEPLOYMENT_VERSION = os.getenv("OPENAI_DEPLOYMENT_VERSION")

OPENAI_ADA_EMBEDDING_DEPLOYMENT_NAME = os.getenv("OPENAI_ADA_EMBEDDING_DEPLOYMENT_NAME")
OPENAI_ADA_EMBEDDING_MODEL_NAME = os.getenv("OPENAI_ADA_EMBEDDING_MODEL_NAME")

# Initialize Flask app
app = Flask(__name__)

# Configure OpenAI API
openai.api_type = "azure"
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_version = os.getenv('OPENAI_API_VERSION')
llm = AzureChatOpenAI(deployment_name=OPENAI_DEPLOYMENT_NAME,
                      model_name=OPENAI_MODEL_NAME,
                      azure_endpoint=OPENAI_DEPLOYMENT_ENDPOINT,
                      #openai_api_version=OPENAI_DEPLOYMENT_VERSION,
                      openai_api_version="2023-05-15",
                      openai_api_key=OPENAI_API_KEY,
                      openai_api_type="azure")

embeddings = AzureOpenAIEmbeddings(deployment=OPENAI_ADA_EMBEDDING_DEPLOYMENT_NAME,
                                   model=OPENAI_ADA_EMBEDDING_MODEL_NAME,
                                   azure_endpoint=OPENAI_DEPLOYMENT_ENDPOINT,
                                   openai_api_type="azure",
                                   chunk_size=512)

# Initialize gpt-35-turbo and our embedding model
# load the faiss vector store we saved into memory
vectorStore = FAISS.load_local("./dbs/docs/faiss_index", embeddings)

# use the faiss vector store we saved to search the local document
retriever = vectorStore.as_retriever(search_type="similarity", search_kwargs={"k": 2})

QUESTION_PROMPT = PromptTemplate.from_template("""Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:""")

qa = ConversationalRetrievalChain.from_llm(llm=llm,
                                           retriever=retriever,
                                           condense_question_prompt=QUESTION_PROMPT,
                                           return_source_documents=True,
                                           verbose=False)

chat_history = []

@app.route('/ask', methods=['POST'])
def ask_question_api():
    data = request.get_json()
    question = data.get('question')
    chat_history = data.get('chat_history', [])
    result = ask_question(qa, question, chat_history)
    return jsonify(result)

def ask_question(qa, question, chat_history):
    response = qa({"question": question, "chat_history": chat_history})
    print("Question:", question)
    print("Response:", response)
    answer = response.get("answer")
    if answer:
        print("Answer:", answer)
        chat_history.append((question, answer))
        return {"question": question, "answer": answer}
    else:
        print("Failed to retrieve answer from response:", response)
        return {"error": "Failed to retrieve answer"}

if __name__ == "__main__":
    app.run(debug=True)
