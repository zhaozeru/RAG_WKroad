import streamlit as st
from langchain.memory import ConversationBufferMemory
from utils import qa_agent
import openai

st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 60%;
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💬 LangChain RAG PDF问答与对话工具！")
st.divider()


if st.button("🔄 开始新对话"):
    st.session_state['user_questions'] = []
    st.session_state['memory'] = ConversationBufferMemory(return_messages=True)
    st.session_state['messages'] = [
        {"role": "ai", "content": "你好！欢迎回来，我们可以重新开始对话。"}
    ]

with st.sidebar:
    openai_api_key = st.text_input("请输入您的OpenAI API密钥：", type="password")
    st.markdown("[获取OpenAI API key](https://platform.openai.com/account/api-keys)")

    st.markdown("## 💡 功能说明")
    st.markdown(
        "通过输入问题，您可以向PDF文档提问，AI助手会基于您的PDF文档内容进行回答。  \n"
        "若回答有误请见谅。ChatGPT也可能会犯错，请核查重要信息！！🚨"
    )



    st.markdown("## 🎛️ 模型参数调节")
    temperature = st.slider("温度 (Temperature)", 0.0, 1.0, 0.1, 0.1)
    max_tokens = st.slider("最大生成长度 (Max Tokens)", 50, 500, 500, 10)
    top_p = st.slider("顶部_p (Top-p)", 0.0, 1.0, 0.9, 0.1)
    frequency_penalty = st.slider("频率惩罚 (Frequency Penalty)", 0.0, 2.0, 0.3, 0.1)
    presence_penalty = st.slider("存在惩罚 (Presence Penalty)", 0.0, 2.0, 0.3, 0.1)

    with st.expander("📜 历史问题", expanded=False):
        if st.session_state.get("user_questions"):
            for idx, question in enumerate(st.session_state["user_questions"], start=1):
                st.markdown(f"{idx}. {question}")
        else:
            st.markdown("暂无历史问题。")

name = st.query_params.get("name", "空")
if name == "":
    name = "空"


if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )
    st.session_state["messages"] = [
        {"role": "ai", "content": f"您好，我是您的AI助手，您的咨询对象为{name}，请问有什么可以帮你的吗？"}
    ]

if "user_questions" not in st.session_state:
    st.session_state["user_questions"] = []

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("✨ 请输入您咨询的问题:")





if prompt and not openai_api_key:
    st.info("请输入你的OpenAI API密钥")
    st.stop()

if prompt and openai_api_key:
    if name == "空":
        st.info("请返回上一级，选择一个故居作为咨询对象进行问答。")
        st.stop()

    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)
    st.session_state["user_questions"].append(prompt)

    with st.spinner("AI正在思考中，请稍等..."):
        response = qa_agent(
            openai_api_key,
            st.session_state["memory"],
            name,
            prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )


    st.session_state["messages"].append({"role": "ai", "content": response["answer"]})
    st.chat_message("ai").write(response["answer"])


    with st.expander("📄 查看源文档", expanded=False):
        if response["source_documents"]:
            st.write(response["source_documents"])
        else:
            st.write("暂无源文档信息。")
