from zhipuai import ZhipuAI

def model_output(knowledge_id, messages, temperature,max_tokens):
    ZHIPU_API_KEY = "3f2fa69c13a5828f049de33d2d05cfcc.tFt8YLHcgUb8j7g4"
    client = ZhipuAI(api_key=ZHIPU_API_KEY)
    template = """
        你是一个基于给定文档并进行问答的AI助手。
        文档的内容是上海武康路上名人故居的相关数据。

        文档内容：
        {{knowledge}};
        用户提问：
        {{question}};

        先对用户提问进行判断：
        1、如果是和文档内容相关的问题，那么就请你以一个当地导游的角色，根据提供的文档内容来回答用户的问题。
        2、如果是用户的寒暄、交谈或者与文档无关，那么这就是一次聊天，你可以和用户温柔地交谈而无需借助文档内容。
        
        请注意！！
        若超出了文档内容你必须告知用户超出知识库范围或者你可以在告知后不依靠知识库进行作答。
        不要透漏你的判断逻辑，让你的回答像是一次交谈，而不是一次分析。
        """
    response = client.chat.completions.create(
        model="glm-4-air",
        messages=messages,
        tools=[
            {
                "type": "retrieval",
                "retrieval": {
                    "knowledge_id": knowledge_id,
                    "prompt_template": template
                }
            }
        ],
        stream=True,
        temperature=temperature,
        max_tokens=max_tokens
    )
    ai_resp = ''
    deltas = []
    for chunk in response:
        if chunk.choices:
            delta = chunk.choices[0].delta
            if delta:
                print(delta.content, end='', flush=True)
                deltas.append(delta.content)
    ai_resp = ''.join(deltas)
    return {"role": "assistant", "content": ai_resp}

# messages=[
#     {"role": "user", "content": '请问陈果夫和陈立夫什么关系？'}
# ]
# temperature=0.1
# knowledge_id = '1826239520555913216'
# max_tokens = 100
# res = model_output(knowledge_id, messages, temperature,max_tokens)
# print(res)