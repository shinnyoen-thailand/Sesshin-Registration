import datetime
from datetime import datetime
import requests
import streamlit as st

# ご自身のGASのウェブアプリのURLに書き換えてください
GAS_URL = "https://script.google.com/macros/s/AKfycbyTMfOuVuNqIvKecJ32TmjBgEGW4MpqcRtVXkkDIUtC7ZeAGlxScLKLzHXiCZEOJ31Q/exec"

# ---------------------------------------------------------
# 【超重要】Streamlitのボタンを強制的に巨大化するCSS
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

    /* ---------------------------------------------------
       ボタン全体のデザイン（枠線、角丸、背景色）
       --------------------------------------------------- */
    [data-testid="stButton"] button {
        width: 100% !important;
        border-radius: 15px !important;
        border: 4px solid #1e293b !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
        box-shadow: 0px 5px 10px rgba(0,0,0,0.1) !important;
        transition: all 0.2s !important;
    }
    
    /* 押したとき・触れたときの色 */
    [data-testid="stButton"] button:hover {
        background-color: #f1f5f9 !important;
        border-color: #000000 !important;
    }

    /* ---------------------------------------------------
       左側の列（向上、向上相談）のサイズ設定
       --------------------------------------------------- */
    [data-testid="stColumn"]:nth-of-type(1) [data-testid="stButton"] button {
        height: 280px !important; /* ボタンの高さを超巨大に */
    }
    /* 左側の文字サイズ */
    [data-testid="stColumn"]:nth-of-type(1) [data-testid="stButton"] p {
        font-size: 55px !important;
        font-weight: bold !important;
    }

    /* ---------------------------------------------------
       右側の列（初信、相談、特別相談、鑑定）のサイズ設定
       --------------------------------------------------- */
    [data-testid="stColumn"]:nth-of-type(2) [data-testid="stButton"] button {
        height: 125px !important; /* 4つ並べるための高さ */
    }
    /* 右側の文字サイズ */
    [data-testid="stColumn"]:nth-of-type(2) [data-testid="stButton"] p {
        font-size: 40px !important;
        font-weight: bold !important;
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


# --- 画面1：受付種類の選択 ---
if st.session_state.step == "select_category":
  st.markdown("<h1 style='text-align: center; font-size: 45px;'>受付システム - 種類を選択</h1>", unsafe_allow_html=True)
  st.write("")

  # 左右の幅を 1:1 にして綺麗に並べる
  col_left, col_right = st.columns(2, gap="large")

  # 左側：向上、向上相談
  with col_left:
    if st.button("向上", key="btn_kojo", use_container_width=True):
      st.session_state.selected_category = "向上"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button("向上相談", key="btn_kojosodan", use_container_width=True):
      st.session_state.selected_category = "向上相談"
      st.session_state.step = "input_details"
      st.rerun()

  # 右側：初信、相談、特別相談、鑑定
  with col_right:
    if st.button("初信(*)", key="btn_shoshin", use_container_width=True):
      st.session_state.selected_category = "初信(*)"
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


# --- 画面2：詳細情報の入力画面 ---
elif st.session_state.step == "input_details":
  category = st.session_state.selected_category
  st.title(f"受付: 【 {category} 】")

  if st.button("← 最初の画面に戻る"):
    st.session_state.step = "select_category"
    st.rerun()

  st.write("---")

  kai_suu = "-"
  if category == "初信(*)":
    kai_suu = st.selectbox(
        "回数を選んでください", ["1回目", "2回目", "3回目", "1年以上"]
    )

  st.markdown("### お名前（ペンまたはテキストで記入）")
  name = st.text_area(
      "お名前入力欄",
      label_visibility="collapsed",
      placeholder="ここに名前を入力してください",
      height=140,
  )

  language = st.selectbox("言語", ["日本語", "英語", "タイ語"])

  is_kanki = st.checkbox("歓喜以上であればチェックを入れてください")
  is_priority = st.checkbox("優先（チェック欄）")

  payment = st.radio("支払方法", ["QR", "Cash"])

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


# --- 画面3：完了画面 ---
elif st.session_state.step == "completed":
  st.title("受付が完了いたしました")

  st.markdown(f"### お名前: {st.session_state.completed_name} 様")
  st.markdown(f"# 受付番号: {st.session_state.ticket_id}")

  st.info("この番号をレシートにお書きください。")

  st.write("")
  if st.button("次の人の受付をする"):
    st.session_state.step = "select_category"
    st.rerun()
