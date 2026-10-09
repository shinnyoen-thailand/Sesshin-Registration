import datetime
from datetime import datetime
import requests
import streamlit as st

# ご自身のGASのウェブアプリのURLに書き換えてください
GAS_URL = "https://script.google.com/macros/s/AKfycbyTMfOuVuNqIvKecJ32TmjBgEGW4MpqcRtVXkkDIUtC7ZeAGlxScLKLzHXiCZEOJ31Q/exec"

# 画面全体の見た目を大きく調整するためのスタイル（CSS）
st.markdown(
    """
    <style>
    /* ボタンを大きくして押しやすくする */
    .stButton > button {
        font-size: 26px !important;
        font-weight: bold !important;
        height: 90px !important;
        border-radius: 12px !important;
    }
    /* タイトルの文字サイズを大きく */
    h1 {
        font-size: 36px !important;
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


# --- 画面1：受付種類の選択（大きく見やすいボタン） ---
if st.session_state.step == "select_category":
  st.title("受付システム - 種類を選択")
  st.write("画面のボタンをタッチして、受付の種類を選んでください。")
  st.write("")

  col1, col2 = st.columns(2)

  with col1:
    if st.button("向上", use_container_width=True, key="btn_kojo"):
      st.session_state.selected_category = "向上"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button("向上相談", use_container_width=True, key="btn_kojosodan"):
      st.session_state.selected_category = "向上相談"
      st.session_state.step = "input_details"
      st.rerun()

  with col2:
    if st.button("初信(*)", use_container_width=True, key="btn_shoshin"):
      st.session_state.selected_category = "初信(*)"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button("相談", use_container_width=True, key="btn_sodan"):
      st.session_state.selected_category = "相談"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button("特別相談", use_container_width=True, key="btn_tokubetsusodan"):
      st.session_state.selected_category = "特別相談"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button("鑑定", use_container_width=True, key="btn_kantei"):
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

  # 初信(*)の場合の回数選択
  kai_suu = "-"
  if category == "初信(*)":
    kai_suu = st.selectbox(
        "回数を選んでください", ["1回目", "2回目", "3回目", "1年以上"]
    )

  # お名前入力欄を大きく（テキストエリアに変更して最大表示）
  st.markdown("### お名前（ペンまたはテキストで記入）")
  name = st.text_area(
      "お名前入力欄",
      label_visibility="collapsed",
      placeholder="ここに名前を入力してください",
      height=120,
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
  # 受付番号を大きく表示
  st.markdown(f"# 受付番号: {st.session_state.ticket_id}")

  st.info("この番号をレシートにお書きください。")

  st.write("")
  if st.button("次の人の受付をする"):
    st.session_state.step = "select_category"
    st.rerun()
