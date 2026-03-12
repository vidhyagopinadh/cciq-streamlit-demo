import streamlit as st
import plotly.express as px
import pandas as pd
from data_pipeline.db_connection import fetch_engagement_data
from data_pipeline.feature_engineering import add_engagement_features
from models.clustering import run_clustering
from models.validation import validate_clusters

def show_page():
    st.title("Module 2.1 – Patient Engagement")

    # Fetch and process data
    df = fetch_engagement_data()
    df = add_engagement_features(df)
    df, X = run_clustering(df)

    # Validation metric
    score = validate_clusters(X, df["Cluster"])
    st.write(f"Silhouette Score: {score:.2f}")

    # --- KPIs ---
    st.subheader("Overall Engagement Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Patients", len(df))
    col2.metric("Total Calls", int(df["TotalCalls"].sum()))
    col3.metric("Answered Questions", int(df["AnsweredQuestions"].sum()))
    col4.metric("Avg Call Duration (s)", round(df["AvgCallDuration"].mean(), 2))

    # --- Scatter Plot ---
    st.subheader("Patient Distribution")
    fig_scatter = px.scatter(
        df,
        x="CallSuccessRate",
        y="EngagementScoreNorm",
        color="ClusterLabel",
        size="TotalCalls",
        hover_data=["PatientId","AnsweredQuestions","AvgCallDuration"]
    )
    st.plotly_chart(fig_scatter)

    # --- Cluster Comparison ---
    st.subheader("Cluster Comparison")
    cluster_summary = df.groupby("ClusterLabel")[["TotalCalls","AnsweredQuestions","EngagementScoreNorm"]].mean().reset_index()
    fig_bar = px.bar(cluster_summary, x="ClusterLabel", y="EngagementScoreNorm", color="ClusterLabel",
                     text="EngagementScoreNorm", title="Average Engagement Score per Cluster")
    st.plotly_chart(fig_bar)

    # --- Trend Line (if call date available) ---
    if "MostRecentCall" in df.columns:
        try:
            df["CallDate"] = pd.to_datetime(df["MostRecentCall"])
            trend = df.groupby([df["CallDate"].dt.to_period("W"), "ClusterLabel"])["EngagementScoreNorm"].mean().reset_index()
            trend["CallDate"] = trend["CallDate"].astype(str)

            fig_line = px.line(trend, x="CallDate", y="EngagementScoreNorm", color="ClusterLabel",
                               title="Weekly Engagement Trends by Cluster")
            st.subheader("Engagement Trends")
            st.plotly_chart(fig_line)
        except Exception as e:
            st.warning("Trend line could not be generated: " + str(e))

    # --- Patient Table ---
    st.subheader("Patient Engagement Details")
    st.dataframe(df[["PatientId","TotalCalls","AnsweredQuestions","CallSuccessRate","EngagementScoreNorm","ClusterLabel"]])
