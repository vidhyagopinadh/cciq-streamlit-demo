import streamlit as st
import plotly.express as px
from data_pipeline.db_connection import fetch_engagement_data
from data_pipeline.feature_engineering import add_engagement_features
from models.clustering import run_clustering
from models.validation import validate_clusters

def show_page():
    st.title("Module 2.1 – Patient Engagement")

    df = fetch_engagement_data()
    df = add_engagement_features(df)
    df, X = run_clustering(df)

    score = validate_clusters(X, df["Cluster"])
    st.write(f"Silhouette Score: {score:.2f}")

    fig = px.scatter(df, x="CallSuccessRate", y="DaysWithMeasurements",
                     color="ClusterLabel", size="EngagementScoreNorm",
                     hover_data=["PatientID"])
    st.plotly_chart(fig)

    st.subheader("High Priority Patients")
    hp = df[df["ClusterLabel"]=="High Priority"][["PatientID","EngagementScoreNorm"]]
    st.dataframe(hp)
