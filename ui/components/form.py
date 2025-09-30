import streamlit as st
from datetime import date
from core.models import CDLIntake
from core.validators import all_required_present

STREAM_OPTIONS = ["— Select —", "AI", "Climate", "Fintech", "Health", "Space", "Quantum", "Other"]


def intake_form():
    with st.form(key="cdl-intake-form", border=True):
        col1, col2 = st.columns(2)
        with col1:
            date_value: date | None = st.date_input(
                "Date",
                value=None,
                format="YYYY-MM-DD",
                help="Meeting date",
            )
        with col2:
            stream = st.selectbox(
                "CDL Stream",
                STREAM_OPTIONS,
                index=0,
                help="Select the stream (e.g., AI, Climate)",
            )

        founder_name = st.text_input("Founder name", placeholder="Jane Doe")
        venture_name = st.text_input("Venture name", placeholder="Acme Robotics")
        venture_manager_name = st.text_input("Venture manager name", placeholder="Alex Manager")
        link = st.text_input("Link", placeholder="https://example.com")
        comments = st.text_area("Comments (optional)")

        # Pre-validate to control the disabled state of the button
        is_ready, missing = all_required_present(
            date_value=date_value,
            stream=stream,
            founder_name=founder_name,
            venture_name=venture_name,
            venture_manager_name=venture_manager_name,
            link=link,
        )

        if not is_ready:
            st.caption(
                "❗ Fill all required fields to enable submit: " + ", ".join(missing)
            )

        submitted = st.form_submit_button("Submit", type="primary", disabled=not is_ready)

    payload = None

    if submitted:
        try:
            # Pydantic gives strict validation (esp. URL)
            payload = CDLIntake(
                date=date_value,
                stream=stream if stream != "— Select —" else "",
                founder_name=founder_name,
                venture_name=venture_name,
                venture_manager_name=venture_manager_name,
                link=link,
                comments=comments or None,
            )
        except Exception as e:
            st.error(f"Validation error: {e}")
            submitted = False

    return submitted, payload