import streamlit as st
import plotly.express as px
from services.alerts import check_latency

def show_page():
    st.title("Module 2.2 – Care Access Latency")

    # Example demo data
    data = [
        {"PatientID": 1, "Latency": 120},
        {"PatientID": 2, "Latency": 250},
        {"PatientID": 3, "Latency": 400},
    ]

    for record in data:
        status = check_latency(record["Latency"])
        st.write(f"Patient {record['PatientID']} → {record['Latency']}s → {status}")

    # Simple chart
    fig = px.bar(data, x="PatientID", y="Latency", color=[check_latency(d["Latency"]) for d in data])
    st.plotly_chart(fig)
