import streamlit as st
from dashboard.pages import engagement, latency

def run_dashboard():
    st.sidebar.title("ChronicCareIQ Portal")
    page = st.sidebar.radio("Select Module", ["Engagement (2.1)", "Latency (2.2)"])

    if page == "Engagement (2.1)":
        engagement.show_page()
    elif page == "Latency (2.2)":
        latency.show_page()
