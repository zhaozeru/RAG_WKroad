import streamlit as st
from utils import model_output

# 陈果夫和陈立夫什么关系？
knowledge_id_list = {
    "陈立夫旧居": "1826433526632005632",
    "颜福庆旧居": "1826433526590062592",
    "武康庭(FERGUSON LANE）": "1826433526426492928",
    "王元化故居": "1826433526317441024",
    "陈果夫旧居": "1826433526304858112",
    "莫觞清旧居": "1826433526204186624",
    "黄兴故居": "1826433526199877632",
    "马步芳故居": "1826433525998551040",
    "巴金故居": "1826433493404729344",
    "宋庆龄故居": "1826433493400420352",
    "唐绍仪旧居": "1826433493287292928",
    "张乐平故居": "1826433493203410944",
    "柯灵故居": "1826433493178236928",
    "周作民旧居": "1826433493094350848"
}

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

st.title("💬 RAG(Retrieval-Augmented Generation)")
st.markdown("## &nbsp;👉 问答与对话工具！")
st.divider()

if st.button("🔄 开始新对话"):
    try:
        st.session_state['user_questions'] = []
        st.session_state['message'] = []
        st.empty()
        st.session_state['message'] = [
            {"role": "assistant", "content": "您好！欢迎回来，我们可以重新开始对话。"}
        ]
    except Exception as e:
        st.info(f"⚠️ 发生错误：{str(e)}")

with st.sidebar:
    st.markdown("## 💡 功能说明")
    st.markdown(
        "通过输入问题，您可以向知识库文档提问，AI助手会基于文档内容进行回答。  \n  \n"
        "您可以选择对整个故居知识库进行问答，也可以返回上一级选择某个故居进行针对性问答！  \n  \n"
        "若回答有误请见谅。大模型也可能会犯错，请核查重要信息！！🚨"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("## 🎛️ 模型参数调节")
    temperature = st.slider("温度 (Temperature)", 0.0, 1.0, 0.1, 0.1)
    max_tokens = st.slider("最大生成长度 (Max Tokens)", 50, 500, 400, 10)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("📜 历史问题", expanded=False):
        if st.session_state.get("user_questions"):
            for idx, question in enumerate(st.session_state["user_questions"], start=1):
                st.markdown(f"{idx}. {question}")
        else:
            st.markdown("暂无历史问题。")

try:
    name = st.query_params.get("name", "空")
    if name == "":
        name = "故居知识库"

    if name != "空":
        knowledge_id = knowledge_id_list.get(name)
    elif name == "故居知识库":
        knowledge_id = '1826238715882885120'

    if "message" not in st.session_state:
        st.session_state["message"] = [{
            "role": "assistant", "content": f"您好，我是您的AI助手，您的咨询对象为{name}，请问有什么可以帮你的吗？"
        }]
    if "user_questions" not in st.session_state:
        st.session_state["user_questions"] = []

    for message in st.session_state["message"]:
        st.chat_message(message["role"]).write(message["content"])

except KeyError as ke:
    st.info(f"⚠️ 配置错误：{str(ke)}")
except Exception as e:
    st.info(f"⚠️ 发生错误：{str(e)}")

question = st.chat_input("✨ 请输入您咨询的问题:")

if question:
    try:
        st.session_state["user_questions"].append(question)
        st.session_state["message"].append({"role": "user", "content": question})
        st.chat_message("human").write(question)

        with st.spinner("💦 AI正在思考中，请稍等..."):
            response = model_output(
                knowledge_id=knowledge_id,
                messages=st.session_state["message"],
                temperature=temperature,
                max_tokens=max_tokens
            )

        st.session_state["message"].append(response)
        st.chat_message("assistant").write(response["content"])
    except Exception as e:
        st.info(f"⚠️ 发生错误：{str(e)}")
        st.markdown("[获取错误码文档](https://open.bigmodel.cn/dev/api#queryfile)")
