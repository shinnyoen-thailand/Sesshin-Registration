import datetime
from datetime import datetime
import requests
import streamlit as st

# ご自身のGASのウェブアプリのURLに書き換えてください
GAS_URL = "https://script.google.com/macros/s/AKfycbyTMfOuVuNqIvKecJ32TmjBgEGW4MpqcRtVXkkDIUtC7ZeAGlxScLKLzHXiCZEOJ31Q/exec"

# 画面全体のデザイン設定（ボタンを大きくし、横幅いっぱいに綺麗に配置）
st.markdown(
    """
    <style>
    /* 画面のパディングを整える */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    
    /* ボタン全体のデザイン（文字を大きく、太く） */
    .stButton > button {
        font-size: 30px !important;
        font-weight: bold !important;
        width: 100% !important;
        border-radius: 12px !important;
        border: 2px solid #2c3e50 !important;
        background-color: #f8f9fa !important;
        color: #2c3e50 !important;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    
    /* マウスを乗せたとき・タップしたときの色 */
    .stButton > button:hover {
        background-color: #e2e8f0 !important;
        border-color: #1a252f !important;
    }

    /* 左側の大きなボタン（向上・向上相談）の高さ：260px */
    .left-btn-box div.stButton > button {
        height: 260px !important;
    }

    /* 右側の4つのボタン（初信・相談・特別相談・鑑定）の高さ：120px */
    .right-btn-box div.stButton > button {
        height: 120px !important;
    }

    h1 {
        font-size: 36px !important;
        text-align: center;
        margin-bottom: 30px;
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
  st.title("受付システム - 種類を選択")

  # 左右に大きく2分割
  col_left, col_right = st.columns(2, gap="large")

  # 左側：向上、向上相談
  with col_left:
    st.markdown('<div class="left-btn-box">', unsafe_allow_html=True)
    if st.button("向上", key="btn_kojo"):
      st.session_state.selected_category = "向上"
      st.session_state.step = "input_details"
      st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")  # 上下の隙間

    st.markdown('<div class="left-btn-box">', unsafe_allow_html=True)
    if st.button("向上相談", key="btn_kojosodan"):
      st.session_state.selected_category = "向上相談"
      st.session_state.step = "input_details"
      st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

  # 右側：初信、相談、特別相談、鑑定
  with col_right:
    st.markdown('<div class="right-btn-box">', unsafe_allow_html=True)
    if st.button("初信(*)", key="btn_shoshin"):
      st.session_state.selected_category = "初信(*)"
      st.session_state.step = "input_details"
      st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    st.markdown('<div class="right-btn-box">', unsafe_allow_html=True)
    if st.button("相談", key="btn_sodan"):
      st.session_state.selected_category = "相談"
      st.session_state.step = "input_details"
      st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    st.markdown('<div class="right-btn-box">', unsafe_allow_html=True)
    if st.button("特別相談", key="btn_tokubetsusodan"):
      st.session_state.selected_category = "特別相談"
      st.session_state.step = "input_details"
      st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    st.markdown('<div class="right-btn-box">', unsafe_allow_html=True)
    if st.button("鑑定", key="btn_kantei"):
      st.session_state.selected_category = "鑑定"
      st.session_state.step = "input_details"
      st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


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
  st.markdown(f"# 受付番号: {st.session_state.ticket_id}")

  st.info("この番号をレシートにお書きください。")

  st.write("")
  if st.button("次の人の受付をする"):
    st.session_state.step = "select_category"
    st.rerun()
