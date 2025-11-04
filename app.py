import streamlit as st
from ui.components.form import intake_form
from services.storage import append_entry, ensure_data_dir
from pathlib import Path
import base64

st.set_page_config(page_title="CDL Intake UI", page_icon="🗂️", layout="wide")

def load_css(path: str = "style.css"):
    css = Path(path)
    if css.exists():
        st.markdown(f"<style>{css.read_text()}</style>", unsafe_allow_html=True)

load_css("style.css")

# --- Force banner styling no matter what's in style.css ---
st.markdown("""
<style>
/* Scope to this banner only */
.hero-banner { position: relative; width: 100%; height: 260px;
  border-radius: 18px; overflow: hidden; box-shadow: 0 8px 30px rgba(0,0,0,.08); }
.hero-banner img { width: 100% !important; height: 100% !important;
  object-fit: cover !important; display: block; }
/* If you still have global img rules, this resets Streamlit image widgets */
div[data-testid="stImage"] img { max-width: 100% !important; height: auto !important; }
</style>
""", unsafe_allow_html=True)

def img_b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()

# ---- Header: Banner + Title ----
photo_path = Path("logo.jpeg")  # replace if needed
if photo_path.exists():
    b64 = img_b64(photo_path)
    st.markdown(
        f"""
        <div class="hero-banner">
          <img src="data:image/jpeg;base64,{b64}">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.info(f"Banner not found at: {photo_path.resolve()}")

st.markdown(
    """
    <div style='text-align:center; margin-top:1rem;'>
        <h1 style='margin-bottom:0;'>Data Sharing Tool</h1>
        <h2 style='color:gray; font-weight:400;'>Enter the details below.</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# ---- Form ----
ensure_data_dir()
submitted, payload = intake_form()
if submitted and payload is not None:
    append_entry(payload)
    st.success("Entry saved and synced ✅")
    with st.expander("Preview last submission"):
        st.json(payload.model_dump())
