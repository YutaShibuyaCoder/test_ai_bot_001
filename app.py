import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets["OpenAIAPI"]["openai_api_key"]

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
    ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state.messages
    user_message = {"role": "user", "content": st.session_state.user_input}
    messages.append(user_message)
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        bot_message = response.choices[0].message["content"]
        messages.append({"role": "assistant", "content": bot_message})
    except Exception as e:
        st.error(f"An error occurred: {e}")

# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

# テキスト入力
user_input = st.text_input("メッセージを入力してください。", key="user_input")

# 送信ボタン
if st.button("送信"):
    if user_input:  # 入力が空でない場合のみ実行
        communicate()

# チャット履歴の表示
if st.session_state.messages:
    messages = st.session_state.messages
    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"] == "assistant":
            speaker = "🤖"
        st.write(speaker + ": " + message["content"])
