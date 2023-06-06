from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


def find_outliers(trajectories: dict, n_clusters:int, outlier_threshold):
    ids = list(trajectories.keys())
    slopes = list(trajectories.values())

    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=20).fit(slopes)
    centers = kmeans.cluster_centers_

    distances = pairwise_distances_argmin_min(slopes, centers)

    outliers = [ids[i] for i, dist in enumerate(distances[0]) if dist > outlier_threshold]
    return outliers
