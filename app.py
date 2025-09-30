import streamlit as st
from ui.components.form import intake_form
from services.storage import append_entry, ensure_data_dir


st.set_page_config(page_title="CDL Intake UI", page_icon="🗂️", layout="centered")
st.title("Data Sharing Tool")


ensure_data_dir()


submitted, payload = intake_form()


if submitted and payload is not None:
    append_entry(payload)
    st.success("Entry saved to data/entries.csv ✅")
    with st.expander("Preview last submission"):
        st.json(payload.model_dump())