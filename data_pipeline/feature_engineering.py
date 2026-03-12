def add_engagement_features(df):
    df["CallSuccessRate"] = df["AnsweredCalls"] / df["TotalCalls"].replace(0,1)
    df["WeightedEngagementScore"] = (df["TotalCalls"] * 0.4) + (df["DaysWithMeasurements"] * 0.6)
    df["EngagementScoreNorm"] = 100 * (df["WeightedEngagementScore"] / df["WeightedEngagementScore"].max())
    return df
