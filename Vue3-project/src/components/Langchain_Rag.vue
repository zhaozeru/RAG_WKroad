<template>
  <div class="knowledge-base-container">
    <div class="title">
      <h3> RAG(Retrieval-Augmented Generation) 基础问答：</h3>
    </div>
    <div class="content">
      <div class="description">
        <p>您可以直接点击右侧按钮对整个故居知识库进行问答；<br>也可以先在故居栏选择感兴趣的故居进行针对性问答！</p>
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
    font-size: 19px;
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
    margin-left: 280px;
    margin-top: 25px;
    font-size: 17px;
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