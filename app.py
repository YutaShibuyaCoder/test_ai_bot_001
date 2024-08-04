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

# タイトルとサブタイトル
st.markdown("<div class='header'><h1>My AI Assistant</h1><p>ChatGPT APIを使ったチャットボットです。</p></div>", unsafe_allow_html=True)

# チャット履歴の表示
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages[1:]:  # システムメッセージをスキップ
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user"><div class="message-content">{message["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message ai"><div class="message-content">{message["content"]}</div></div>', unsafe_allow_html=True)

# 入力欄
input_container = st.container()
with input_container:
    st.text_input("ChatGPT にメッセージを送信する", key="user_input", on_change=communicate)

# カスタムCSS
st.markdown("""
<style>
body {
    font-family: Arial, sans-serif;
    background-color: #f0f2f5;
}
.header {
    background-color: white;
    padding: 20px;
    border-radius: 10px 10px 0 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.header h1 {
    color: #333;
    font-size: 24px;
    margin-bottom: 5px;
}
.header p {
    color: #666;
    font-size: 14px;
    margin: 0;
}
.stApp {
    padding: 20px;
}
[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
    background-color: white;
    border-radius: 0 0 10px 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    padding: 20px;
    margin-bottom: 80px;
}
.stTextInput {
    position: fixed;
    bottom: 20px;
    max-width: calc(100% - 40px);
    width: calc(100% - 40px);
    left: 20px;
}
.stTextInput > div > div > input {
    font-size: 16px;
    padding: 12px 20px;
    border-radius: 24px;
    border: 1px solid #ddd;
    background-color: #f0f2f5;
}
.chat-message {
    display: flex;
    margin-bottom: 20px;
}
.chat-message .message-content {
    font-size: 16px;
    line-height: 1.5;
    padding: 12px 16px;
    border-radius: 18px;
    max-width: 70%;
}
.chat-message.user {
    justify-content: flex-end;
}
.chat-message.user .message-content {
    background-color: #0084ff;
    color: white;
}
.chat-message.ai .message-content {
    background-color: #f0f2f5;
    color: black;
}
</style>
""", unsafe_allow_html=True)
