import datetime
from datetime import datetime
import requests
import streamlit as st

# ご自身のGASのウェブアプリのURLに書き換えてください
GAS_URL = "https://script.google.com/macros/s/AKfycbyTMfOuVuNqIvKecJ32TmjBgEGW4MpqcRtVXkkDIUtC7ZeAGlxScLKLzHXiCZEOJ31Q/exec"

# ---------------------------------------------------------
# 全画面共通のベース設定（ボタンの枠線や背景色）
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

    /* ボタン全体の基本デザイン */
    [data-testid="stButton"] button {
        width: 100% !important;
        border-radius: 15px !important;
        border: 4px solid #1e293b !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
        box-shadow: 0px 5px 10px rgba(0,0,0,0.1) !important;
        transition: all 0.2s !important;
    }
    
    [data-testid="stButton"] button:hover {
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
  # 画面1専用のCSS（巨大ボタンの設定）
  st.markdown(
      """
      <style>
      /* 左側の列 */
      [data-testid="stColumn"]:nth-of-type(1) [data-testid="stButton"] button { height: 280px !important; }
      [data-testid="stColumn"]:nth-of-type(1) [data-testid="stButton"] p { font-size: 55px !important; font-weight: bold !important; }
      /* 右側の列 */
      [data-testid="stColumn"]:nth-of-type(2) [data-testid="stButton"] button { height: 125px !important; }
      [data-testid="stColumn"]:nth-of-type(2) [data-testid="stButton"] p { font-size: 40px !important; font-weight: bold !important; }
      </style>
      """,
      unsafe_allow_html=True,
  )

  st.markdown("<h1 style='text-align: center; font-size: 45px;'>受付システム - 種類を選択</h1>", unsafe_allow_html=True)
  st.write("")

  col_left, col_right = st.columns(2, gap="large")

  with col_left:
    if st.button("向上", key="btn_kojo"):
      st.session_state.selected_category = "向上"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button("向上相談", key="btn_kojosodan"):
      st.session_state.selected_category = "向上相談"
      st.session_state.step = "input_details"
      st.rerun()

  with col_right:
    if st.button("初信", key="btn_shoshin"):
      st.session_state.selected_category = "初信"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button("相談", key="btn_sodan"):
      st.session_state.selected_category = "相談"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button("特別相談", key="btn_tokubetsusodan"):
      st.session_state.selected_category = "特別相談"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button("鑑定", key="btn_kantei"):
      st.session_state.selected_category = "鑑定"
      st.session_state.step = "input_details"
      st.rerun()


# =========================================================
# 画面2：詳細情報の入力画面
# =========================================================
elif st.session_state.step == "input_details":
  # 画面2専用のCSS（入力項目の文字を大きくする設定）
  st.markdown(
      """
      <style>
      /* 戻るボタンや完了ボタンのサイズ */
      [data-testid="stButton"] button { height: 110px !important; }
      [data-testid="stButton"] p { font-size: 38px !important; font-weight: bold !important; }
      
      /* 文字を全体的に大きく */
      .stCheckbox p, .stRadio p, .stSelectbox p {
          font-size: 32px !important;
          font-weight: bold !important;
      }
      div[data-baseweb="select"] { font-size: 28px !important; }
      h3 { font-size: 36px !important; color: #1e293b !important; margin-bottom: 5px !important; }
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

  # 1. お名前入力（画面いっぱいに横長）
  st.markdown("### お名前（ペンまたはテキストで記入）")
  name = st.text_area(
      "お名前",
      label_visibility="collapsed",
      placeholder="ここに名前を記入してください",
      height=150,
  )
  
  st.write("---")

  # 2. その他の情報を横に3分割して画面をフル活用
  col1, col2, col3 = st.columns(3, gap="large")

  with col1:
    st.markdown("### 言語")
    language = st.selectbox("言語", ["日本語", "英語", "タイ語"], label_visibility="collapsed")
    
    # 初信が選ばれた場合だけ「回数」を表示
    kai_suu = "-"
    if category == "初信":
      st.write("")
      st.markdown("### 回数")
      kai_suu = st.selectbox("回数", ["1回目", "2回目", "3回目", "1年以上"], label_visibility="collapsed")

  with col2:
    st.markdown("### オプション")
    is_kanki = st.checkbox("歓喜以上")
    st.write("")
    is_priority = st.checkbox("優先")

  with col3:
    st.markdown("### 支払方法")
    payment = st.radio("支払方法", ["QR", "Cash"], label_visibility="collapsed")

  st.write("---")
  st.write("")

  # 完了ボタン
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
  # 画面3専用のCSS
  st.markdown(
      """
      <style>
      [data-testid="stButton"] button { height: 120px !important; }
      [data-testid="stButton"] p { font-size: 40px !important; font-weight: bold !important; }
      h1 { font-size: 50px !important; text-align: center; }
      h2 { font-size: 100px !important; text-align: center; color: #1e293b; margin-top: 20px;}
      h3 { font-size: 45px !important; text-align: center; }
      </style>
      """,
      unsafe_allow_html=True,
  )

  st.markdown("<h1>受付が完了いたしました</h1>", unsafe_allow_html=True)
  st.markdown(f"<h3>お名前:
