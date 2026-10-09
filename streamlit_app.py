import datetime
from datetime import datetime
import requests
import streamlit as st

# ご自身のGASのウェブアプリのURLに書き換えてください
GAS_URL = "https://script.google.com/macros/s/AKfycbyTMfOuVuNqIvKecJ32TmjBgEGW4MpqcRtVXkkDIUtC7ZeAGlxScLKLzHXiCZEOJ31Q/exec"

# ---------------------------------------------------------
# 全画面共通のベース設定
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* 画面の左右の余白を極限まで減らして、iPadの画面をフルに使う */
    .block-container {
        max-width: 95% !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* ボタン全体の基本デザイン。絶対に幅を100%にする */
    div[data-testid="stButton"], div[data-testid="stButton"] > button {
        width: 100% !important;
    }
    
    div[data-testid="stButton"] > button {
        border-radius: 15px !important;
        border: 4px solid #1e293b !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
        box-shadow: 0px 5px 10px rgba(0,0,0,0.1) !important;
        transition: all 0.2s !important;
    }
    
    div[data-testid="stButton"] > button:hover {
        background-color: #f1f5f9 !important;
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
      /* 左側の列（向上・向上相談） */
      div[data-testid="column"]:nth-of-type(1) div[data-testid="stButton"] button { height: 260px !important; margin-bottom: 20px !important; }
      div[data-testid="column"]:nth-of-type(1) div[data-testid="stButton"] p { font-size: 55px !important; font-weight: bold !important; }
      
      /* 右側の列（初信・相談・特別相談・鑑定） */
      div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"] button { height: 120px !important; margin-bottom: 15px !important; }
      div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"] p { font-size: 40px !important; font-weight: bold !important; }
      </style>
      """,
      unsafe_allow_html=True,
  )

  st.markdown("<h1 style='text-align: center; font-size: 45px;'>受付システム - 種類を選択</h1>", unsafe_allow_html=True)
  st.write("")

  # 左右の幅を 1:1 にして綺麗に並べる
  col_left, col_right = st.columns(2, gap="large")

  # ※ use_container_width=True を指定して強制的に幅を広げます
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
      /* 戻るボタンや完了ボタンのサイズ */
      div[data-testid="stButton"] button { height: 110px !important; }
      div[data-testid="stButton"] p { font-size: 38px !important; font-weight: bold !important; }
      
      h3 { font-size: 36px !important; color: #1e293b !important; margin-bottom: 10px !important; }

      /* ▼▼ 言語などのプルダウン（選択ボックス）を巨大化 ▼▼ */
      div[data-baseweb="select"] > div {
          min-height: 70px !important;
          font-size: 28px !important;
          border-radius: 10px !important;
      }
      /* プルダウンを開いたときの選択肢の文字も巨大化 */
      ul[role="listbox"] li {
          font-size: 28px !important;
          padding-top: 15px !important;
          padding-bottom: 15px !important;
      }

      /* ▼▼ チェックボックスとラジオボタンの枠を巨大化 ▼▼ */
      [data-testid="stCheckbox"] {
          transform: scale(1.8);  /* 1.8倍に拡大！ */
          transform-origin: left center;
          margin-top: 10px;
          margin-bottom: 25px;
          margin-left: 10px;
      }
      [data-testid="stRadio"] {
          transform: scale(1.8);  /* 1.8倍に拡大！ */
          transform-origin: left center;
          margin-left: 10px;
      }
      </style>
      """,
      unsafe_allow_html=True,
  )

  category = st.session_state.selected_category
  st.markdown(f"<h1>受付: 【 {category} 】</h1>", unsafe_allow_html=True)

  if st.button("← 最初の画面に戻る"):
    st.session_state.step = "select_category"
    st.rerun()

  st.write("---")

  st.markdown("### お名前（ペンまたはテキストで記入）")
  name = st.text_area(
      "お名前",
      label_visibility="collapsed",
      placeholder="ここに名前を記入してください",
      height=150,
  )
  
  st.write("---")

  col1, col2, col3 = st.columns(3, gap="large")

  with col1:
    st.markdown("### 言語")
    language = st.selectbox("言語", ["日本語", "英語", "タイ語"], label_visibility="collapsed")
    
    kai_suu = "-"
    if category == "初信":
      st.write("")
      st.markdown("### 回数")
      kai_suu = st.selectbox("回数", ["1回目", "2回目", "3回目", "1年以上"], label_visibility="collapsed")

  with col2:
    # 「オプション」の文字を消しつつ、隣の「言語」と高さを揃えるための透明なスペース
    st.markdown("<div style='height: 52px;'></div>", unsafe_allow_html=True)
    
    is_kanki = st.checkbox("歓喜以上")
    st.write("")
    is_priority = st.checkbox("優先")

  with col3:
    st.markdown("### 支払方法")
    payment = st.radio("支払方法", ["QR", "Cash"], label_visibility="collapsed")

  st.write("---")
  st.write("")

  if st.button("受付を完了する", type="primary"):
    if name.strip() == "":
      st.warning("お名前を入力してください。")
    else:
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
          st.error("データの送信に失敗しました。")
      except Exception as e:
        st.error(f"エラーが発生しました: {e}")


# =========================================================
# 画面3：完了画面
# =========================================================
elif st.session_state.step == "completed":
  st.markdown(
      """
      <style>
      div[data-testid="stButton"] button { height: 120px !important; }
      div[data-testid="stButton"] p { font-size: 40px !important; font-weight: bold !important; }
      h1 { font-size: 50px !important; text-align: center; }
      h2 { font-size: 100px !important; text-align: center; color: #1e293b; margin-top: 20px;}
      h3 { font-size: 45px !important; text-align: center; }
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
