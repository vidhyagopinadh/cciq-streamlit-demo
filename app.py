import streamlit as st
import plotly.express as px
from data_loader import get_unified_data
from insights import (
    engagement_metrics, engagement_trend,
    care_access_latency,
    clinician_workload,
    care_outreach_patterns
)

st.set_page_config(page_title="ChronicCareIQ AI Dashboard", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to section:",
    [
        "2.1 Engagement Metrics",
        "2.2 Care Access Latency",
        "2.3 Clinician Workload",
        "2.4 Care Outreach Patterns",
        "Unified Data View"
    ]
)

df_unified = get_unified_data()

# ---------------- 2.1 Engagement Metrics ----------------
if page == "2.1 Engagement Metrics":
    st.header("2.1 Patient Engagement Metrics")
    engagement = engagement_metrics(df_unified)

    fig1 = px.scatter(engagement, x="CallSuccessRate", y="EngagementScore",
                      color="ClusterLabel", hover_data=["PatientId"],
                      title="Patient Engagement Clusters")
    st.plotly_chart(fig1, use_container_width=True)

    fig_pie = px.pie(engagement, names="ClusterLabel", title="Cluster Distribution")
    st.plotly_chart(fig_pie, use_container_width=True)

    trend = engagement_trend(df_unified)
    fig_trend = px.line(trend, x="Week", y="AvgEngagementScore", markers=True,
                        title="Weekly Average Engagement Score")
    st.plotly_chart(fig_trend, use_container_width=True)

    st.dataframe(engagement)

# ---------------- 2.2 Care Access Latency ----------------
elif page == "2.2 Care Access Latency":
    st.header("2.2 Care Access Latency")
    latency, clinician_summary, trend = care_access_latency(df_unified)

    fig_latency = px.histogram(latency, x="LatencySec", color="AlertType",
                               title="Latency Distribution", nbins=30)
    fig_latency.add_vline(x=300, line_dash="dash", line_color="red", annotation_text="SLA Breach > 300s")
    st.plotly_chart(fig_latency, use_container_width=True)

    fig_clinician = px.bar(clinician_summary, x="DestinationPhone", y="AvgLatencySec",
                           color="CriticalBreaches", title="Average Latency per Clinician")
    st.plotly_chart(fig_clinician, use_container_width=True)

    fig_trend = px.line(trend, x="Week", y="AvgLatencySec", markers=True,
                        title="Weekly Average Latency")
    fig_trend.add_hline(y=300, line_dash="dash", line_color="red", annotation_text="SLA Threshold")
    st.plotly_chart(fig_trend, use_container_width=True)

    st.dataframe(latency)
    st.dataframe(clinician_summary)

# ---------------- 2.3 Clinician Workload ----------------
elif page == "2.3 Clinician Workload":
    st.header("2.3 Clinician Workload")
    workload, trend = clinician_workload(df_unified)

    fig_workload = px.bar(workload, x="DestinationPhone", y="TotalDuration",
                          color="TotalCalls", title="Clinician Workload (Duration vs Calls)")
    st.plotly_chart(fig_workload, use_container_width=True)

    fig_regression = px.scatter(workload, x="TotalCalls", y="TotalDuration",
                            title="Calls vs Duration")
    fig_regression.add_traces(px.line(workload, x="TotalCalls", y="PredictedDuration").data)
    st.plotly_chart(fig_regression, use_container_width=True)

    fig_trend = px.line(trend, x="Week", y="TotalWorkload", markers=True,
                        title="Weekly Total Workload")
    st.plotly_chart(fig_trend, use_container_width=True)

    st.dataframe(workload)

# ---------------- 2.4 Care Outreach Patterns ----------------
elif page == "2.4 Care Outreach Patterns":
    st.header("2.4 Care Outreach Patterns")
    outreach, trend = care_outreach_patterns(df_unified)

    # Heatmap of outreach patterns
    fig_heatmap = px.density_heatmap(outreach, x="hour", y="Direction",
                                     z="AvgDuration", color_continuous_scale="Viridis",
                                     title="Outreach Patterns (Avg Duration by Hour & Direction)")
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Bar chart of call volume by direction
    fig_bar = px.bar(outreach, x="Direction", y="CallVolume", color="hour",
                     title="Call Volume by Direction and Hour")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Weekly trend of call volume
    fig_trend = px.line(trend, x="Week", y="TotalCalls", markers=True,
                        title="Weekly Call Volume Trend")
    st.plotly_chart(fig_trend, use_container_width=True)

    st.dataframe(outreach)
    st.dataframe(trend)

# ---------------- Unified Data View ----------------
elif page == "Unified Data View":
    st.header("📑 Unified Data View — Joined Tables")
    st.dataframe(df_unified)

    st.subheader("Summary Statistics")
    st.write(df_unified.describe(include="all"))

    # Quick latency distribution
    fig_latency = px.histogram(df_unified, x="LatencySec", color="PatientId",
                               title="Latency Distribution (Joined Data)")
    st.plotly_chart(fig_latency, use_container_width=True)

    # Engagement scatter
    if "Score" in df_unified.columns:
        fig_engagement = px.scatter(df_unified, x="DaysWithMeasurements", y="Score",
                                    color="PatientId", title="Vitals vs Survey Score")
        st.plotly_chart(fig_engagement, use_container_width=True)