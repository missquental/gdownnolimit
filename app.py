import streamlit as st
import gdown
import os
from pathlib import Path

# ===============================
# KONFIGURASI
# ===============================
DEFAULT_DRIVE_FOLDER = "https://drive.google.com/drive/folders/11FjfDb7j1QNFy4R0wwE_0OSi9iABN3hR"

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

# ===============================
# UI STREAMLIT
# ===============================
st.set_page_config(page_title="Google Drive Folder Downloader", layout="centered")

st.title("📥 Google Drive Folder Downloader")
st.write("Download **SEMUA video/file** dari Google Drive folder tanpa batas.")

drive_url = st.text_input(
    "🔗 Google Drive Folder URL",
    value=DEFAULT_DRIVE_FOLDER
)

folder_name = st.text_input(
    "📁 Nama Folder Output",
    value="drive_videos"
)

download_btn = st.button("🚀 Mulai Download")

status_box = st.empty()
log_box = st.empty()

# ===============================
# FUNGSI DOWNLOAD
# ===============================
def download_drive_folder(url, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)

    status_box.info("🔄 Mengambil data dari Google Drive...")
    
    # download folder recursive
    gdown.download_folder(
        url=url,
        output=str(output_dir),
        quiet=False,
        use_cookies=False
    )

    status_box.success("✅ Download selesai!")

# ===============================
# ACTION
# ===============================
if download_btn:
    if not drive_url.strip():
        st.error("⚠️ URL folder tidak boleh kosong")
    else:
        output_path = DOWNLOAD_DIR / folder_name

        with st.spinner("⏳ Sedang mendownload semua file..."):
            try:
                download_drive_folder(drive_url, output_path)

                files = list(output_path.rglob("*"))
                files = [f for f in files if f.is_file()]

                st.success(f"🎉 Total file terdownload: {len(files)}")

                with st.expander("📄 Daftar File"):
                    for f in files:
                        st.write(f"• {f.name}")

            except Exception as e:
                st.error(f"❌ Terjadi error: {e}")
