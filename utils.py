from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import streamlit as st
from langchain.prompts import PromptTemplate


def qa_agent(openai_api_key,memory, name, question, temperature, max_tokens, top_p, frequency_penalty, presence_penalty):
    pdf_path = f"{name}.pdf"

    if not os.path.exists(pdf_path):
        return {"answer": "找不到对应的文件。", "chat_history": memory}

    if "db" not in st.session_state:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=[",","\n","。","，",""]
        )
        texts = text_splitter.split_documents(docs)

        embeddings_model = OpenAIEmbeddings(openai_api_key=openai_api_key,openai_api_base="https://api.aigc369.com/v1")
        db = FAISS.from_documents(texts, embeddings_model)
        st.session_state["db"] = db


    db = st.session_state["db"]
    retriever = db.as_retriever(search_kwargs={"k": 2})


    relevant_docs = retriever.get_relevant_documents(question)
    context = " ".join([doc.page_content for doc in relevant_docs])
    prompt_template = PromptTemplate(
        template="""
        你是一个基于给定文档并进行问答的AI助手。
        文档的内容是上海武康路上名人故居的相关数据。
       
        文档内容：
        {context};
        用户提问：
        {question}

        先对用户提问进行判断：
        1、如果是和文档内容相关的问题，那么就请你以一个当地导游的角色，根据提供的文档内容来回答用户的问题。
        当然，若超出了文档内容你可以告知用户超出知识库范围无法作答或者你可以不依靠知识库进行作答；
        2、如果是用户的寒暄、交谈或者与文档无关，那么这就是一次聊天，你可以和用户温柔地交谈而无需借助文档内容。

        """,
        input_variables=["context", "question"]
    )



    final_prompt = prompt_template.format(context=context, question=question)

    model = ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_key=openai_api_key,
        openai_api_base="https://api.aigc369.com/v1",
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )


    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory,
        return_source_documents=True
    )

    response = qa.invoke({"chat_history": memory, "question": final_prompt})

    source_documents = response.get("source_documents", [])
    source_text = "\n\n".join([doc.page_content for doc in source_documents[:1]])

    return {
        "answer": response["answer"],
        "source_documents": source_text,
        "chat_history": memory
    }