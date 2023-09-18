import streamlit as st
import os
import time
# Split text
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Vectorstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import pickle
import tempfile
# Chatbot
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


# API Key
# import constant
# openai_api_key = constant.APIKEY

#################################################################################

st.title("AI Analyst: Chat with your PDF")

# Introduction
st.markdown('''
#### Introduction:
Welcome to the **:red[AI Analyst: Chat with your PDF]**. The AI can help 
answer your questions **:red[based on the provided PDF file]** by following the guidelines below:

1. Upload a PDF file.
2. Ask any question about the PDF file after loading.
3. Answer **:red[based on the PDF file]** will be displayed.
4. The answers will depend on the **:red[previous chat history.]**
''')
st.divider()

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.sidebar:
    st.markdown('''
    # About the AI Analyst:
    The objective of this app is to provide assistance in **answering questions according to the provided PDF file and analyzing CSV data.** 
    This application consists of two main functions:

    **1. Chat with your PDF**
    
    **2. EDA by Automatic Visualization**

    AI Analyst is written by **Isaac Mak**. 
    - [LinkedIn](https://www.linkedin.com/in/isaac-ccmak/)
    - [Source Code](https://github.com/ccmak514/ai-analyst)
    - [GitHub](https://github.com/ccmak514)
    ''')
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    st.title("Upload a PDF File")
    pdf_file = st.file_uploader(" ", type=['pdf'])

#################################################################################


def load_vectorstore(pdf_file):
    if pdf_file:
        # Get the name of the pdf and check if the vectorstore already exists
        storename = pdf_file.name[:-4]
        # Load the vectorstore if it exists
        if os.path.exists(f"{storename}.pkl"):
            with open(f"{storename}.pkl", "rb") as f:
                vectorstore = pickle.load(f)
        # Create the vectorstore
        else:
            # Create temporary file for loading
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                # Write the pdf_file into the temp_file
                temp_file.write(pdf_file.read())
                # Get the path of the temp_file
                temp_file_path = temp_file.name
            # Load and split the temp_file into chunks
            loader = PyPDFLoader(temp_file_path)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=150)
            chunks = text_splitter.split_documents(documents)
            # Create the vectorstore by embeddings and FAISS
            embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
            vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
            # save the vectorstore in pickle with the name of the pdf_file
            with open(f"{storename}.pkl", "wb") as f:
                pickle.dump(vectorstore, f)
            # Remove the temp_file
            os.remove(temp_file_path)
        return vectorstore


def chain(prompt, vectorstore):
    llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    # Access the previous messages from the session state
    for message in st.session_state['messages']:
        if message["role"] == "user":
            memory.chat_memory.add_user_message(message["content"])
        else:
            memory.chat_memory.add_ai_message(message["content"])
    retriever = vectorstore.as_retriever()
    qa = ConversationalRetrievalChain.from_llm(
        llm, chain_type='stuff', retriever=retriever, memory=memory)
    return qa(prompt)['answer']


def main():
    if prompt := st.chat_input("Please enter your question..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        response = chain(prompt, vectorstore)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for word in response.split():
                full_response += word + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": response})


##############################################################################


if __name__ == "__main__":
    vectorstore = load_vectorstore(pdf_file)
    main()
