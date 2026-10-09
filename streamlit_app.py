import datetime
from datetime import datetime
import requests
import streamlit as st

# TODO: 下の "ここにGASのURLを貼り付け" を、ご自身のウェブアプリのURLに書き換えてください
GAS_URL = "https://script.google.com/macros/s/AKfycbyUJU4AzTrhulU6i_ncSTp6sd_wZ1FyVpbRu1MX5ecIJt5vvZADoa6sJ9NN3B7r9b7k/exec"

st.title("📝 受付システム")

# 1. 受付の種類を選ぶ
categories = [
    "向上",
    "向上相談",
    "相談",
    "特別相談",
    "鑑定",
    "初信(*)",
]
selected_category = st.selectbox("受付の種類を選んでください", categories)

# 初信(*)が選ばれた場合の追加項目
kai_suu = "-"
if selected_category == "初信(*)":
  kai_suu = st.selectbox(
      "何回目ですか？", ["1回目", "2回目", "3回目", "1年以上"]
  )

# 2. 基本情報の入力
name = st.text_input("お名前（※ペンまたはテキストで記入）")
language = st.selectbox("言語", ["日本語", "英語", "その他"])

# チェックボックス類
is_kanki = st.checkbox("歓喜以上であればチェックを入れてください")
is_priority = st.checkbox("優先（チェック欄）")

payment = st.radio("支払方法", ["QR", "Cash"])

# 送信ボタン
if st.button("受付を完了する"):
  if name.strip() == "":
    st.warning("お名前を入力してください。")
  else:
    # 現在の日時
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 送るデータをまとめる
    post_data = {
        "date": now,
        "category": selected_category,
        "name": name,
        "kaiSuu": kai_suu,
        "language": language,
        "isKanki": "〇" if is_kanki else "",
        "isPriority": "〇" if is_priority else "",
        "payment": payment,
    }

    try:
      # GASにデータを送信！
      response = requests.post(GAS_URL, json=post_data)

      if response.status_code == 200:
        st.success(f"{name} 様の受付を完了しました！")
      else:
        st.error("データの送信に失敗しました。")
    except Exception as e:
      st.error(f"エラーが発生しました: {e}")
