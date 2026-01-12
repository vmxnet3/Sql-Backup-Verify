# -*- coding: utf-8 -*-
import streamlit as st
import pyodbc
import os
import pandas as pd
import shutil
from datetime import datetime
import string

# --- MULTI-LANGUAGE DICTIONARY ---
LANG = {
    "EN": {
        "title": "Sql Backup Verify", "desc": "Verify .bak files using RESTORE VERIFYONLY.",
        "conn_settings": "SQL Server Connection Settings", "clean_settings": "Backup Cleanup",
        "drive_status": "Drive Status", "close_app": "Close Application",
        "start_date": "Start Date", "end_date": "End Date", "refresh": "Refresh",
        "verify_btn": "Start Verification", "success": "Success", "fail": "Failed",
        "waiting": "Waiting", "verifying": "Verifying", "done": "All tasks completed.",
        "no_select": "Please select at least one file.", "day": "Days", "delete": "Delete",
        "free_gb": "GB Free", "export": "Export Logs (TXT)", "path_label": "Backup Path"
    },
    "TR": {
        "title": "Sql Yedek Doğrulama", "desc": ".bak dosyalarını RESTORE VERIFYONLY ile doğrular.",
        "conn_settings": "SQL Server Bağlantı Ayarları", "clean_settings": "Yedek Temizliği",
        "drive_status": "Sürücü Durumu", "close_app": "Uygulamayı Kapat",
        "start_date": "Başlangıç", "end_date": "Bitiş", "refresh": "Yenile",
        "verify_btn": "Doğrulamayı Başlat", "success": "Başarılı", "fail": "Başarısız",
        "waiting": "Bekliyor", "verifying": "Doğrulanıyor", "done": "İşlem tamamlandı.",
        "no_select": "Lütfen seçim yapın.", "day": "Gün", "delete": "Sil",
        "free_gb": "GB Boş", "export": "Logları Dışa Aktar (TXT)", "path_label": "Yedek Yolu"
    }
}

LOG_FILE = "verify_logs.txt"

def write_log(filename, status):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{now} | {filename} | {status}\n")
    except: pass

st.set_page_config(page_title="Sql Backup Verify", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    :root { --primary-color: #4F6D7A; }
    .header-box { display: flex; align-items: baseline; gap: 10px; margin-top: -65px; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 25px; }
    .title-text { font-size: 22px; font-weight: bold; color: #2C3E50; margin: 0; }
    .desc-text { font-size: 13px; color: #95A5A6; margin: 0; }
    .stProgress > div > div > div > div { background-color: #4F6D7A !important; }
    input[type="checkbox"]:checked { background-color: #4F6D7A !important; }
    [data-testid="column"] { display: flex; align-items: flex-end; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    # Dil seçimi artık Bağlantı Ayarlarının üstünde ama daha entegre
    lang_choice = st.selectbox("Global Language / Dil", ["EN", "TR"], index=0)
    T = LANG[lang_choice]
    
    st.divider()
    st.write(f"**{T['conn_settings']}**")
    server = st.text_input("Server", value="localhost", label_visibility="collapsed")
    c_u, c_p = st.columns([1, 2])
    with c_u: user = st.text_input("User", value="sa")
    with c_p: pwd = st.text_input("Pass", type="password")
    
    # Backup Path default boş ve placeholderlı
    path = st.text_input(T['path_label'], value="", placeholder="C:\\Backups\\...", help="Enter the full path of your .bak files").replace("/", "\\")

    st.divider()
    st.write(f"**{T['clean_settings']}**")
    c_g, c_b = st.columns([0.6, 1])
    with c_g: gun = st.number_input(T['day'], min_value=1, value=7, label_visibility="collapsed")
    with c_b: 
        if st.button(T['delete'], use_container_width=True): st.warning("Cleanup active.")

    st.divider()
    st.write(f"**{T['drive_status']}**")
    for l in string.ascii_uppercase:
        d = f"{l}:\\"
        if os.path.exists(d):
            try:
                t, u, f = shutil.disk_usage(d)
                st.caption(f"{d} - {f // (2**30)} {T['free_gb']}")
                st.progress(1 - (f / t))
            except: continue

    st.write(" ")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            st.download_button(T['export'], f.read(), file_name=LOG_FILE, use_container_width=True)

    if st.button(T['close_app'], use_container_width=True): os._exit(0)
    st.caption("ugur.es | 2026 Free Edition")

# --- ANA PANEL ---
st.markdown(f'<div class="header-box"><p class="title-text">{T["title"]}</p><p class="desc-text">{T["desc"]}</p></div>', unsafe_allow_html=True)

def row_styler(row):
    if T['success'] in str(row.Durum): return ['background-color: #DDE5E8; color: #2C3E50; border-left: 5px solid #4F6D7A'] * len(row)
    if T['fail'] in str(row.Durum): return ['background-color: #EBDADA; color: #2C3E50; border-left: 5px solid #8D5B5B'] * len(row)
    return [''] * len(row)

bugun = datetime.now().date()
a1, a2, a3, _ = st.columns([1, 1, 0.5, 1.5]) 
with a1: start = st.date_input(T['start_date'], value=bugun)
with a2: end = st.date_input(T['end_date'], value=bugun)
with a3:
    st.markdown("<p style='margin-bottom: 28px;'></p>", unsafe_allow_html=True) 
    if st.button(T['refresh'], use_container_width=True):
        if 'main_df' in st.session_state: del st.session_state.main_df
        st.rerun()

# DOSYA TARAMA
if 'main_df' not in st.session_state:
    data = []
    if path and os.path.exists(path):
        for root, _, files in os.walk(path):
            for f in files:
                if f.lower().endswith('.bak'):
                    fp = os.path.join(root, f)
                    try:
                        dt = datetime.fromtimestamp(os.path.getmtime(fp)).date()
                        if start <= dt <= end:
                            sz = float(os.path.getsize(fp) / (1024**3))
                            data.append({"Dosya": f, "Tarih": dt, "Boyut (GB)": round(sz, 2), "Yol": fp, "Durum": T['waiting']})
                    except: continue
    st.session_state.main_df = pd.DataFrame(data) if data else pd.DataFrame()

# TABLO
if not st.session_state.main_df.empty:
    event = st.dataframe(
        st.session_state.main_df.style.apply(row_styler, axis=1).format({"Boyut (GB)": "{:.2f}"}), 
        use_container_width=True, on_select="rerun", selection_mode="multi-row", key="prod_table", hide_index=True
    )

    if st.button(T['verify_btn'], use_container_width=True):
        sel_indices = event.get("selection", {}).get("rows", [])
        if sel_indices:
            p_msg = st.empty()
            p_bar = st.progress(0)
            try:
                conn_str = f'DRIVER={{SQL Server}};SERVER={server};UID={user};PWD={pwd};'
                with pyodbc.connect(conn_str, timeout=10, autocommit=True) as conn:
                    cursor = conn.cursor()
                    for i, idx in enumerate(sel_indices):
                        fname = st.session_state.main_df.iloc[idx]["Dosya"]
                        fpath = st.session_state.main_df.iloc[idx]["Yol"]
                        p_msg.info(f"{T['verifying']}: {fname}")
                        p_bar.progress((i + 1) / len(sel_indices))
                        try:
                            cursor.execute("RESTORE VERIFYONLY FROM DISK = ?", fpath)
                            st.session_state.main_df.at[idx, "Durum"] = T['success']
                            write_log(fname, "SUCCESS")
                        except:
                            st.session_state.main_df.at[idx, "Durum"] = T['fail']
                            write_log(fname, "FAILED")
                p_msg.success(T['done'])
                st.rerun()
            except Exception as e: st.error(f"Error: {e}")