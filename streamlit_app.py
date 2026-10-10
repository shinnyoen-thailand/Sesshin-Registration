import datetime
from datetime import datetime
import requests
import streamlit as st

# ご自身のGASのウェブアプリのURLに書き換えてください
GAS_URL = "https://script.google.com/macros/s/AKfycbyTMfOuVuNqIvKecJ32TmjBgEGW4MpqcRtVXkkDIUtC7ZeAGlxScLKLzHXiCZEOJ31Q/exec"

# =========================================================
# 全画面共通：ベース設定
# =========================================================
st.markdown(
    """
    <style>
    /* 画面の左右の余白を極限まで減らして、iPadの画面をフルに使う */
    .block-container {
        max-width: 98% !important;
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }

    /* 全てのボタンに「最低でもこの高さにする」という絶対命令 */
    .stButton > button {
        width: 100% !important;
        min-height: 160px !important;
        border-radius: 20px !important;
        border: 4px solid #1e293b !important;
        background-color: #ffffff !important;
        box-shadow: 0px 8px 16px rgba(0,0,0,0.15) !important;
        transition: all 0.2s !important;
    }
    
    .stButton > button p {
        font-size: 50px !important;
        font-weight: 900 !important;
        color: #0f172a !important;
        margin: 0 !important;
    }

    .stButton > button:hover {
        background-color: #f8fafc !important;
        border-color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 画面の状態管理
if "step" not in st.session_state:
  st.session_state.step = "select_category"
if "selected_category" not in st.session_state:
  st.session_state.selected_category = ""


# =========================================================
# 画面1：受付種類の選択
# =========================================================
if st.session_state.step == "select_category":
  st.markdown(
      """
      <style>
      div[data-testid="column"]:first-child .stButton > button,
      div[data-testid="stColumn"]:first-child .stButton > button {
          min-height: 350px !important;
          margin-bottom: 20px !important;
      }
      div[data-testid="column"]:first-child .stButton > button p,
      div[data-testid="stColumn"]:first-child .stButton > button p {
          font-size: 70px !important;
      }

      div[data-testid="column"]:last-child .stButton > button,
      div[data-testid="stColumn"]:last-child .stButton > button {
          min-height: 160px !important;
          margin-bottom: 10px !important;
      }
      </style>
      """,
      unsafe_allow_html=True,
  )

  st.markdown("<h1 style='text-align: center; font-size: 50px; margin-bottom: 30px;'>接心受付</h1>", unsafe_allow_html=True)

  col_left, col_right = st.columns(2, gap="large")

  with col_left:
    if st.button("向上", key="btn_kojo", use_container_width=True):
      st.session_state.selected_category = "向上"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button("向上相談", key="btn_kojosodan", use_container_width=True):
      st.session_state.selected_category = "向上相談"
      st.session_state.step = "input_details"
      st.rerun()

  with col_right:
    if st.button("初信", key="btn_shoshin", use_container_width=True):
      st.session_state.selected_category = "初信"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button("相談", key="btn_sodan", use_container_width=True):
      st.session_state.selected_category = "相談"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button("特別相談", key="btn_tokubetsusodan", use_container_width=True):
      st.session_state.selected_category = "特別相談"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button("鑑定", key="btn_kantei", use_container_width=True):
      st.session_state.selected_category = "鑑定"
      st.session_state.step = "input_details"
      st.rerun()


# =========================================================
# 画面2：詳細情報の入力画面
# =========================================================
elif st.session_state.step == "input_details":
  st.markdown(
      """
      <style>
      button[kind="secondary"] { 
          min-height: 100px !important; 
      }
      button[kind="secondary"] p { 
          font-size: 35px !important; 
      }

      button[kind="primary"] { 
          min-height: 140px !important; 
      }
      button[kind="primary"] p { 
          font-size: 45px !important; 
      }
      
      h3 { font-size: 40px !important; color: #1e293b !important; margin-bottom: 15px !important; }

      div[data-baseweb="select"] > div {
          min-height: 100px !important;
          font-size: 40px !important;
          border-radius: 12px !important;
      }
      div[data-baseweb="select"] span {
          font-size: 40px !important;
      }
      ul[role="listbox"] li {
          font-size: 40px !important;
          padding-top: 25px !important;
          padding-bottom: 25px !important;
      }

      [data-testid="stCheckbox"] {
          transform: scale(2.0);
          transform-origin: left center;
          margin-top: 15px;
          margin-bottom: 35px;
          margin-left: 15px;
      }
      [data-testid="stRadio"] {
          transform: scale(2.0);
          transform-origin: left center;
          margin-left: 15px;
          margin-top: 10px;
      }
      </style>
      """,
      unsafe_allow_html=True,
  )

  category = st.session_state.selected_category
  st.markdown(f"<h1 style='font-size: 45px;'>受付: 【 {category} 】</h1>", unsafe_allow_html=True)

  if st.button("← 最初の画面に戻る"):
    st.session_state.step = "select_category"
    st.rerun()

  st.write("---")

  st.markdown("### お名前（ペンまたはテキストで記入）")
  name = st.text_area(
      "お名前",
      label_visibility="collapsed",
      placeholder="ここに名前を記入してください",
      height=180,
  )
  
  st.write("---")

  col1, col2, col3 = st.columns(3, gap="large")

  with col1:
    st.markdown("### 言語")
    language = st.selectbox("言語", ["日本語", "英語", "タイ語"], label_visibility="collapsed")
    
    kai_suu = "-"
    if category == "初信":
      st.write("")
      st.write("")
      st.markdown("### 回数")
      kai_suu = st.selectbox("回数", ["1回目", "2回目", "3回目", "1年以上"], label_visibility="collapsed")

  with col2:
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
    is_kanki = st.checkbox("歓喜以上")
    st.write("")
    is_priority = st.checkbox("優先")

  with col3:
    st.markdown("### 支払方法")
    payment = st.radio("支払方法", ["QR", "Cash"], label_visibility="collapsed")

  st.write("---")
  st.write("")

  if st.button("完了", type="primary"):
    if name.strip() == "":
      st.warning("お名前を入力してください。")
    else:
      # ボタンを押した瞬間、画面に「送信中...」というクルクル（スピナー）を表示して入力を完全ロックする
      with st.spinner("送信中... しばらくお待ちください"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        post_data = {
            "date": now,
            "category": category,
            "name": name.strip(),
            "kaiSuu": kai_suu,
            "language": language,
            "isKanki": "〇" if is_kanki else "",
            "isPriority": "〇" if is_priority else "",
            "payment": payment,
        }

        try:
          response = requests.post(GAS_URL, json=post_data)
          res_json = response.json()

          if response.status_code == 200 and res_json.get("status") == "success":
            ticket_id = res_json.get("ticketId", "J1")
            st.session_state.ticket_id = ticket_id
            st.session_state.completed_name = name.strip()
            st.session_state.step = "completed"
            st.rerun()
          else:
            st.error("データの送信に失敗しました。もう一度お試しください。")
        except Exception as e:
          st.error(f"エラーが発生しました: {e}")


# =========================================================
# 画面3：完了画面
# =========================================================
elif st.session_state.step == "completed":
  st.markdown(
      """
      <style>
      .stButton > button { min-height: 150px !important; }
      .stButton > button p { font-size: 50px !important; font-weight: bold !important; }
      h1 { font-size: 60px !important; text-align: center; }
      h2 { font-size: 120px !important; text-align: center; color: #1e293b; margin-top: 30px; margin-bottom: 30px;}
      h3 { font-size: 50px !important; text-align: center; }
      </style>
      """,
      unsafe_allow_html=True,
  )

  st.markdown("<h1>受付が完了いたしました</h1>", unsafe_allow_html=True)
  st.markdown(f"<h3>お名前: {st.session_state.completed_name} 様</h3>", unsafe_allow_html=True)
  
  st.markdown(f"<h2>受付番号: {st.session_state.ticket_id}</h2>", unsafe_allow_html=True)

  st.info("この番号をレシートにお書きください。")

  st.write("")
  st.write("")
  if st.button("次の人の受付をする"):
    st.session_state.step = "select_category"
    st.rerun()
