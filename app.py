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
    for message in st.session_state.messages[1:]:  # システムメッセージをスキップ
        if message["role"] == "user":
            st.write("You: " + message["content"])
        else:
            st.write("AI: " + message["content"])

# 入力欄と送信ボタンを画面最下部に固定
input_container = st.container()
with input_container:
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)
    with col2:
        st.button("送信", on_click=communicate)

# カスタムCSS
st.markdown("""
<style>
.stApp {
    padding-bottom: 100px;
}
[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
    height: calc(100vh - 200px);
    overflow-y: auto;
}
.stTextInput, .stButton {
    position: fixed;
    bottom: 20px;
}
.stTextInput {
    width: calc(80% - 20px);
    left: 20px;
}
.stButton {
    width: 20%;
    right: 20px;
}
</style>
""", unsafe_allow_html=True)
