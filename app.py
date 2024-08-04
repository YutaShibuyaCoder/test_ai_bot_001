import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets["OpenAIAPI"]["openai_api_key"]

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
    ]

# チャットボットとやりとりする関数
def communicate():
    try:
        messages = st.session_state["messages"]
        user_message = {"role": "user", "content": st.session_state["user_input"]}
        messages.append(user_message)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        bot_message = response.choices[0].message["content"]
        messages.append({"role": "assistant", "content": bot_message})

        # 新しいセッションキーを使用して入力欄をリセット
        st.session_state["new_input"] = ""
        st.experimental_rerun()
    except Exception as e:
        st.error(f"An error occurred: {e}")

# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

# 新しいセッションキーを使用
user_input = st.text_input("メッセージを入力してください。", key="new_input")
if st.button("送信"):
    st.session_state["user_input"] = st.session_state["new_input"]
    communicate()

if st.session_state["messages"]:
    messages = st.session_state["messages"]
    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"] == "assistant":
            speaker = "🤖"
        st.write(speaker + ": " + message["content"])
