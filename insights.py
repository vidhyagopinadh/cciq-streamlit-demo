import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression

# ---------- 2.1 Engagement Metrics ----------
def engagement_metrics(unified_df):
    call_counts = unified_df.groupby("PatientId")["CallRecordId"].nunique().reset_index(name="TotalCalls")
    answered_calls = unified_df[unified_df["Score"].notnull()].groupby("PatientId")["CallRecordId"].nunique().reset_index(name="AnsweredCalls")
    call_success = call_counts.merge(answered_calls, on="PatientId", how="left").fillna(0)
    call_success["CallSuccessRate"] = call_success["AnsweredCalls"] / call_success["TotalCalls"]

    vitals = unified_df.groupby("PatientId")["DaysWithMeasurements"].max().reset_index()
    merged = call_success.merge(vitals, on="PatientId", how="left").fillna(0)
    merged["EngagementScore"] = (merged["TotalCalls"] * 0.4) + (merged["DaysWithMeasurements"] * 0.6)

    if len(merged) >= 3:
        kmeans = KMeans(n_clusters=3, random_state=42)
        merged["cluster"] = kmeans.fit_predict(merged[["EngagementScore", "CallSuccessRate"]])
    else:
        merged["cluster"] = 0

    cluster_map = {0: "High Priority", 1: "Monitor", 2: "Engaged"}
    merged["ClusterLabel"] = merged["cluster"].map(cluster_map)
    return merged

def engagement_trend(unified_df):
    df = engagement_metrics(unified_df)
    df["Week"] = pd.to_datetime(unified_df["CallStart"]).dt.to_period("W").dt.start_time
    return df.groupby("Week").agg(AvgEngagementScore=("EngagementScore", "mean")).reset_index()

# ---------- 2.2 Care Access Latency ----------
def care_access_latency(unified_df):
    df = unified_df.copy()
    df["LatencySec"] = (pd.to_datetime(df["PickupTime"]) - pd.to_datetime(df["CallStart"])).dt.total_seconds()
    df["LatencySec"] = df["LatencySec"].fillna(0)

    def classify_latency(x):
        if x > 300: return "Critical"
        elif x > 180: return "Warning"
        else: return "Normal"
    df["AlertType"] = df["LatencySec"].apply(classify_latency)

    clinician_summary = df.groupby("DestinationPhone").agg(
        AvgLatencySec=("LatencySec", "mean"),
        CriticalBreaches=("AlertType", lambda x: (x == "Critical").sum()),
        WarningBreaches=("AlertType", lambda x: (x == "Warning").sum()),
        TotalCalls=("CallRecordId", "nunique")
    ).reset_index()

    df["Week"] = pd.to_datetime(df["CallStart"]).dt.to_period("W").dt.start_time
    trend = df.groupby("Week").agg(AvgLatencySec=("LatencySec", "mean")).reset_index()

    return df[["PatientId", "DestinationPhone", "LatencySec", "AlertType", "Week"]], clinician_summary, trend

# ---------- 2.3 Clinician Workload ----------
def clinician_workload(unified_df):
    df = unified_df.copy()
    df["CallDurationSec"] = pd.to_timedelta(df["CallDuration"]).dt.total_seconds()

    workload = df.groupby("DestinationPhone").agg(
        TotalCalls=("CallRecordId", "nunique"),
        TotalDuration=("CallDurationSec", "sum"),
        AvgCallDuration=("CallDurationSec", "mean")
    ).reset_index()

    if len(workload) > 1:
        X = workload[["TotalCalls"]]
        y = workload["TotalDuration"]
        model = LinearRegression().fit(X, y)
        workload["PredictedDuration"] = model.predict(X)
    else:
        workload["PredictedDuration"] = workload["TotalDuration"]

    df["Week"] = pd.to_datetime(df["CallStart"]).dt.to_period("W").dt.start_time
    trend = df.groupby("Week").agg(TotalWorkload=("CallDurationSec", "sum")).reset_index()

    return workload, trend

# ---------- 2.4 Care Outreach Patterns ----------
def care_outreach_patterns(unified_df):
    df = unified_df.copy()
    df["hour"] = pd.to_datetime(df["CallStart"]).dt.hour
    df["CallDurationSec"] = pd.to_timedelta(df["CallDuration"]).dt.total_seconds()

    outreach = df.groupby(["hour", "Direction"]).agg(
        AvgDuration=("CallDurationSec", "mean"),
        CallVolume=("CallRecordId", "nunique")
    ).reset_index()

    df["Week"] = pd.to_datetime(df["CallStart"]).dt.to_period("W").dt.start_time
    trend = df.groupby("Week").agg(TotalCalls=("CallRecordId", "nunique")).reset_index()

    return outreach, trend
