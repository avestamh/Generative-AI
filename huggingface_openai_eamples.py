#### huggingface example.
import os
from langchain.chains import RetrievalQA ## to create a chain to retrieve relevant document and generate answers using language model
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import huggingface_hub # to use huggingface language model for generating answer or perform other nlp taks

# Step 1: seth the HuggingFace API token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# Step 2: Load the Pdf document
path = 'home/doc.pdf'
doc = PyPDFLoader(path)
pages = doc.loader()

# Step 3: Split the text into manageable chunks
text_slplitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
texts = text_slplitter.split_documents(pages) # split the pdf content into chunks

# Step 4: Generate Embedings using a huggingface model
# embedings_model = HuggingFaceBgeEmbeddings(model='sentence-transformers/all-MiniLM-L6-v2')
# embedings       = embedings_model.embed_dcouments(texts)
embedings = HuggingFaceBgeEmbeddings(model='sentence-transformers/all-MiniLM-L6-v2')

# Step 5: store embedings in FAISS
vectorstore = FAISS.from_documents(texts, embedings)
# ### we can save it. it is required for big system and for production
# vectorstore.save_local('faiss_index_constitutions')

# ## Step 6: Load the persisted vector
# persisted_vector = FAISS.load_local("faiss_index_constitutions", embedings)

## Step 6: Initialize the Hugging face language model

llm = huggingface_hub(
    huggingface_hub_api_tokens = os.environ["HUGGINGFACEHUB_API_TOKEN"],
    repo_id = 'google/flan-t5-small',  ## specify the model to use for answering
    model_kwarg = {'temperature': 0, 'max_length':64}
)

# Step 7: create a retrievalQA chain with the LLM and FAISS retriever
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore)

# Step 8: Define the query you wnat to answer
query = "what is Apache Spark?"

# Step 9: Run the query through the QA chain to get an answer
answer = qa_chain.run(query)
print(answer)
