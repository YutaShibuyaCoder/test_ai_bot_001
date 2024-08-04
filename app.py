import streamlit as st
import openai

# ページ設定を行い、レイアウトを調整
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets["OpenAIAPI"]["openai_api_key"]

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
    ]

# チャットボットとやりとりする関数
def communicate():
    if st.session_state.user_input and st.session_state.user_input.strip():
        user_message = st.session_state.user_input
        st.session_state.messages.append({"role": "user", "content": user_message})
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            bot_message = response.choices[0].message["content"]
            st.session_state.messages.append({"role": "assistant", "content": bot_message})
        except Exception as e:
            st.error(f"An error occurred: {e}")
        
        st.session_state.user_input = ""  # 入力欄をクリア

# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

# チャット履歴の表示
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.messages[1:]:  # システムメッセージをスキップ
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user"><span>{message["content"]}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message ai"><span>{message["content"]}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 入力欄
input_container = st.container()
with input_container:
    st.text_input("メッセージを入力してください（Enterで送信）", key="user_input", on_change=communicate)

# カスタムCSS
st.markdown("""
<style>
.stApp {
    padding-bottom: 60px;
}
.chat-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 20px;
}
[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
    height: calc(100vh - 160px);
    overflow-y: auto;
}
.stTextInput {
    position: fixed;
    bottom: 20px;
    max-width: 760px;
    width: calc(100% - 40px);
    left: 50%;
    transform: translateX(-50%);
}
.stTextInput > div > div > input {
    font-size: 16px;
    padding: 10px 15px;
    border-radius: 20px;
}
.chat-message {
    display: flex;
    margin-bottom: 10px;
}
.chat-message span {
    font-size: 16px;
    line-height: 1.4;
    display: inline-block;
    padding: 8px 12px;
    border-radius: 18px;
    max-width: 70%;
}
.chat-message.user {
    justify-content: flex-end;
}
.chat-message.ai {
    justify-content: flex-start;
}
.chat-message.user span {
    background-color: #5cb85c;
    color: white;
}
.chat-message.ai span {
    background-color: #f1f0f0;
    color: black;
}
</style>
""", unsafe_allow_html=True)
