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

# チャット履歴の表示領域
chat_container = st.container()

# 入力欄と送信ボタンを画面最下部に固定
input_container = st.container()

# チャット履歴の表示
with chat_container:
    for message in st.session_state.messages[1:]:  # システムメッセージをスキップ
        if message["role"] == "user":
            st.text_area("You:", value=message["content"], height=50, disabled=True)
        else:
            st.text_area("AI:", value=message["content"], height=50, disabled=True)

# 入力欄と送信ボタン
with input_container:
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("メッセージを入力してください。", key="user_input")
    with col2:
        if st.button("送信"):
            if user_input:  # 入力が空でない場合のみ実行
                communicate()
                st.experimental_rerun()  # チャット履歴を即時更新

# カスタムCSS
st.markdown("""
<style>
.stApp [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
    height: calc(100vh - 200px);
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

# 最新のメッセージが見えるようにスクロール
st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
