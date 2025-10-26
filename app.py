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

load_css("style.css")  # make sure your file is named styles.css

# ---- Header: Logo + Title (corporate dashboard style) ----
header = st.container()
with header:
    col_logo, col_title = st.columns([1, 6], vertical_alignment="center")

    with col_logo:
        logo_path = Path("logo.jpeg")  # or Path("assets/logo.png")
        if logo_path.exists():
            st.image(str(logo_path), width=300)
        else:
            # graceful fallback if the logo is missing
            st.markdown(
                "<div style='font-size:2rem;line-height:1;'>🗂️</div>",
                unsafe_allow_html=True
            )

    with col_title:
        # Using markdown keeps our CSS header styles intact
        st.markdown("<h1>Data Sharing Tool</h1>", unsafe_allow_html=True)
        st.markdown(
            "<h2>Enter the details below.</h2>",
            unsafe_allow_html=True
        )

# ---- Ensure storage and render form ----
ensure_data_dir()
submitted, payload = intake_form()

if submitted and payload is not None:
    append_entry(payload)
    st.success("Entry saved to data/entries.csv ✅")
    with st.expander("Preview last submission"):
        st.json(payload.model_dump())
