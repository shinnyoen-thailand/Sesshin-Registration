import datetime
from datetime import datetime, date
import re
import requests
import streamlit as st

# ご自身のGASのウェブアプリのURLに書き換えてください
GAS_URL = "https://script.google.com/macros/s/AKfycbz-b7OIJlO1M2cmMOw7l-Nf5yHuIS2bfGuT-z4xiw3SIb3kibEscaYay1iEbfS25uGk/exec"

# =========================================================
# 端末識別子 (ipad=A / ipad=B) の確実な取得と保持処理
# =========================================================
if "ipad_id" not in st.session_state:
    try:
        raw_param = st.query_params.get("ipad", "A")
        if isinstance(raw_param, list):
            raw_param = raw_param[0] if raw_param else "A"
        match = re.search(r'[A-Za-z0-9]', str(raw_param))
        st.session_state.ipad_id = match.group(0).upper() if match else "A"
    except Exception:
        st.session_state.ipad_id = "A"

# URLのアドレスバーにもパラメータを維持
st.query_params["ipad"] = st.session_state.ipad_id

# 受付種類ごとの金額設定データ (Baht 表記統一)
AMOUNT_CONFIG = {
    "向上": {
        "thai": "โคโจเซสชิน",
        "jp": "向上",
        "base": "100 Baht",
        "child": "50 Baht\n(15 years or under)",
    },
    "向上相談": {
        "thai": "โคโจโซดันเซสชิน",
        "jp": "向上相談",
        "base": "200 Baht",
        "child": "100 Baht\n(15 years or under)",
    },
    "初信": {
        "thai": "Beginner",
        "jp": "初信",
        "base": "100 Baht",
        "child": "50 Baht\n(15 years or under)",
    },
    "相談": {
        "thai": "เซสชินปรึกษา",
        "jp": "相談",
        "base": "300 Baht",
        "child": "150 Baht\n(15 years or under)",
    },
    "特別相談": {
        "thai": "เซสชินปรึกษาพิเศษ",
        "jp": "特別相談",
        "base": "600 Baht",
        "child": "300 Baht\n(15 years or under)",
    },
    "鑑定": {
        "thai": "เซสชินเพื่อการตัดสินใจ",
        "jp": "鑑定",
        "base": "800 Baht",
        "child": "400 Baht\n(15 years or under)",
    },
}

# 全画面共通ベース設定（背景色・基本ボタン・中央ローディングの設定）
st.markdown(
    """
<style>
.stApp, [data-testid="stAppViewContainer"] {
    background-color: #f0f7ff !important;
}

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

/* 送信中・処理中ローディング */
[data-testid="stSpinner"] {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    background-color: rgba(15, 23, 42, 0.65) !important;
    z-index: 999999 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
[data-testid="stSpinner"] > div {
    background-color: #ffffff !important;
    padding: 35px 55px !important;
    border-radius: 20px !important;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.3) !important;
    border: 4px solid #3b82f6 !important;
}
[data-testid="stSpinner"] * {
    font-size: 30px !important;
    font-weight: 900 !important;
    color: #0f172a !important;
}
</style>
""",
    unsafe_allow_html=True,
)

if "step" not in st.session_state:
    st.session_state.step = "select_category"
if "selected_category" not in st.session_state:
    st.session_state.selected_category = ""


# =========================================================
# 画面1：接心受付 ＆ 集計ボタン・取り消しボタン
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

div.st-key-btn_summary > button {
    min-height: 90px !important;
    background-color: #fef9c3 !important;
    border: 3px solid #eab308 !important;
}
div.st-key-btn_summary > button p {
    font-size: 24px !important;
    color: #854d0e !important;
}

div.st-key-btn_cancel_page > button {
    min-height: 90px !important;
    background-color: #f1f5f9 !important;
    border: 3px solid #64748b !important;
}
div.st-key-btn_cancel_page > button p {
    font-size: 24px !important;
    color: #334155 !important;
}
</style>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<h1 style='text-align: center; font-size: 42px; margin-bottom: 10px;'>Sesshin Registration / 接心受付</h1>"
        f"<p style='text-align: center; font-size: 26px; font-weight: 900; color: #0284c7; margin-bottom: 20px;'>【 Terminal {st.session_state.ipad_id} 】</p>",
        unsafe_allow_html=True,
    )

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

    c_sum, c_cancel = st.columns(2, gap="medium")
    with c_sum:
        if st.button("📊 Today's Summary\n本日の集計・現金確認", key="btn_summary", use_container_width=True):
            st.session_state.step = "summary"
            st.rerun()
    with c_cancel:
        if st.button("🗑️ Cancel Registration\n受付の取り消し・修正", key="btn_cancel_page", use_container_width=True):
            st.session_state.step = "cancel_page"
            st.rerun()


# =========================================================
# 画面2：詳細情報の入力画面
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
}

textarea[aria-label="お名前"] {
    font-size: 40px !important;
    font-weight: 900 !important;
    height: 120px !important;
    color: #000000 !important;
    background-color: #ffffff !important;
    border: 3px solid #1e293b !important;
    border-radius: 12px !important;
}

textarea[aria-label="任意金額"] {
    font-size: 38px !important;
    font-weight: 900 !important;
    height: 90px !important;
    color: #000000 !important;
    background-color: #ffffff !important;
    border: 3px solid #ca8a04 !important;
    border-radius: 10px !important;
}

[data-testid="stRadio"] label p {
    font-size: 25px !important;
    font-weight: 800 !important;
    color: #000000 !important;
    white-space: pre-line !important;
    line-height: 1.25 !important;
}
[data-testid="stRadio"] {
    transform: scale(1.2);
    transform-origin: left center;
    margin-left: 10px;
    margin-top: 10px;
    margin-bottom: 15px;
}

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

    st.markdown(f"<h1 style='font-size: 34px; margin-bottom: 10px;'>受付: 【 {category} ({thai_title}) 】 <span style='font-size:24px; color:#0284c7;'>(Terminal {st.session_state.ipad_id})</span></h1>", unsafe_allow_html=True)

    if st.button("← ย้อนกลับ / 戻る"):
        st.session_state.step = "select_category"
        st.rerun()

    st.write("---")

    st.markdown("### Name （ภาษาอังกฤษ/English)")
    name = st.text_area(
        "お名前",
        label_visibility="collapsed",
        placeholder="กรอกชื่อภาษาอังกฤษ / Type Name in English",
        height=120,
    )

    if name.strip():
        st.markdown(
            f"""
<div style="border: 3px solid #1e293b; background-color: #ffffff; border-radius: 12px; padding: 15px; text-align: center; margin-top: 10px; margin-bottom: 15px; box-shadow: 0px 4px 8px rgba(0,0,0,0.1);">
<p style="font-size: 22px; font-weight: bold; color: #475569; margin: 0;">ตรวจสอบชื่อ / ご入力名のご確認</p>
<p style="font-size: 55px; font-weight: 950; color: #0f172a; margin: 5px 0 0 0; word-break: break-all;">{name.strip()} san</p>
</div>
""",
            unsafe_allow_html=True,
        )

    st.write("---")

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.markdown("### ภาษา / 言語")
        language = st.radio(
            "言語", 
            ["ภาษาไทย / タイ語", "Japanese / 日本語", "English / 英語"], 
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

        other_option_label = "การถวาย\nお典供"

        amount_type = st.radio(
            "金額種別",
            [amt_info["base"], amt_info["child"], other_option_label],
            label_visibility="collapsed",
            key="amount_radio",
        )

        is_amount_error = False

        if "การถวาย" in amount_type or "お典供" in amount_type:
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
            custom_currency = st.radio("通貨", ["Baht", "円 / Yen"], horizontal=True, label_visibility="collapsed", key="custom_currency")

            clean_currency = "円" if "円" in custom_currency else "Baht"

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
            selected_amount = amount_type.replace("\n", " ")

        st.write("")
        st.markdown("### วิธีชำระเงิน / 支払方法")
        payment = st.radio("支払方法", ["QR", "Cash"], label_visibility="collapsed")

    st.write("---")
    st.write("")

    if st.button("完了 / เสร็จสิ้น", type="primary"):
        if name.strip() == "":
            st.warning("กรุณากรอกชื่อ / お名前を入力してください。")
        elif is_amount_error:
            st.error("กรุณาลบตัวอักษรในช่องจำนวนเงิน / 金額欄の誤入力を修正してください。")
        else:
            with st.spinner("กำลังส่งข้อมูล... / 送信中..."):
                now = datetime.now().strftime("%Y-%m-%d")

                cat_map = {
                    "向上": "KOJO",
                    "向上相談": "KOJOSOUDAN",
                    "初信": "Biginner",
                    "相談": "SODAN",
                    "特別相談": "TOKUBETU",
                    "鑑定": "KANTEI",
                }
                clean_cat = cat_map.get(category, category)

                clean_lang = "Japanese"
                if "English" in language:
                    clean_lang = "English"
                elif "ภาษาไทย" in language:
                    clean_lang = "Thai"

                clean_kai = "-"
                if "1" in kai_suu: clean_kai = "1"
                elif "2" in kai_suu: clean_kai = "2"
                elif "3" in kai_suu: clean_kai = "3"
                elif "มากกว่า" in kai_suu or "1年" in kai_suu: clean_kai = "1year up"

                post_data = {
                    "date": now,
                    "terminal": st.session_state.ipad_id,
                    "category": clean_cat,
                    "amount": selected_amount,
                    "name": name.strip(),
                    "kaiSuu": clean_kai,
                    "language": clean_lang,
                    "isKanki": "〇" if is_kanki else "",
                    "isPriority": "〇" if is_priority else "",
                    "isInfant": "〇" if is_infant else "",
                    "payment": payment,
                }

                try:
                    response = requests.post(GAS_URL, json=post_data)
                    res_json = response.json()

                    if response.status_code == 200 and res_json.get("status") == "success":
                        ticket_id = res_json.get("ticketId", "A-1")
                        st.session_state.ticket_id = ticket_id
                        st.session_state.completed_name = name.strip()
                        st.session_state.step = "completed"
                        st.rerun()
                    else:
                        st.error("การส่งข้อมูลล้มเหลว / データの送信に失敗しました。")
                except Exception as e:
                    st.error(f"Error: {e}")


# =========================================================
# 画面3：受付の取り消し・キャンセル画面
# =========================================================
elif st.session_state.step == "cancel_page":
    st.markdown("<h1 style='text-align: center; font-size: 38px;'>Cancel Registration / 受付の取り消し</h1>", unsafe_allow_html=True)

    if st.button("← ย้อนกลับ / 戻る"):
        st.session_state.step = "select_category"
        st.rerun()

    st.write("---")

    today_str = datetime.now().strftime("%Y-%m-%d")
    st.markdown(f"### Today's Registration Data List ({today_str})")

    records = []
    with st.spinner("กำลังโหลดข้อมูล... / データ取得中..."):
        try:
            res = requests.post(GAS_URL, json={"action": "get_records", "date": today_str})
            if res.status_code == 200:
                records = res.json().get("records", [])
        except Exception as e:
            st.error(f"Data Retrieval Error: {e}")

    if not records:
        st.info("There are no registration records for today.")
    else:
        for i, rec in enumerate(records):
            t_id = rec.get("ticketId") or f"NO_ID_{i}"
            name_str = rec.get("name", "Unknown")
            cat_str = rec.get("category", "-")
            amt_str = rec.get("amount", "-")
            pay_str = rec.get("payment", "-")

            c_info, c_btn = st.columns([3.5, 1.5])

            with c_info:
                st.markdown(
                    f"""
<div style="background-color: #ffffff; border: 2px solid #cbd5e1; border-radius: 10px; padding: 12px; margin-bottom: 10px;">
<span style="font-size: 24px; font-weight: 900; color: #1e293b;">【{t_id}】 {name_str} san</span><br>
<span style="font-size: 20px; font-weight: bold; color: #0284c7;">Category: {cat_str}</span> │ 
<span style="font-size: 20px; font-weight: bold; color: #16a34a;">Amount: {amt_str}</span> │ 
<span style="font-size: 20px; font-weight: bold; color: #d97706;">Payment: {pay_str}</span>
</div>
""",
                    unsafe_allow_html=True,
                )

            with c_btn:
                st.write("")
                if st.button(f"❌ Cancel\n({t_id})", key=f"del_{t_id}_{i}", use_container_width=True):
                    with st.spinner("กำลังยกเลิก... / 取り消し処理中..."):
                        try:
                            c_res = requests.post(GAS_URL, json={"action": "cancel_record", "ticketId": t_id})
                            if c_res.status_code == 200 and c_res.json().get("status") == "success":
                                st.success(f"【{t_id}】{name_str} The registration has been cancelled.")
                                st.rerun()
                            else:
                                st.error("Cancellation failed.")
                        except Exception as e:
                            st.error(f"error: {e}")


# =========================================================
# 画面4：集計画面
# =========================================================
elif st.session_state.step == "summary":
    st.markdown("<h1 style='text-align: center; font-size: 36px;'>Today's Summary and Cash Verification<br>本日の受付集計 ＆ 現金確認</h1>", unsafe_allow_html=True)

    if st.button("← ย้อนกลับ / 戻る"):
        st.session_state.step = "select_category"
        st.rerun()

    st.write("---")

    today_str = datetime.now().strftime("%Y-%m-%d")

    rows_def = [
        ("โคโจเซสชิน\n向上", 50, "Baht", "kojo_50"),
        ("", 100, "Baht", "kojo_100"),
        ("", 125, "Baht", "kojo_125"),
        ("", 250, "Baht", "kojo_250"),
        ("", 1000, "Yen", "kojo_1000y"),
        ("Beginner\n初信", 50, "Baht", "shoshin_50"),
        ("", 100, "Baht", "shoshin_100"),
        ("", 125, "Baht", "shoshin_125"),
        ("", 250, "Baht", "shoshin_250"),
        ("", 1000, "Yen", "shoshin_1000y"),
        ("โคโจโซดันเซสชิน 向上相談", 200, "Baht", "kojosodan_200"),
        ("เซสชินปรึกษา 相談", 300, "Baht", "sodan_300"),
        ("เซสชินปรึกษาพิเศษ 特別相談", 600, "Baht", "tokubetsu_600"),
        ("เซสชินเพื่อการตัดสินใจ 鑑定", 800, "Baht", "kantei_800"),
    ]

    summary_data = {}
    with st.spinner("กำลังคำนวณ... / 集計中..."):
        try:
            res = requests.post(GAS_URL, json={"action": "summary", "date": today_str})
            if res.status_code == 200:
                summary_data = res.json().get("summary", {})
        except Exception as e:
            st.error(f"Calculation Error: {e}")

    baht_cash_amt = 0
    yen_cash_amt = 0
    baht_qr_amt = 0
    yen_qr_amt = 0

    tbody_html = ""

    for cat_label, price, curr, key in rows_def:
        d = summary_data.get(key, {"cash_p": 0, "qr_p": 0})

        c_person = d.get("cash_p", 0)
        q_person = d.get("qr_p", 0)

        c_amount = c_person * price
        q_amount = q_person * price

        if curr == "Baht":
            baht_cash_amt += c_amount
            baht_qr_amt += q_amount
        else:
            yen_cash_amt += c_amount
            yen_qr_amt += q_amount

        qr_person_style = "background-color: #00e5ff;"
        qr_amount_style = ""
        if curr == "Yen":
            qr_person_style = "background-color: #555555;"
            qr_amount_style = "background-color: #555555;"

        cat_td = ""
        if cat_label == "โคโจเซสชิน\n向上":
            cat_td = f'<td rowspan="5" style="border: 1px solid #000; font-weight: bold; vertical-align: middle; white-space: pre-line;">{cat_label}</td>'
        elif cat_label == "Beginner\n初信":
            cat_td = f'<td rowspan="5" style="border: 1px solid #000; font-weight: bold; vertical-align: middle; white-space: pre-line;">{cat_label}</td>'
        elif cat_label != "":
            cat_td = f'<td style="border: 1px solid #000; font-weight: bold; text-align: left; padding-left: 10px;">{cat_label}</td>'

        c_amt_str = f"{c_amount:,}" if c_amount > 0 else ""
        q_amt_str = f"{q_amount:,}" if q_amount > 0 and curr != "Yen" else ""
        c_p_str = str(c_person) if c_person > 0 else ""
        q_p_str = str(q_person) if q_person > 0 and curr != "Yen" else ""

        tbody_html += f"<tr>{cat_td}<td style='border: 1px solid #000;'>{price} {curr}</td><td style='border: 1px solid #000; background-color: #00e5ff; font-weight: bold;'>{c_p_str}</td><td style='border: 1px solid #000;'>{c_amt_str}</td><td style='border: 1px solid #000; {qr_person_style} font-weight: bold;'>{' ' if curr=='Yen' else q_p_str}</td><td style='border: 1px solid #000; {qr_amount_style}'>{' ' if curr=='Yen' else q_amt_str}</td></tr>"

    table_html = f"""<div style="overflow-x:auto;">
<table style="width:100%; border-collapse: collapse; font-size: 18px; text-align: center; background-color: #ffffff; border: 2px solid #000000;">
<thead>
<tr style="background-color: #f1f5f9;">
<th rowspan="2" style="border: 1px solid #000; width: 25%; font-size: 16px;">Date</th>
<th rowspan="2" style="border: 1px solid #000; width: 15%; font-size: 16px;">ราคาต่อหน่วย<br>単価</th>
<th colspan="2" style="border: 1px solid #000; width: 30%; background-color: #f8fafc;">Cash</th>
<th colspan="2" style="border: 1px solid #000; width: 30%; background-color: #f8fafc;">QR</th>
</tr>
<tr style="background-color: #f8fafc;">
<th style="border: 1px solid #000; width: 15%;">Person</th>
<th style="border: 1px solid #000; width: 15%;">Amount</th>
<th style="border: 1px solid #000; width: 15%;">Person</th>
<th style="border: 1px solid #000; width: 15%;">Amount</th>
</tr>
<tr style="background-color: #ffffff;">
<td style="border: 1px solid #000; font-weight: bold; background-color: #f1f5f9;">{today_str}</td>
<td style="border: 1px solid #000;"></td>
<td style="border: 1px solid #000; background-color: #00e5ff;"></td>
<td style="border: 1px solid #000;"></td>
<td style="border: 1px solid #000; background-color: #00e5ff;"></td>
<td style="border: 1px solid #000;"></td>
</tr>
</thead>
<tbody>
{tbody_html}
<tr style="background-color: #d1d5db; font-weight: bold;">
<td colspan="2" style="border: 1px solid #000; text-align: right; padding-right: 15px;">Baht Total</td>
<td style="border: 1px solid #000;"></td>
<td style="border: 1px solid #000;">{baht_cash_amt:,}</td>
<td style="border: 1px solid #000; background-color: #555555;"></td>
<td style="border: 1px solid #000;">{baht_qr_amt:,}</td>
</tr>
<tr style="background-color: #d1d5db; font-weight: bold;">
<td colspan="2" style="border: 1px solid #000; text-align: right; padding-right: 15px;">Yen Total</td>
<td style="border: 1px solid #000;"></td>
<td style="border: 1px solid #000;">{yen_cash_amt:,}</td>
<td style="border: 1px solid #000; background-color: #555555;"></td>
<td style="border: 1px solid #000; background-color: #555555;"></td>
</tr>
</tbody>
</table>
</div>"""

    st.markdown(table_html, unsafe_allow_html=True)

    st.write("")
    st.write("---")

    # CASH ONLY エリア
    st.markdown("### CASH ONLY（Count the cash in the safe and enter the amount.）")

    # ★ 手入力エリアのCSS（＋/－ボタン動作完全補正 & 1000 Yen(n_1000y) の直接水色化指定）
    st.markdown(
        """
<style>
div[data-testid="stNumberInput"] {
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
}

div[data-testid="stNumberInput"] > div {
    width: 100% !important;
    background-color: transparent !important;
    border: none !important;
}

div[data-testid="stNumberInput"] input {
    background-color: #ffff00 !important;
    font-size: 24px !important;
    font-weight: bold !important;
    color: #0f172a !important;
    height: 52px !important;
    border-radius: 4px 0 0 4px !important;
    border: 2px solid #000000 !important;
    text-align: center !important;
    -webkit-appearance: none !important;
    -moz-appearance: textfield !important;
    box-sizing: border-box !important;
}

div[data-testid="stNumberInput"] button {
    height: 52px !important;
    min-width: 36px !important;
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    border: 2px solid #000000 !important;
    border-left: none !important;
    font-size: 20px !important;
    font-weight: bold !important;
    z-index: 10 !important;
    cursor: pointer !important;
}

/* ★ 1000 Yen (st-key-n_1000y) 専用の水色＆濃い青文字デザイン */
div.st-key-n_1000y input {
    background-color: #e0f2fe !important; /* 水色 */
    color: #0369a1 !important;            /* 濃い青文字 */
    border: 2px solid #0284c7 !important; /* 青枠線 */
}
div.st-key-n_1000y button {
    background-color: #bae6fd !important;
    border: 2px solid #0284c7 !important;
    border-left: none !important;
    color: #0369a1 !important;
}
</style>
""",
        unsafe_allow_html=True,
    )

    # ★ ペン入力で「L」など文字が入った場合の自動サニタイズ（クリア）関数
    def clean_number_input(input_key):
        val = st.session_state.get(input_key)
        if val is None:
            st.session_state[input_key] = 0

    cash_denom_def = [
        (50, "n_50_1", "Baht"),
        (10, "n_10", "Baht"),
        (20, "n_20", "Baht"),
        (50, "n_50_2", "Baht"),
        (100, "n_100", "Baht"),
        (500, "n_500", "Baht"),
        (1000, "n_1000b", "Baht"),
        (1000, "n_1000y", "Yen"),
    ]

    calc_baht_total = 0
    calc_yen_total = 0
    counts_dict = {}

    for denom, key, currency in cash_denom_def:
        c1, c2, c3, c4 = st.columns([1.5, 1.0, 2.5, 3.0])

        with c1:
            st.markdown(f"<p style='font-size:24px; font-weight:bold; text-align:right; margin-top:8px;'>{denom}</p>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<p style='font-size:22px; font-weight:bold; text-align:left; margin-top:8px;'>{currency}</p>", unsafe_allow_html=True)
        with c3:
            count_input = st.number_input(
                f"{key}", 
                min_value=0, 
                value=None, 
                step=1, 
                label_visibility="collapsed", 
                key=key,
                on_change=clean_number_input,
                args=(key,)
            )
            count = count_input if count_input is not None else 0
            counts_dict[key] = count
        with c4:
            subtotal = denom * count
            if currency == "Baht":
                calc_baht_total += subtotal
            else:
                calc_yen_total += subtotal
            st.markdown(
                f"""
<div style="background-color: #ffffff; border: 1.5px solid #000000; height: 52px; display: flex; align-items: center; justify-content: center; box-sizing: border-box;">
<span style="font-size: 24px; font-weight: bold; color: #000000;">{subtotal:,}</span>
</div>
""",
                unsafe_allow_html=True,
            )

    st.write("")

    c_label, c_baht_val, c_otsuri_label, c_otsuri_val, c_total_label, c_total_val = st.columns([2.5, 2.0, 2.0, 2.0, 1.5, 2.0])

    with c_label:
        st.markdown("<p style='font-size:20px; font-weight:bold; margin:0;'>ยอดเงินสดคงเหลือ<br>現金残高</p>", unsafe_allow_html=True)
    with c_baht_val:
        st.markdown(f"<div style='background-color:#ffffff; border:2px solid #000; text-align:center; padding:8px; font-size:24px; font-weight:bold; height:52px; display:flex; align-items:center; justify-content:center; box-sizing: border-box;'>{calc_baht_total:,} Baht</div>", unsafe_allow_html=True)

    with c_otsuri_label:
        st.markdown("<p style='font-size:18px; font-weight:bold; text-align:right; margin:0;'>เงินทอน<br>(おつり)</p>", unsafe_allow_html=True)
    with c_otsuri_val:
        otsuri_input = st.number_input(
            "おつり", 
            min_value=0, 
            value=None, 
            step=100, 
            label_visibility="collapsed", 
            key="otsuri_val",
            on_change=clean_number_input,
            args=("otsuri_val",)
        )
        otsuri = otsuri_input if otsuri_input is not None else 0

    with c_total_label:
        st.markdown("<p style='font-size:20px; font-weight:bold; text-align:center; margin-top:10px;'>Total</p>", unsafe_allow_html=True)
    with c_total_val:
        total_after_otsuri = calc_baht_total - otsuri
        st.markdown(f"<div style='background-color:#ffffff; border:2px solid #000; text-align:center; padding:8px; font-size:24px; font-weight:bold; height:52px; display:flex; align-items:center; justify-content:center; box-sizing: border-box;'>{total_after_otsuri:,}</div>", unsafe_allow_html=True)

    st.write("")
    cy_label, cy_val, cy_dummy1, cy_dummy2 = st.columns([2.5, 2.0, 4.0, 3.5])
    with cy_label:
        st.markdown("<p style='font-size:20px; font-weight:bold; margin:0;'>ยอดเงินสดคงเหลือ<br>現金残高</p>", unsafe_allow_html=True)
    with cy_val:
        st.markdown(f"<div style='background-color:#ffffff; border:2px solid #000; text-align:center; padding:8px; font-size:24px; font-weight:bold; height:52px; display:flex; align-items:center; justify-content:center; box-sizing: border-box;'>{calc_yen_total:,} Yen</div>", unsafe_allow_html=True)

    st.write("")
    st.write("")

    if st.button("💾 Save", use_container_width=True):
        with st.spinner("กำลังบันทึก... / 保存中..."):
            save_payload = {
                "action": "save_cash_only",
                "date": today_str,
                "counts": counts_dict,
                "otsuri": otsuri,
                "baht_total": calc_baht_total,
                "yen_total": calc_yen_total,
                "total_after_otsuri": total_after_otsuri
            }
            try:
                res = requests.post(GAS_URL, json=save_payload)
                res_j = res.json()
                if res_j.get("status") == "success":
                    st.success("✅ Saved successfully！")
                else:
                    st.error("Failed to save")
            except Exception as e:
                st.error(f"Failed to send: {e}")


# =========================================================
# 画面5：完了画面
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
    st.markdown(f"<h3>ชื่อ / お名前: {st.session_state.completed_name} san </h3>", unsafe_allow_html=True)

    st.markdown(f"<h2>หมายเลข / 受付番号: {st.session_state.ticket_id}</h2>", unsafe_allow_html=True)

    st.info("กรุณากรอกหมายเลขนี้ในใบเสร็จ / この番号をレシートにお書きください。")

    st.write("")
    st.write("")
    if st.button("ลงทะเบียนคนถัดไป / 次の人の受付をする"):
        st.session_state.step = "select_category"
        st.rerun()
