import streamlit as st
from ui.components.form import intake_form
from services.storage import append_entry, ensure_data_dir
from pathlib import Path

# ---- Page config FIRST (before any Streamlit output) ----
st.set_page_config(page_title="CDL Intake UI", page_icon="🗂️", layout="centered")

# ---- Load custom CSS ----
def load_css(path: str = "style.css"):
    css_file = Path(path)
    if css_file.exists():
        st.markdown(f"<style>{css_file.read_text()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Custom CSS not found at: {css_file.resolve()}")

load_css("style.css")

# ---- Header: Image + Title ----
header = st.container()
with header:
    photo_path = Path("banner.jpeg")  # <-- your image file (rename as needed)
    if photo_path.exists():
        st.image(str(photo_path), use_container_width=True)
    else:
        st.markdown("<div style='font-size:2rem;'>🗂️</div>", unsafe_allow_html=True)

    # Centered title + subtitle below image
    st.markdown(
        """
        <div style='text-align:center; margin-top:1rem;'>
            <h1 style='margin-bottom:0;'>Data Sharing Tool</h1>
            <h2 style='color:gray; font-weight:400;'>Enter the details below.</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---- Ensure storage and render form ----
ensure_data_dir()
submitted, payload = intake_form()

if submitted and payload is not None:
    append_entry(payload)
    st.success("Entry saved and synced ✅")
    with st.expander("Preview last submission"):
        st.json(payload.model_dump())
