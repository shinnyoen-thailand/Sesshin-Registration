import datetime
from datetime import datetime, date
import requests
import streamlit as st

# ご自身のGASのウェブアプリのURLに書き換えてください
GAS_URL = "https://script.google.com/macros/s/AKfycbxuLepC6AnvSTG4A2qufRUczqgYFmuRzkBXhydO4Ww9dnpuyixRfjxyyUyA3zlgYkJl/exec"

# 受付種類ごとの金額設定データ（タイ語・日本語・英語併記）
AMOUNT_CONFIG = {
    "向上": {
        "thai": "โคโจเซสชิน",
        "jp": "向上",
        "base": "100 Bath",
        "child": "50 Bath\n(15 years or under)",
    },
    "向上相談": {
        "thai": "โคโจโซดันเซสชิน",
        "jp": "向上相談",
        "base": "200 Bath",
        "child": "100 Bath\n(15 years or under)",
    },
    "初信": {
        "thai": "Beginner",
        "jp": "初信",
        "base": "100 Bath",
        "child": "50 Bath\n(15 years or under)",
    },
    "相談": {
        "thai": "เซสชินปรึกษา",
        "jp": "相談",
        "base": "300 Bath",
        "child": "150 Bath\n(15 years or under)",
    },
    "特別相談": {
        "thai": "เซสชินปรึกษาพิเศษ",
        "jp": "特別相談",
        "base": "600 Bath",
        "child": "300 Bath\n(15 years or under)",
    },
    "鑑定": {
        "thai": "เซสชินเพื่อการตัดสินใจ",
        "jp": "鑑定",
        "base": "900 Bath",
        "child": "450 Bath\n(15 years or under)",
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
        min-height: 120px !important;
        border-radius: 16px !important;
        border: 3px solid #1e293b !important;
        background-color: #ffffff !important;
        box-shadow: 0px 6px 12px rgba(0,0,0,0.12) !important;
        transition: all 0.2s !important;
    }
    .stButton > button p {
        font-size: 36px !important;
        font-weight: 900 !important;
        color: #0f172a !important;
        margin: 0 !important;
        white-space: pre-line !important;
        text-align: center !important;
        line-height: 1.2 !important;
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
          min-height: 240px !important;
          margin-bottom: 15px !important;
      }
      div[data-testid="column"]:last-child .stButton > button,
      div[data-testid="stColumn"]:last-child .stButton > button {
          min-height: 120px !important;
          margin-bottom: 10px !important;
      }
      .stButton > button p {
          font-size: 32px !important;
          font-weight: 900 !important;
      }
      </style>
      """,
      unsafe_allow_html=True,
  )

  st.markdown("<h1 style='text-align: center; font-size: 45px; margin-bottom: 20px;'>Sesshin Registration / 接心受付</h1>", unsafe_allow_html=True)

  col_left, col_right = st.columns(2, gap="large")

  def make_btn_text(jp_name):
    cfg = AMOUNT_CONFIG.get(jp_name, {})
    thai = cfg.get("thai", "")
    return f"{thai}\n{jp_name}"

  with col_left:
    if st.button(make_btn_text("向上"), key="btn_kojo", use_container_width=True):
      st.session_state.selected_category = "向上"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button(make_btn_text("向上相談"), key="btn_kojosodan", use_container_width=True):
      st.session_state.selected_category = "向上相談"
      st.session_state.step = "input_details"
      st.rerun()

  with col_right:
    if st.button(make_btn_text("初信"), key="btn_shoshin", use_container_width=True):
      st.session_state.selected_category = "初信"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button(make_btn_text("相談"), key="btn_sodan", use_container_width=True):
      st.session_state.selected_category = "相談"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button(make_btn_text("特別相談"), key="btn_tokubetsusodan", use_container_width=True):
      st.session_state.selected_category = "特別相談"
      st.session_state.step = "input_details"
      st.rerun()

    if st.button(make_btn_text("鑑定"), key="btn_kantei", use_container_width=True):
      st.session_state.selected_category = "鑑定"
      st.session_state.step = "input_details"
      st.rerun()

  st.write("")
  if st.button("📊 Today's Summary and Cash Verification\n本日の集計・金庫確認", key="btn_summary", use_container_width=True):
    st.session_state.step = "summary"
    st.rerun()


# =========================================================
# 画面2：詳細情報の入力画面 (iPad最適化サイズ)
# =========================================================
elif st.session_state.step == "input_details":
  st.markdown(
      """
      <style>
      button[kind="secondary"] { min-height: 70px !important; }
      button[kind="secondary"] p { font-size: 26px !important; }
      button[kind="primary"] { min-height: 110px !important; }
      button[kind="primary"] p { font-size: 38px !important; }
      
      h3 { 
          font-size: 28px !important; 
          font-weight: 900 !important; 
          color: #1e293b !important; 
          border-left: 8px solid #3b82f6;
          padding-left: 12px;
          margin-bottom: 12px !important; 
          margin-top: 5px !important; 
      }

      /* お名前入力欄 */
      textarea[aria-label="お名前"] {
          font-size: 40px !important;
          font-weight: 900 !important;
          height: 120px !important;
          color: #000000 !important;
          background-color: #f8fafc !important;
          border: 3px solid #1e293b !important;
          border-radius: 12px !important;
      }
      
      /* 任意金額入力欄 */
      textarea[aria-label="任意金額"] {
          font-size: 38px !important;
          font-weight: 900 !important;
          height: 90px !important;
          color: #000000 !important;
          background-color: #ffffff !important;
          border: 3px solid #ca8a04 !important;
          border-radius: 10px !important;
      }

      /* ラジオボタンの文字サイズ（iPad用最適化） */
      [data-testid="stRadio"] label p {
          font-size: 25px !important;
          font-weight: 800 !important;
          color: #000000 !important;
          white-space: pre-line !important; /* 改行を有効化 */
          line-height: 1.25 !important;
      }
      [data-testid="stRadio"] {
          transform: scale(1.2);
          transform-origin: left center;
          margin-left: 10px;
          margin-top: 10px;
          margin-bottom: 15px;
      }

      /* チェックボックスの文字サイズ（iPad用最適化） */
      [data-testid="stCheckbox"] label p {
          font-size: 25px !important;
          font-weight: 800 !important;
          color: #000000 !important;
          line-height: 1.25 !important;
      }
      [data-testid="stCheckbox"] {
          transform: scale(1.3);
          transform-origin: left center;
          margin-top: 10px;
          margin-bottom: 10px;
          margin-left: 10px;
      }
      </style>
      """,
      unsafe_allow_html=True,
  )

  category = st.session_state.selected_category
  amt_info = AMOUNT_CONFIG.get(category, AMOUNT_CONFIG["向上"])
  thai_title = amt_info.get("thai", "")
  
  st.markdown(f"<h1 style='font-size: 36px; margin-bottom: 10px;'>受付 / ลงทะเบียน: 【 {category} ({thai_title}) 】</h1>", unsafe_allow_html=True)

  if st.button("← 戻る / ย้อนกลับ"):
    st.session_state.step = "select_category"
    st.rerun()

  st.write("---")

  # 1. お名前入力欄 ＆ 確認欄
  st.markdown("### Name （ภาษาอังกฤษ/English) / お名前")
  name = st.text_area(
      "お名前",
      label_visibility="collapsed",
      placeholder="กรอกชื่อภาษาอังกฤษ / Type Name in English",
      height=120,
  )
  
  if name.strip():
    st.markdown(
        f"""
        <div style="
            border: 3px solid #1e293b;
            background-color: #f8fafc;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            margin-top: 10px;
            margin-bottom: 15px;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
        ">
            <p style="font-size: 22px; font-weight: bold; color: #475569; margin: 0;">ตรวจสอบชื่อ / ご入力名のご確認</p>
            <p style="font-size: 55px; font-weight: 950; color: #0f172a; margin: 5px 0 0 0; word-break: break-all;">
                {name.strip()} ท่าน / 様
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.write("---")

  # 2. その他の選択肢 (左右カラム)
  col_left, col_right = st.columns(2, gap="large")

  with col_left:
    st.markdown("### ภาษา / 言語")
    language = st.radio(
        "言語", 
        ["日本語 / Japanese", "英語 / English", "タイ語 / ภาษาไทย"], 
        label_visibility="collapsed"
    )
    
    kai_suu = "-"
    if category == "初信":
      st.write("")
      st.markdown("### จำนวนครั้ง / 回数")
      kai_suu = st.radio(
          "回数", 
          ["ครั้งที่ 1 / 1回目", "ครั้งที่ 2 / 2回目", "ครั้งที่ 3 / 3回目", "มากกว่า 1 ปี / 1年以上"], 
          label_visibility="collapsed"
      )

    st.write("")
    st.markdown("### ตัวเลือกอื่น ๆ / その他")
    is_kanki = st.checkbox("ปีติขึ้นไป / 歓喜以上")
    is_priority = st.checkbox("Priority / 優先")
    is_infant = st.checkbox("พร้อมทารก / 乳児連れ")

  with col_right:
    st.markdown("### จำนวนเงิน / 金額")
    
    # 金額選択肢（2段表示・小さめ文字対応）
    other_option_label = "อื่น ๆ (ถวายปัจจัย)\nその他（お典供）"
    
    amount_type = st.radio(
        "金額種別",
        [amt_info["base"], amt_info["child"], other_option_label],
        label_visibility="collapsed",
        key="amount_radio",
    )

    is_amount_error = False

    if "อื่น ๆ" in amount_type or "その他" in amount_type:
      st.markdown(
          """
          <div style='background-color: #fef9c3; padding: 18px; border-radius: 12px; border: 3px solid #facc15; margin-top: 10px;'>
          <p style='font-size: 22px; font-weight: 900; color: #854d0e; margin-bottom: 10px;'>กรอกตัวเลข / 半角数字で記入</p>
          """, 
          unsafe_allow_html=True
      )
      
      custom_amount = st.text_area(
          "任意金額",
          label_visibility="collapsed",
          placeholder="Ex: 2000",
          height=90,
          key="custom_amount"
      )

      custom_val = custom_amount.strip()
      
      st.write("")
      custom_currency = st.radio("通貨", ["Bath", "円 / Yen"], horizontal=True, label_visibility="collapsed", key="custom_currency")

      clean_currency = "円" if "円" in custom_currency else "Bath"

      if custom_val:
        if not custom_val.isdigit():
          st.error("⚠️ Error: กรอกเฉพาะตัวเลข / 数字のみで入力してください。")
          is_amount_error = True
          selected_amount = f"{custom_val} {clean_currency}"
        else:
          st.success(f"確認 / OK: {custom_val} {clean_currency}")
          selected_amount = f"{custom_val} {clean_currency}"
      else:
        selected_amount = f"0 {clean_currency}"

      st.markdown("</div>", unsafe_allow_html=True)
        
    else:
      # 2段改行が含まれる選択肢の場合、1行（改行除去）にして保存用データを作成
      selected_amount = amount_type.replace("\n", " ")

    st.write("")
    st.markdown("### วิธีชำระเงิน / 支払方法")
    payment = st.radio("支払方法", ["QR", "Cash"], label_visibility="collapsed")

  st.write("---")
  st.write("")

  if st.button("เสร็จสิ้น / 完了", type="primary"):
    if name.strip() == "":
      st.warning("กรุณากรอกชื่อ / お名前を入力してください。")
    elif is_amount_error:
      st.error("กรุณาลบตัวอักษรในช่องจำนวนเงิน / 金額欄の誤入力を修正してください。")
    else:
      with st.spinner("กำลังส่งข้อมูล... / 送信中..."):
        now = datetime.now().strftime("%Y-%m-%d")

        # 言語データ整形（GAS保存用）
        clean_lang = "日本語"
        if "English" in language:
          clean_lang = "英語"
        elif "ภาษาไทย" in language:
          clean_lang = "タイ語"

        # 回数データ整形
        clean_kai = "-"
        if "1" in kai_suu: clean_kai = "1回目"
        elif "2" in kai_suu: clean_kai = "2回目"
        elif "3" in kai_suu: clean_kai = "3回目"
        elif "มากกว่า" in kai_suu or "1年" in kai_suu: clean_kai = "1年以上"

        # 優先判定
        priority_str = ""
        if is_priority and is_infant:
          priority_str = "〇 / 乳児連れ"
        elif is_priority:
          priority_str = "〇"
        elif is_infant:
          priority_str = "乳児連れ"

        post_data = {
            "date": now,
            "category": category,
            "amount": selected_amount,
            "name": name.strip(),
            "kaiSuu": clean_kai,
            "language": clean_lang,
            "isKanki": "〇" if is_kanki else "",
            "isPriority": priority_str,
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
            st.error("การส่งข้อมูลล้มเหลว / データの送信に失敗しました。")
        except Exception as e:
          st.error(f"Error: {e}")


# =========================================================
# 集計画面（スプレッドシートの集計結果 + 視認性重視の金庫カウント）
# =========================================================
elif st.session_state.step == "summary":
  st.markdown("<h1 style='text-align: center; font-size: 38px;'>Today's Summary and Cash Verification<br>本日の受付集計 ＆ 現金確認</h1>", unsafe_allow_html=True)

  if st.button("← 戻る / ย้อนกลับ"):
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
    st.error(f"エラー: {e}")

  categories = ["向上", "初信", "向上相談", "相談", "特別相談", "鑑定"]
  
  tot_count = 0
  tot_qr = 0
  tot_bath = 0
  tot_yen = 0

  table_html = """<table style="width:100%; border-collapse: collapse; font-size: 22px; text-align: center; background-color: #ffffff;"><thead><tr style="background-color: #f1f5f9;"><th style="border: 2px solid #1e293b; padding: 10px;"></th><th style="border: 2px solid #1e293b; padding: 10px;">人数</th><th style="border: 2px solid #1e293b; padding: 10px;">QR</th><th colspan="2" style="border: 2px solid #1e293b; padding: 10px; background-color: #e2e8f0;">Cash</th></tr><tr style="background-color: #f8fafc;"><th style="border: 2px solid #1e293b; padding: 6px;"></th><th style="border: 2px solid #1e293b; padding: 6px;"></th><th style="border: 2px solid #1e293b; padding: 6px;"></th><th style="border: 2px solid #1e293b; padding: 6px;">Bath</th><th style="border: 2px solid #1e293b; padding: 6px;">Yen</th></tr></thead><tbody>"""

  for cat in categories:
    d = summary_data.get(cat, {"count": 0, "qr": 0, "bath": 0, "yen": 0})
    tot_count += d["count"]
    tot_qr += d["qr"]
    tot_bath += d["bath"]
    tot_yen += d["yen"]

    table_html += f"""<tr><td style="border: 2px solid #1e293b; padding: 10px; font-weight: bold; background-color: #f8fafc;">{cat}</td><td style="border: 2px solid #1e293b; padding: 10px;">{d["count"]}</td><td style="border: 2px solid #1e293b; padding: 10px;">{d["qr"]}</td><td style="border: 2px solid #1e293b; padding: 10px;">{d["bath"]}</td><td style="border: 2px solid #1e293b; padding: 10px;">{d["yen"]}</td></tr>"""

  table_html += f"""<tr style="background-color: #cbd5e1; font-weight: bold;"><td style="border: 2px solid #1e293b; padding: 10px;">合計 / Total</td><td style="border: 2px solid #1e293b; padding: 10px;">{tot_count}</td><td style="border: 2px solid #1e293b; padding: 10px;">{tot_qr}</td><td style="border: 2px solid #1e293b; padding: 10px;">{tot_bath}</td><td style="border: 2px solid #1e293b; padding: 10px;">{tot_yen}</td></tr></tbody></table>"""
  
  st.markdown(table_html, unsafe_allow_html=True)

  st.write("")
  st.write("---")

  st.markdown("### 💰 金庫の現金カウント（実査・入力枠）")

  st.markdown(
      """
      <style>
      input[type="number"] {
          background-color: #fef08a !important;
          font-size: 28px !important;
          font-weight: bold !important;
          color: #0f172a !important;
          height: 50px !important;
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
      st.markdown(f"<p style='font-size:28px; font-weight:bold; text-align:right; margin-top:8px;'>{denom}</p>", unsafe_allow_html=True)
    with c2:
      st.markdown("<p style='font-size:36px; font-weight:900; text-align:center; margin-top:3px; color:#1e293b;'>×</p>", unsafe_allow_html=True)
    with c3:
      count = st.number_input(f"{denom}", min_value=0, value=0, step=1, label_visibility="collapsed", key=key)
    with c4:
      st.markdown("<p style='font-size:36px; font-weight:900; text-align:center; margin-top:3px; color:#1e293b;'>＝</p>", unsafe_allow_html=True)
    with c5:
      subtotal = denom * count
      calc_totals[currency] += subtotal
      st.markdown(
          f"""
          <div style="
              background-color: #fef08a;
              border: 2px solid #ca8a04;
              border-radius: 6px;
              height: 50px;
              display: flex;
              align-items: center;
              justify-content: center;
              margin-top: 3px;
          ">
              <span style="font-size: 26px; font-weight: bold; color: #0f172a;">{subtotal:,} {currency}</span>
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
          border-radius: 10px;
          padding: 15px;
          text-align: center;
          margin-top: 15px;
      ">
          <p style="font-size: 24px; font-weight: bold; color: #166534; margin: 0;">【現金合計 / Cash Total】</p>
          <p style="font-size: 38px; font-weight: 950; color: #14532d; margin: 5px 0 0 0;">
              🇹🇭 <b>{total_bath:,} Bath</b> /別 🇯🇵 <b>{total_yen:,} Yen</b>
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
      .stButton > button { min-height: 120px !important; }
      .stButton > button p { font-size: 40px !important; font-weight: bold !important; }
      h1 { font-size: 45px !important; text-align: center; }
      h2 { font-size: 90px !important; text-align: center; color: #1e293b; margin-top: 20px; margin-bottom: 20px;}
      h3 { font-size: 36px !important; text-align: center; }
      </style>
      """,
      unsafe_allow_html=True,
  )

  st.markdown("<h1>ลงทะเบียนเสร็จสิ้น / 受付が完了いたしました</h1>", unsafe_allow_html=True)
  st.markdown(f"<h3>ชื่อ / お名前: {st.session_state.completed_name} ท่าน / 様</h3>", unsafe_allow_html=True)
  
  st.markdown(f"<h2>หมายเลข / 受付番号: {st.session_state.ticket_id}</h2>", unsafe_allow_html=True)

  st.info("กรุณากรอกหมายเลขนี้ในใบเสร็จ / この番号をレシートにお書きください。")

  st.write("")
  st.write("")
  if st.button("ลงทะเบียนคนถัดไป / 次の人の受付をする"):
    st.session_state.step = "select_category"
    st.rerun()
