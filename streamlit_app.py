import datetime
from datetime import datetime, date
import requests
import streamlit as st

# ご自身のGASのウェブアプリのURLに書き換えてください
GAS_URL = "https://script.google.com/macros/s/AKfycbyGofUnzrAKmmUEeGpeX8dSs5amZQPiLC0sHnHLi-0RMItVJFwXp5gC08LJGBCrcsbO/exec"

# 受付種類ごとの金額設定データ
AMOUNT_CONFIG = {
    "向上": {
        "base": "100 Bath",
        "child": "50 Bath（15歳以下）",
        "countries": [
            "日本 1000円",
            "日本 250Bath",
            "シンガポール 150Bath",
            "アメリカ 200Bath",
            "フランス 300Bath",
        ],
    },
    "向上相談": {
        "base": "200 Bath",
        "child": "100 Bath（15歳以下）",
        "countries": [
            "日本 2000円",
            "日本 400Bath",
            "シンガポール 250Bath",
            "アメリカ 300Bath",
            "フランス 400Bath",
        ],
    },
    "相談": {
        "base": "300 Bath",
        "child": "150 Bath（15歳以下）",
        "countries": [
            "日本 3000円",
            "日本 600Bath",
            "シンガポール 300Bath",
            "アメリカ 400Bath",
            "フランス 500Bath",
        ],
    },
    "特別相談": {
        "base": "600 Bath",
        "child": "300 Bath（15歳以下）",
        "countries": [
            "日本 6000円",
            "日本 1200Bath",
            "シンガポール 500Bath",
            "アメリカ 600Bath",
            "フランス 700Bath",
        ],
    },
    "鑑定": {
        "base": "900 Bath",
        "child": "450 Bath（15歳以下）",
        "countries": [
            "日本 9000円",
            "日本 1900Bath",
            "シンガポール 1100Bath",
            "アメリカ 12000Bath",
            "フランス 1400Bath",
        ],
    },
}

# =========================================================
# 全画面共通：ベース設定
# =========================================================
st.markdown(
    """
    <style>
    .block-container {
        max-width: 98% !important;
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
    .stButton > button {
        width: 100% !important;
        min-height: 140px !important;
        border-radius: 20px !important;
        border: 4px solid #1e293b !important;
        background-color: #ffffff !important;
        box-shadow: 0px 8px 16px rgba(0,0,0,0.15) !important;
        transition: all 0.2s !important;
    }
    .stButton > button p {
        font-size: 45px !important;
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
# 画面1：接心受付 ＆ 集計ボタン
# =========================================================
if st.session_state.step == "select_category":
  st.markdown(
      """
      <style>
      div[data-testid="column"]:first-child .stButton > button,
      div[data-testid="stColumn"]:first-child .stButton > button {
          min-height: 300px !important;
          margin-bottom: 15px !important;
      }
      div[data-testid="column"]:first-child .stButton > button p,
      div[data-testid="stColumn"]:first-child .stButton > button p {
          font-size: 65px !important;
      }
      div[data-testid="column"]:last-child .stButton > button,
      div[data-testid="stColumn"]:last-child .stButton > button {
          min-height: 140px !important;
          margin-bottom: 10px !important;
      }
      </style>
      """,
      unsafe_allow_html=True,
  )

  st.markdown("<h1 style='text-align: center; font-size: 50px; margin-bottom: 20px;'>接心受付</h1>", unsafe_allow_html=True)

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

  st.write("")
  if st.button("📊 本日の集計・金庫確認を開く", key="btn_summary", use_container_width=True):
    st.session_state.step = "summary"
    st.rerun()


# =========================================================
# 画面2：詳細情報の入力画面
# =========================================================
elif st.session_state.step == "input_details":
  st.markdown(
      """
      <style>
      button[kind="secondary"] { min-height: 80px !important; }
      button[kind="secondary"] p { font-size: 30px !important; }
      button[kind="primary"] { min-height: 120px !important; }
      button[kind="primary"] p { font-size: 40px !important; }
      h3 { font-size: 28px !important; color: #1e293b !important; margin-bottom: 10px !important; }

      /* プルダウン（セレクトボックスの箱自体）の高さを大きく（約2倍）し、枠線を太く */
      [data-testid="stSelectbox"] div[data-baseweb="select"] {
          min-height: 100px !important;
          border-radius: 12px !important;
          border: 4px solid #1e293b !important;
      }
      /* プルダウン内で選択されている文字を大きく太く */
      [data-testid="stSelectbox"] div[data-baseweb="select"] * {
          font-size: 32px !important;
          font-weight: bold !important;
          color: #0f172a !important;
      }
      /* プルダウンを開いたときの中身（メニュー一覧）の文字と余白を大きく */
      div[data-baseweb="menu"] *, ul[role="listbox"] *, li[role="option"] * {
          font-size: 32px !important;
          font-weight: bold !important;
          color: #0f172a !important;
          padding-top: 12px !important;
          padding-bottom: 12px !important;
      }
      /* ラジオボタン（金額・支払方法）の文字を大きく太く */
      [data-testid="stRadio"] label p {
          font-size: 32px !important;
          font-weight: bold !important;
          color: #0f172a !important;
      }
      /* チェックボックスの文字を大きく太く */
      [data-testid="stCheckbox"] label p {
          font-size: 32px !important;
          font-weight: bold !important;
          color: #0f172a !important;
      }
      [data-testid="stCheckbox"] {
          transform: scale(1.6);
          transform-origin: left center;
          margin-top: 15px;
          margin-bottom: 25px;
          margin-left: 10px;
      }
      [data-testid="stRadio"] {
          transform: scale(1.5);
          transform-origin: left center;
          margin-left: 10px;
          margin-top: 10px;
          margin-bottom: 10px;
      }
      </style>
      """,
      unsafe_allow_html=True,
  )

  category = st.session_state.selected_category
  st.markdown(f"<h1 style='font-size: 40px;'>受付: 【 {category} 】</h1>", unsafe_allow_html=True)

  if st.button("← 戻る"):
    st.session_state.step = "select_category"
    st.rerun()

  st.write("---")

  st.markdown("### お名前（ペンまたはテキストで記入）")
  name = st.text_area(
      "お名前",
      label_visibility="collapsed",
      placeholder="ここに名前を記入してください",
      height=120,
  )
  
  if name.strip():
    st.markdown(
        f"""
        <div style="
            border: 4px solid #1e293b;
            background-color: #f8fafc;
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            margin-top: 5px;
            margin-bottom: 15px;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
        ">
            <p style="font-size: 24px; font-weight: bold; color: #475569; margin: 0;">【ご入力名のご確認】</p>
            <p style="font-size: 55px; font-weight: 900; color: #0f172a; margin: 5px 0 0 0; word-break: break-all;">
                {name.strip()} 様
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.write("---")

  amt_info = AMOUNT_CONFIG.get(category, AMOUNT_CONFIG["向上"])
  col1, col2, col3 = st.columns(3, gap="large")

  with col1:
    st.markdown("### 金額")
    amount_type = st.radio(
        "金額種別",
        [amt_info["base"], amt_info["child"], "国別選択（その他）"],
        label_visibility="collapsed",
        key="amount_radio",
    )

    if amount_type == "国別選択（その他）":
      st.write("")
      selected_amount = st.selectbox(
          "国別金額",
          amt_info["countries"],
          label_visibility="collapsed",
          key="country_amount_select",
      )
    else:
      selected_amount = amount_type

  with col2:
    st.markdown("### 言語")
    language = st.selectbox("言語", ["日本語", "英語", "タイ語"], label_visibility="collapsed")
    
    kai_suu = "-"
    if category == "初信":
      st.write("")
      st.markdown("### 回数")
      kai_suu = st.selectbox("回数", ["1回目", "2回目", "3回目", "1年以上"], label_visibility="collapsed")

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
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
      with st.spinner("送信中... しばらくお待ちください"):
        now = datetime.now().strftime("%Y-%m-%d")

        post_data = {
            "date": now,
            "category": category,
            "amount": selected_amount,
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
# 集計画面（スプレッドシートの集計結果 + 視認性重視の金庫カウント）
# =========================================================
elif st.session_state.step == "summary":
  st.markdown("<h1 style='text-align: center; font-size: 45px;'>本日の受付集計 ＆ 現金確認</h1>", unsafe_allow_html=True)

  if st.button("← 戻る"):
    st.session_state.step = "select_category"
    st.rerun()

  st.write("---")

  today_str = datetime.now().strftime("%Y-%m-%d")
  st.markdown(f"### Date: **{today_str}**")

  summary_data = {}
  try:
    res = requests.post(GAS_URL, json={"action": "summary", "date": today_str})
    if res.status_code == 200:
      summary_data = res.json().get("summary", {})
  except Exception as e:
    st.error(f"集計データの取得に失敗しました: {e}")

  categories = ["向上", "初信", "向上相談", "相談", "特別相談", "鑑定"]
  
  tot_count = 0
  tot_qr = 0
  tot_bath = 0
  tot_yen = 0

  table_html = """<table style="width:100%; border-collapse: collapse; font-size: 24px; text-align: center; background-color: #ffffff;"><thead><tr style="background-color: #f1f5f9;"><th style="border: 2px solid #1e293b; padding: 12px;"></th><th style="border: 2px solid #1e293b; padding: 12px;">人数</th><th style="border: 2px solid #1e293b; padding: 12px;">QR</th><th colspan="2" style="border: 2px solid #1e293b; padding: 12px; background-color: #e2e8f0;">Cash</th></tr><tr style="background-color: #f8fafc;"><th style="border: 2px solid #1e293b; padding: 8px;"></th><th style="border: 2px solid #1e293b; padding: 8px;"></th><th style="border: 2px solid #1e293b; padding: 8px;"></th><th style="border: 2px solid #1e293b; padding: 8px;">Bath</th><th style="border: 2px solid #1e293b; padding: 8px;">Yen</th></tr></thead><tbody>"""

  for cat in categories:
    d = summary_data.get(cat, {"count": 0, "qr": 0, "bath": 0, "yen": 0})
    tot_count += d["count"]
    tot_qr += d["qr"]
    tot_bath += d["bath"]
    tot_yen += d["yen"]

    table_html += f"""<tr><td style="border: 2px solid #1e293b; padding: 12px; font-weight: bold; background-color: #f8fafc;">{cat}</td><td style="border: 2px solid #1e293b; padding: 12px;">{d["count"]}</td><td style="border: 2px solid #1e293b; padding: 12px;">{d["qr"]}</td><td style="border: 2px solid #1e293b; padding: 12px;">{d["bath"]}</td><td style="border: 2px solid #1e293b; padding: 12px;">{d["yen"]}</td></tr>"""

  table_html += f"""<tr style="background-color: #cbd5e1; font-weight: bold;"><td style="border: 2px solid #1e293b; padding: 12px;">合計</td><td style="border: 2px solid #1e293b; padding: 12px;">{tot_count}</td><td style="border: 2px solid #1e293b; padding: 12px;">{tot_qr}</td><td style="border: 2px solid #1e293b; padding: 12px;">{tot_bath}</td><td style="border: 2px solid #1e293b; padding: 12px;">{tot_yen}</td></tr></tbody></table>"""
  
  st.markdown(table_html, unsafe_allow_html=True)

  st.write("")
  st.write("---")

  st.markdown("### 💰 金庫の現金カウント（実査・入力枠）")
  st.markdown("黄色の枠内に金庫にある紙幣の枚数を入力してください。金額が自動計算されます。")

  st.markdown(
      """
      <style>
      input[type="number"] {
          background-color: #fef08a !important;
          font-size: 32px !important;
          font-weight: bold !important;
          color: #0f172a !important;
          height: 55px !important;
          border-radius: 6px !important;
          border: 2px solid #ca8a04 !important;
          text-align: center !important;
      }
      </style>
      """,
      unsafe_allow_html=True,
  )

  denominations = [
      (50, "n_50", "Bath"),
      (100, "n_100", "Bath"),
      (500, "n_500", "Bath"),
      (1000, "n_1000", "Bath"),
      (250, "n_250", "Bath"),
      (1000, "n_1000y", "Yen"),
  ]

  calc_totals = {"Bath": 0, "Yen": 0}

  for denom, key, currency in denominations:
    c1, c2, c3, c4, c5 = st.columns([1.5, 0.8, 2.5, 0.8, 3.5])
    
    with c1:
      st.markdown(f"<p style='font-size:32px; font-weight:bold; text-align:right; margin-top:10px;'>{denom}</p>", unsafe_allow_html=True)
    with c2:
      st.markdown("<p style='font-size:40px; font-weight:900; text-align:center; margin-top:5px; color:#1e293b;'>×</p>", unsafe_allow_html=True)
    with c3:
      count = st.number_input(f"{denom}", min_value=0, value=0, step=1, label_visibility="collapsed", key=key)
    with c4:
      st.markdown("<p style='font-size:40px; font-weight:900; text-align:center; margin-top:5px; color:#1e293b;'>＝</p>", unsafe_allow_html=True)
    with c5:
      subtotal = denom * count
      calc_totals[currency] += subtotal
      st.markdown(
          f"""
          <div style="
              background-color: #fef08a;
              border: 2px solid #ca8a04;
              border-radius: 6px;
              height: 55px;
              display: flex;
              align-items: center;
              justify-content: center;
              margin-top: 5px;
          ">
              <span style="font-size: 30px; font-weight: bold; color: #0f172a;">{subtotal:,} {currency}</span>
          </div>
          """,
          unsafe_allow_html=True,
      )

  total_bath = calc_totals["Bath"]
  total_yen = calc_totals["Yen"]

  st.write("")
  st.markdown(
      f"""
      <div style="
          background-color: #dcfce7;
          border: 3px solid #16a34a;
          border-radius: 12px;
          padding: 20px;
          text-align: center;
          margin-top: 20px;
      ">
          <p style="font-size: 28px; font-weight: bold; color: #166534; margin: 0;">【現金合計】</p>
          <p style="font-size: 45px; font-weight: 950; color: #14532d; margin: 10px 0 0 0;">
              🇹🇭 <b>{total_bath:,} Bath</b> / 🇯🇵 <b>{total_yen:,} Yen</b>
          </p>
      </div>
      """,
      unsafe_allow_html=True,
  )


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
