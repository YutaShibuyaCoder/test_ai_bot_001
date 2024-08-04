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

# メッセージを表示する関数
def display_message(role, content):
    if role == "user":
        st.markdown(f'<div class="chat-message user"><div class="message-content">{content}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message ai"><div class="message-content">{content}</div></div>', unsafe_allow_html=True)

# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

# チャット履歴の表示
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages[1:]:  # システムメッセージをスキップ
        display_message(message["role"], message["content"])

# 入力欄
input_container = st.container()
with input_container:
    st.text_input("メッセージを入力してください（Enterで送信）", key="user_input", on_change=communicate)

# カスタムCSS
st.markdown("""
<style>
.stApp {
    padding-bottom: 80px;
}
[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
    height: calc(100vh - 180px);
    overflow-y: auto;
}
.stTextInput {
    position: fixed;
    bottom: 20px;
    width: calc(100% - 40px);
    left: 20px;
}
.stTextInput > div > div > input {
    font-size: 16px;
    padding: 10px 15px;
    border-radius: 20px;
}
.chat-message {
    padding: 1.5rem; 
    border-radius: 0.5rem; 
    margin-bottom: 1rem; 
    display: flex;
    flex-direction: column;
}
.chat-message.user {
    background-color: #2b313e;
    align-items: flex-end;
}
.chat-message.ai {
    background-color: #475063;
    align-items: flex-start;
}
.chat-message .message-content {
    max-width: 80%;
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
}
.chat-message.user .message-content {
    background-color: #2196f3;
    color: white;
}
.chat-message.ai .message-content {
    background-color: #ffffff;
    color: black;
}
</style>
""", unsafe_allow_html=True)
