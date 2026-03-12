from sklearn.metrics import silhouette_score

def validate_clusters(X, labels):
    return silhouette_score(X, labels)
