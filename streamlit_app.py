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
    # 会話回数が存在しない場合は0で初期化
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0

    # 背景色を設定
    colors = ['#F3FFD8', '#FFDBC9', '#FFD5EC']
    color_index = st.session_state.conversation_count // 3 % 3
    set_bg_color(colors[color_index])

    # 会話回数に応じて表示する画像を選択
    images = ["猫1.gif", "猫2.gif", "猫3.gif"]
    image_index = (st.session_state.conversation_count // 3) % 3  # 画像をループさせる

    # 会話回数が3の倍数であれば画像を表示
    if st.session_state.conversation_count % 3 == 0 and st.session_state.conversation_count > 0:
        image_path = images[image_index]
        image = Image.open(image_path)
        st.image(image, use_column_width=True)


def main_page():
    
    st.title('ATAIとの対話型鑑賞')
    st.write('<font size="5">アート思考力を高めるために対話型鑑賞しましょう。左のサイドバーからあなたが好きな絵を選んでください。好きな絵についてATAI(Art Thinking AI) と思ったこと/感じたことを話してみましょう。「この絵は明るいね」「よくわからない」など素直にどんどん書き出して会話を楽しみましょう。好きな絵についてATAI(Art Thinking AI) と思ったこと/感じたことを話してみましょう。page1~5をの絵を選択して、対話型鑑賞をやってみましょう。</font>', unsafe_allow_html=True)
    image_main = Image.open("総合.png")
    st.image(image_main, width=400)
    st.write('<font size="5">対話型鑑賞：ニューヨーク近代美術館で生まれた美術教育の新しい方法論。作品を見ながら鑑賞者と教育者で対話しながら「なぜこの絵が気になるのか？」という疑問や感想を用いて、作品の背景にあるものを考察することで、自身の思考を深める教育法です。</font>', unsafe_allow_html=True)
    

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
            st.text('質問を受け付けました！')
            conversation_history_1.append({"role": "user", "content": prompt})
             # OpenAIのAPIを直接使用
            headers = {
                'Authorization': f'Bearer {openai.api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "命令書:あなたは[対話型鑑賞の専門家]です。"},
                    {"role": "system", "content": "命令書:あなたは以下の制約条件に従って、相手に問いかけます。"},
                    {"role": "system", "content": "制約条件:あなたはリクリット・ティラバーニャ「Who's Afraid of Red, Yellow and Green?」という作品について、相手とやり取りする"},
                    {"role": "system", "content": "制約条件:あなたが1度の会話で行う質問は必ず1つずつ"},
                    {"role": "system", "content": "制約条件:あなたが一度の会話で答えられる文字数は、150字以内。"},
                    {"role": "system", "content": "制約条件:あなたが説明する時は、あなたが質問を5つ以上行った後とする。"},
                    {"role": "system", "content": "制約条件:相手が「終了」「終わります」と言ったら、あなたは「ありがとうございました」と返す。"},
                    {"role": "system", "content": "制約条件:あなたは相手との会話で[対話型鑑賞力]を評価する。相手の[対話型鑑賞力]を100点満点で点数を付ける。"},
                    {"role": "system", "content": "制約条件:講評として相手の考え方・特徴を述べる。"},
                ] + conversation_history_1
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data).json()
            
            with st.spinner("ATAIの返信を受診中..."):
                time.sleep(2)
            st.markdown('''### ATAI (Art Thinking AI)より''')
            st.info(response['choices'][0]['message']['content'])

            # 会話の回数が3の倍数であれば画像を表示するロジックをここに挿入
            if st.session_state.conversation_count % 3 == 0:
                images = ["猫1.gif", "猫2.gif", "猫3.gif"]
                image_index = (st.session_state.conversation_count // 3 - 1) % len(images)
                image_path = images[image_index]
                image = Image.open(image_path)
                st.image(image, caption="Artistic Inspiration!", use_column_width=True)

            conversation_history_1.append({"role": "assistant", "content": response['choices'][0]['message']['content']})


    
# ページ選択用のサイドバー
page_names_to_funcs = {
    "Main Page": main_page,
    "1.リクリット・ティラバーニャ「Who’s　Afraid　of　Red,　Yellow　and　Green?」": page1,
    }

selected_page = st.sidebar.radio("メニュー", ["main　page",
                                          "1.リクリット・ティラバーニャ「Who’s　Afraid　of　Red,　Yellow　and　Green?」",])
if selected_page == "main　page":
    main_page()
elif selected_page == "1.リクリット・ティラバーニャ「Who’s　Afraid　of　Red,　Yellow　and　Green?」":
    page1()
else:
    pass
