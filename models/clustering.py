from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def run_clustering(df):
    # Use only the columns that exist
    features = df[["CallSuccessRate", "EngagementScoreNorm"]]
    X = StandardScaler().fit_transform(features)

    kmeans = KMeans(n_clusters=3, random_state=42)
    df["Cluster"] = kmeans.fit_predict(X)

    # Label clusters based on call success rate
    cluster_means = df.groupby("Cluster")[["CallSuccessRate"]].mean()
    def label(row):
        if row["Cluster"] == cluster_means["CallSuccessRate"].idxmin():
            return "High Priority"
        elif row["Cluster"] == cluster_means["CallSuccessRate"].idxmax():
            return "Engaged"
        else:
            return "Monitor"
    df["ClusterLabel"] = df.apply(label, axis=1)

    return df, X
