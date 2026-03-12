def add_engagement_features(df):
    df["CallSuccessRate"] = df["AnsweredQuestions"] / df["TotalCalls"].replace(0,1)
    df["EngagementScoreNorm"] = 100 * (df["WeightedEngagementScore"] / df["WeightedEngagementScore"].max())
    return df
