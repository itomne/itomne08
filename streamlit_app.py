import os
import time
import openai
import requests
import streamlit as st

from PIL import Image


# APIキーの設定
# 設定したAPIキーの読み込み
openai.api_key = os.environ.get("OPENAI_API_KEY")


#会話履歴保存場所
conversation_history_1 = []  # Global scopes
conversation_history_2 = []  # Global scope
conversation_history_3 = []  # Global scope
conversation_history_4 = []  # Global scope
conversation_history_5 = []  # Global scope

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
# 会話履歴と背景色を更新する関数の定義
def update_bg_and_show_image():
    # 会話回数を追跡
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0

    # 会話回数に応じて背景色を更新
    colors = ['#F3FFD8', '#FFDBC9', '#FFD5EC']
    color_index = st.session_state.conversation_count // 3 % 3
    set_bg_color(colors[color_index])

    # 会話回数が3の倍数の場合、画像を表示
    if st.session_state.conversation_count % 3 == 0 and st.session_state.conversation_count > 0:
        image = Image.open("th_shiba_waai.webp")
        st.image(image, caption="Artistic Inspiration!", use_column_width=True)

# 提出ボタンが押された場合の処理に追加
if submitted:
    st.session_state.conversation_count += 1
    update_bg_and_show_image()

def update_bg_color():
    # アプリの開始時に背景色を更新
    update_bg_color()

def main_page():
    
    st.title('ATAIとの対話型鑑賞')
    st.write('<font size="5">アート思考力を高めるために対話型鑑賞しましょう。左のサイドバーからあなたが好きな絵を選んでください。好きな絵についてATAI(Art Thinking AI) と思ったこと/感じたことを話してみましょう。「この絵は明るいね」「よくわからない」など素直にどんどん書き出して会話を楽しみましょう。好きな絵についてATAI(Art Thinking AI) と思ったこと/感じたことを話してみましょう。page1~5をの絵を選択して、対話型鑑賞をやってみましょう。</font>', unsafe_allow_html=True)
    image_main = Image.open("総合.png")
    st.image(image_main, width=400)
    st.write('<font size="5">対話型鑑賞：ニューヨーク近代美術館で生まれた美術教育の新しい方法論。作品を見ながら鑑賞者と教育者で対話しながら「なぜこの絵が気になるのか？」という疑問や感想を用いて、作品の背景にあるものを考察することで、自身の思考を深める教育法です。</font>', unsafe_allow_html=True)
    


def page1():
    prompt = ""  # Initialize your prompt

    st.title("リクリット・ティラバーニャ「Who's Afraid of Red, Yellow and Green?」")
    st.write('<font size="5">好きな絵についてATAI(Art Thinking AI)  と思ったこと/感じたことを話してみましょう。「この絵は明るいね」「よくわからない」など素直にどんどん書き出して会話を楽しみましょう。</font>', unsafe_allow_html=True)
    image_1 = Image.open("11.リクリット・ティラバーニャ「“Who’s Afraid of Red, Yellow and Green,」.jpg")
    st.image(image_1, width=400)


    with st.form('qestion_form', clear_on_submit=False):
        st.markdown('### 話しかけてみよう!')
        prompt = st.text_area('テキストエリア')
        submitted = st.form_submit_button("送信")


        if submitted:
             # 会話の回数をカウント
            st.session_state.conversation_count += 1
            update_bg_color()
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
            
            # レスポンスの処理
            with st.spinner("ATAIの返信を受診中..."):
                time.sleep(2)
            st.markdown('''### ATAI (Art Thinking AI)より''')
            st.info(response['choices'][0]['message']['content'])
           
            conversation_history_1.append({"role": "assistant", "content": response['choices'][0]['message']['content']})

    
def page2():
    prompt = ""  # Initialize your prompt

    st.title('マルセル・デュシャン「泉」')
    st.write('<font size="5">好きな絵についてATAI(Art Thinking AI)  と思ったこと/感じたことを話してみましょう。「この絵は明るいね」「よくわからない」など素直にどんどん書き出して会話を楽しみましょう。</font>', unsafe_allow_html=True)
    image_1 = Image.open("4.マルセル・デュシャン「泉」.png")
    st.image(image_1, width=400)
    

    with st.form('qestion_form', clear_on_submit=False):
        st.markdown('''### 話しかけてみよう!''')
        prompt = st.text_area('テキストエリア')
        submitted = st.form_submit_button("送信")


        if submitted:
            st.text('質問を受け付けました！')
            conversation_history_2.append({"role": "user", "content": prompt})
            

            # OpenAIのAPIを直接使用
            headers = {
                'Authorization': f'Bearer {openai.api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content":"命令書:あなたは[対話型鑑賞の専門家]です。"},
                    {"role": "system", "content": "命令書:あなたは以下の制約条件に従って、相手に問いかけます。"},
                    {"role": "system", "content": "制約条件:あなたはマルセル・デュシャン「泉」という作品について、相手とやり取りする"},
                    {"role": "system", "content": "制約条件:あなたが1度の会話で行う質問は必ず1つずつ。"},
                    {"role": "system", "content": "制約条件:あなたが一度の会話で答えられる文字数は、150字以内。"},
                    {"role": "system", "content": "制約条件:あなたが説明する時は、あなたが質問を5つ以上行った後とする。"},
                    {"role": "system", "content": "制約条件:相手が「終了」「終わります」と言ったら、あなたは「ありがとうございました」と返す。"},
                    {"role": "system", "content": "制約条件:あなたは相手との会話で[対話型鑑賞力]を評価する。相手の[対話型鑑賞力]を100点満点で点数を付ける。"},
                    {"role": "system", "content": "制約条件:講評として相手の考え方・特徴を述べる。"},
                     ] + conversation_history_2
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data).json()
            
            # レスポンスの処理
            with st.spinner("ATAIの返信を受診中..."):
                time.sleep(2)
            st.markdown('''### ATAI (Art Thinking AI)より''')
            st.info(response['choices'][0]['message']['content'])
            # st.info(response.choices[0].message.content)
            


            # print(prompt)
            # print(response.choices[0].message.content.strip())
            conversation_history_2.append({"role": "assistant", "content": response['choices'][0]['message']['content']})

    
def page3():
    prompt = ""  # Initialize your prompt

    st.title('クリスト＆ジャンヌ＝クロード「L’Arc de Triomphe, Wrapped」')
    st.write('<font size="5">好きな絵についてATAI(Art Thinking AI)  と思ったこと/感じたことを話してみましょう。「この絵は明るいね」「よくわからない」など素直にどんどん書き出して会話を楽しみましょう。</font>', unsafe_allow_html=True)
    image_1 = Image.open("9.クリスト＆ジャンヌ＝クロード「「L’Arc de Triomphe, Wrapped」.jpg")
    st.image(image_1, width=400)
    

    with st.form('qestion_form', clear_on_submit=False):
        st.markdown('### 話しかけてみよう!')
        prompt = st.text_area('テキストエリア')
        submitted = st.form_submit_button("送信")


        if submitted:
            st.text('質問を受け付けました！')
            conversation_history_3.append({"role": "user", "content": prompt})
            

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
                    {"role": "system", "content": "制約条件:あなたはクリスト＆ジャンヌ＝クロード「L’Arc　de　Triomphe,　Wrapped」という作品について、相手とやり取りする。"},
                    {"role": "system", "content": "制約条件:あなたが1度の会話で行う質問は必ず1つずつ。"},
                    {"role": "system", "content": "制約条件:あなたが一度の会話で答えられる文字数は、150字以内。"},
                    {"role": "system", "content": "制約条件:あなたが説明する時は、あなたが質問を5つ以上行った後とする。"},
                    {"role": "system", "content": "制約条件:相手が「終了」「終わります」と言ったら、あなたは「ありがとうございました」と返す。"},
                    {"role": "system", "content": "制約条件:あなたは相手との会話で[対話型鑑賞力]を評価する。相手の[対話型鑑賞力]を100点満点で点数を付ける。"},
                    {"role": "system", "content": "制約条件:講評として相手の考え方・特徴を述べる。"},
                     ] + conversation_history_3
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data).json()
            

            # レスポンスの処理
            with st.spinner("ATAIの返信を受診中..."):
                time.sleep(2)
            st.markdown('''### ATAI (Art Thinking AI)より''')
            st.info(response['choices'][0]['message']['content'])
            # st.info(response.choices[0].message.content)
            


            # print(prompt)
            # print(response.choices[0].message.content.strip())
            conversation_history_3.append({"role": "assistant", "content": response['choices'][0]['message']['content']})


def page4():
    prompt = ""  # Initialize your prompt

    st.title('フェリックス・ゴンザレス＝トレス「無題(ロスの肖像 L.A.にて)」')
    st.write('<font size="5">好きな絵についてATAI(Art Thinking AI)  と思ったこと/感じたことを話してみましょう。「この絵は明るいね」「よくわからない」など素直にどんどん書き出して会話を楽しみましょう。</font>', unsafe_allow_html=True)
    image_1 = Image.open("10.フェリックス・ゴンザレス＝トレス「無題(ロスの肖像 L.A.にて)」.jpg")
    st.image(image_1, width=400)
    

    with st.form('qestion_form', clear_on_submit=False):
        st.markdown('''### 話しかけてみよう!''')
        prompt = st.text_area('テキストエリア')
        submitted = st.form_submit_button("送信")


        if submitted:
            st.text('質問を受け付けました！')
            conversation_history_4.append({"role": "user", "content": prompt})
            

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
                    {"role": "system", "content": "制約条件:あなたはフェリックス・ゴンザレス＝トレス「無題(ロスの肖像 L.A.にて)」という作品について、相手とやり取りする。"},
                    {"role": "system", "content": "制約条件:あなたが1度の会話で行う質問は必ず1つずつ。"},
                    {"role": "system", "content": "制約条件:あなたが一度の会話で答えられる文字数は、150字以内。"},
                    {"role": "system", "content": "制約条件:あなたが説明する時は、あなたが質問を5つ以上行った後とする。"},
                    {"role": "system", "content": "制約条件:相手が「終了」「終わります」と言ったら、あなたは「ありがとうございました」と返す。"},
                    {"role": "system", "content": "制約条件:あなたは相手との会話で[対話型鑑賞力]を評価する。相手の[対話型鑑賞力]を100点満点で点数を付ける。"},
                    {"role": "system", "content": "制約条件:講評として相手の考え方・特徴を述べる。"},
                    ] + conversation_history_4
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data).json()
            

            # レスポンスの処理
            with st.spinner("ATAIの返信を受診中..."):
                time.sleep(2)
            st.markdown('''### ATAI (Art Thinking AI)より''')
            st.info(response['choices'][0]['message']['content'])
            # st.info(response.choices[0].message.content)
            


            # print(prompt)
            # print(response.choices[0].message.content.strip())
            conversation_history_4.append({"role": "assistant", "content": response['choices'][0]['message']['content']})



def page5():
    prompt = ""  # Initialize your prompt

    st.title('パブロ・ピカソ「アヴィニョンの娘たち」')
    st.write('<font size="5">好きな絵についてATAI(Art Thinking AI)  と思ったこと/感じたことを話してみましょう。「この絵は明るいね」「よくわからない」など素直にどんどん書き出して会話を楽しみましょう。</font>', unsafe_allow_html=True)
    image_1 = Image.open("2.パブロ・ピカソ「アヴィニョンの娘たち」.jpg")
    st.image(image_1, width=400)
    

    with st.form('qestion_form', clear_on_submit=False):
        st.markdown('### 話しかけてみよう!')
        prompt = st.text_area('テキストエリア')
        submitted = st.form_submit_button("送信")


        if submitted:
            st.text('質問を受け付けました！')
            conversation_history_5.append({"role": "user", "content": prompt})
            

            # OpenAIのAPIを直接使用
            headers = {
                'Authorization': f'Bearer {openai.api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                "model": "gpt-4",
                "messages":[
                    {"role": "system", "content": "命令書:あなたは[対話型鑑賞の専門家]です。"},
                    {"role": "system", "content": "命令書:あなたは以下の制約条件に従って、相手に問いかけます。"},
                    {"role": "system", "content": "制約条件:あなたはパブロ・ピカソ「アヴィニョンの娘たち」という作品について、相手とやり取りする"},
                    {"role": "system", "content": "制約条件:あなたが1度の会話で行う質問は必ず1つずつ"},
                    {"role": "system", "content": "制約条件:あなたが一度の会話で答えられる文字数は、150字以内。"},
                    {"role": "system", "content": "制約条件:あなたが説明する時は、あなたが質問を5つ以上行った後とする。"},
                    {"role": "system", "content": "制約条件:相手が「終了」「終わります」と言ったら、あなたは「ありがとうございました」と返す。"},
                    {"role": "system", "content": "制約条件:あなたは相手との会話で[対話型鑑賞力]を評価する。相手の[対話型鑑賞力]を100点満点で点数を付ける。"},
                    {"role": "system", "content": "制約条件:講評として相手の考え方・特徴を述べる。"},
                     ] + conversation_history_5
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data).json()
            

            # レスポンスの処理
            with st.spinner("ATAIの返信を受診中..."):
                time.sleep(2)
            st.markdown('''### ATAI (Art Thinking AI)より''')
            st.info(response['choices'][0]['message']['content'])
            # st.info(response.choices[0].message.content)
            


            # print(prompt)
            # print(response.choices[0].message.content.strip())
            conversation_history_5.append({"role": "assistant", "content": response['choices'][0]['message']['content']})



page_names_to_funcs = {
    "Main Page": main_page,
    "1.リクリット・ティラバーニャ「Who’s　Afraid　of　Red,　Yellow　and　Green?」": page1,
    "2.マルセル・デュシャン「泉」": page2,
    "3.クリスト＆ジャンヌ＝クロード「L’Arc　de　Triomphe,　Wrapped」": page3,
    "4.フェリックス・ゴンザレス＝トレス「無題(ロスの肖像 L.A.にて)」": page4,
    "5.パブロ・ピカソ「アヴィニョンの娘たち」": page5,
    }

selected_page = st.sidebar.radio("メニュー", ["main　page",
                                          "1.リクリット・ティラバーニャ「Who’s　Afraid　of　Red,　Yellow　and　Green?」",
                                          "2.マルセル・デュシャン「泉」",
                                          "3.クリスト＆ジャンヌ＝クロード「L’Arc　de　Triomphe,　Wrapped」",
                                          "4.フェリックス・ゴンザレス＝トレス「無題(ロスの肖像 L.A.にて)」", 
                                          "5.パブロ・ピカソ「アヴィニョンの娘たち」"])
if selected_page == "main　page":
    main_page()
elif selected_page == "1.リクリット・ティラバーニャ「Who’s　Afraid　of　Red,　Yellow　and　Green?」":
    page1()
elif selected_page == "2.マルセル・デュシャン「泉」":
    page2()
elif selected_page == "3.クリスト＆ジャンヌ＝クロード「L’Arc　de　Triomphe,　Wrapped」":
    page3()
elif selected_page == "4.フェリックス・ゴンザレス＝トレス「無題(ロスの肖像 L.A.にて)」":
    page4()
elif selected_page == "5.パブロ・ピカソ「アヴィニョンの娘たち」":
    page5()
else:
    pass
