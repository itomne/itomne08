import os
import time
import openai
import requests
import streamlit as st
from PIL import Image

# APIキーの設定
openai.api_key = os.environ.get("OPENAI_API_KEY")

# 会話履歴保存場所
conversation_history_1 = []

def set_bg_color(color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def update_bg_and_show_image():
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0

    colors = ['#F3FFD8', '#FFDBC9', '#FFD5EC']
    color_index = st.session_state.conversation_count // 3 % 3
    set_bg_color(colors[color_index])

    if st.session_state.conversation_count % 3 == 0 and st.session_state.conversation_count > 0:
        image = Image.open("おぱんちゅうさぎ.jpg")
        st.image(image, use_column_width=True)

def page1():
    prompt = ""
    st.title("リクリット・ティラバーニャ「Who's Afraid of Red, Yellow and Green?」")
    st.write('<font size="5">好きな絵についてATAI(Art Thinking AI) と思ったこと/感じたことを話してみましょう。「この絵は明るいね」「よくわからない」など素直にどんどん書き出して会話を楽しみましょう。</font>', unsafe_allow_html=True)
    image_1 = Image.open("11.リクリット・ティラバーニャ「“Who’s Afraid of Red, Yellow and Green,」.jpg")
    st.image(image_1, width=400)

    with st.form('question_form', clear_on_submit=False):
        st.markdown('### 話しかけてみよう!')
        prompt = st.text_area('テキストエリア')
        submitted = st.form_submit_button("送信")

        if submitted:
            if 'conversation_count' not in st.session_state:
                st.session_state.conversation_count = 0
            st.session_state.conversation_count += 1

            update_bg_and_show_image()
            st.text('質問を受け付けました！')
            conversation_history_1.append({"role": "user", "content": prompt})
            
            headers = {
                'Authorization': f'Bearer {openai.api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "あなたは対話型鑑賞の専門家です。"},
                    {"role": "user", "content": prompt}
                ] + conversation_history_1
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data).json()
            
            with st.spinner("ATAIの返信を受診中..."):
                time.sleep(2)
            st.markdown('''### ATAI (Art Thinking AI)より''')
            st.info(response['choices'][0]['message']['content'])

            # 会話の回数が3の倍数であれば画像を表示
            if st.session_state.conversation_count % 3 == 0:
                image_path = "おぱんちゅうさぎ.jpg"
                image = Image.open(image_path)
                st.image(image, caption="Artistic Inspiration!", use_column_width=True)

            conversation_history_1.append({"role": "assistant", "content": response['choices'][0]['message']['content']})

    
page_names_to_funcs = {
    "Main Page": main_page,
    "1.リクリット・ティラバーニャ「Who’s　Afraid　of　Red,　Yellow　and　Green?」": page1,
    }

selected_page = st.sidebar.radio("メニュー", ["Main　page",
                                          "1.リクリット・ティラバーニャ「Who’s　Afraid　of　Red,　Yellow　and　Green?」",
                                         ])
if selected_page == "Main　page":
    main_page()
elif selected_page == "1.リクリット・ティラバーニャ「Who’s　Afraid　of　Red,　Yellow　and　Green?」":
    page1()
else:
    pass
