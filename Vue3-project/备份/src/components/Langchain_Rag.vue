<template>
  <div class="knowledge-base-container">
    <div class="title">
      <h3>LangChain RAG 基础问答：</h3>
    </div>
    <div class="content">
      <div class="description">
        <p>请先在故居栏选择感兴趣的故居，然后点击右侧按钮，打开基础问答窗口！</p>
      </div>
      <div class="button-container">
        <button @click="openKnowledgeBase" class="open-button">RAG基础问答！</button>
      </div>
    </div>
  </div>
</template>

<script setup>
  const props = defineProps({
    Langchain_name: {
      type: String,
      required: false
    }
  });

  function openKnowledgeBase() {
    const name = props.Langchain_name;
    console.log('打印名字：', name);
    const queryParams = new URLSearchParams({ name }).toString();
    const url = `https://ragwkroad-fw4up997drjwksfwlt73gm.streamlit.app/?${queryParams}`;
    window.open(url, "_blank");
  }
</script>

<style scoped>
  .knowledge-base-container {
    position: relative;
    padding: 15px;
    background-color: #f3f3f3;
    border-radius: 20px;
    height: 100%;
    box-sizing: border-box; /* 确保内边距和边框不会增加容器的高度 */
    background-color: #E3F8F8;
    opacity: 0.85;
  }

  .title {
    position: absolute;
    top: 1.2%;
    left: 1.2%;
  }

  .title h3 {
    font-size: 20px;
    margin: 0;
  }

  .content {
    position: absolute;
    top: 50%;
    left: 1%;
    right: 3%;
    transform: translateY(-50%);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .description {
    flex: 1;
    margin-left: 150px;
    margin-top: 22px;
    font-size: 17.5px;
  }

  .button-container {
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }

  .open-button {
    padding: 15px 30px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    font-size: 16px;
  }

  .open-button:hover {
    background-color: #0056b3;
  }
</style>