import streamlit.web.cli as stcli
import os, sys

def resolve_path(path):
    # PyInstaller ile .exe yapildiginda dosya yollarinin sasmamasi için gerekli
    if getattr(sys, 'frozen', False):
        resolved_path = os.path.join(sys._MEIPASS, path)
    else:
        resolved_path = os.path.join(os.getcwd(), path)
    return resolved_path

if __name__ == "__main__":
    # Ana uygulama dosyanizin adi sql_verify.py ise burayi o sekilde güncelliyoruz
    target_file = resolve_path("sql_verify.py")
    
    # Streamlit komutunu simüle eder: streamlit run sql_verify.py
    sys.argv = [
        "streamlit",
        "run",
        target_file,
        "--global.developmentMode=false",
    ]
    
    sys.exit(stcli.main())