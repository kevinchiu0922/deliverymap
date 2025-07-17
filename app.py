
import streamlit as st
import pandas as pd
import folium
from io import BytesIO
from streamlit_folium import st_folium

st.set_page_config(page_title="地圖自動產生器", layout="wide")
st.title("📍 訂單地址自動地圖生成工具")

uploaded_file = st.file_uploader("請上傳包含地址的 Excel 檔案", type=["xls", "xlsx", "xlsm"])

if uploaded_file:
    st.success("檔案上傳成功，正在處理...")

    try:
        # 嘗試讀取檔案
        df = pd.read_excel(uploaded_file, sheet_name=None)
        sheet_names = list(df.keys())

        selected_sheet = st.selectbox("選擇工作表", sheet_names)
        df_sheet = df[selected_sheet]
git status


        # 自動偵測是否有「地址」欄位
        address_col = None
        for col in df_sheet.columns:
            if "地址" in str(col):
                address_col = col
                break

        if address_col is None:
            st.error("找不到地址欄位，請確認欄位名稱有包含『地址』")
        else:
            st.info(f"使用地址欄位：「{address_col}」")

            # 假設中心點為台北，製作基礎地圖
            map_center = [25.05, 121.55]
            m = folium.Map(location=map_center, zoom_start=11)

            # 模擬轉換經緯度（真實版應串接 geocoding API）
            import hashlib
            def fake_geocode(address):
                h = int(hashlib.md5(address.encode()).hexdigest(), 16)
                lat = 25 + (h % 1000) * 0.0001
                lng = 121 + ((h // 1000) % 1000) * 0.0001
                return lat, lng

            for i, row in df_sheet.iterrows():
                address = str(row[address_col])
                if not address or address == "nan":
                    continue
                lat, lng = fake_geocode(address)
                folium.Marker(
                    location=[lat, lng],
                    popup=address,
                    tooltip=f"地址：{address}",
                    icon=folium.Icon(color="blue", icon="home")
                ).add_to(m)

            st_folium(m, width=1000, height=600)

    except Exception as e:
        st.error(f"處理檔案時發生錯誤：{e}")
