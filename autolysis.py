import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import requests

# === Predefined Inputs ===
AIPROXY_TOKEN = "your_aiproxy_token_here"  # Replace with your actual OpenAI token
CSV_FILE_PATH = "path_to_your_csv_file.csv"  # Replace with the full path to your CSV file

# Validate inputs
if not os.path.exists(CSV_FILE_PATH):
    raise FileNotFoundError(f"The specified file does not exist: {CSV_FILE_PATH}")

# Output directory setup
filename = os.path.basename(CSV_FILE_PATH)
out_dir = filename.split('.')[0]
os.makedirs(out_dir, exist_ok=True)

# Read the CSV file
try:
    data = pd.read_csv(CSV_FILE_PATH, encoding="utf-8")
    print(f"Successfully loaded {filename} with UTF-8 encoding")
except UnicodeDecodeError:
    data = pd.read_csv(CSV_FILE_PATH, encoding="ISO-8859-1")
    print(f"Successfully loaded {filename} with ISO-8859-1 encoding")

# Show basic info about the data
print("Dataset Overview:")
print(data.info())
print("First 5 Rows:")
print(data.head())

# Analyze missing values
missing_values = data.isnull().sum()
print("\nMissing Values:")
print(missing_values[missing_values > 0])

# Handle missing values
print("\nHandling Missing Values:")
for column in missing_values.index:
    if data[column].dtype in ["float64", "int64"]:  # Numerical columns
        data[column].fillna(data[column].mean(), inplace=True)
        print(f"Filled missing values in '{column}' with mean: {data[column].mean()}")
    elif data[column].dtype == "object":  # Categorical columns
        data[column].fillna(data[column].mode()[0], inplace=True)
        print(f"Filled missing values in '{column}' with mode: {data[column].mode()[0]}")

# Correlation matrix for numerical columns
numerical_columns = data.select_dtypes(include=["float64", "int64"])  # Select only numeric columns
correlation_matrix = numerical_columns.corr()
print("\nCorrelation Matrix:")
print(correlation_matrix)

# Save the correlation heatmap as a PNG file
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
plt.title("Correlation Matrix Heatmap")
plt.savefig(f"{out_dir}/correlation_matrix.png")
print(f"Correlation heatmap saved as '{out_dir}/correlation_matrix.png'")

# Outlier detection using Isolation Forest
print("\nDetecting Outliers with Isolation Forest:")
if "average_rating" in numerical_columns and "ratings_count" in numerical_columns:
    features = numerical_columns[["average_rating", "ratings_count"]]
else:
    features = numerical_columns.iloc[:, :2]  # Use first two numeric columns if specific ones are missing
isolation_forest = IsolationForest(random_state=42, contamination=0.05)
isolation_forest.fit(features)

# Predict anomalies (1 for inliers, -1 for outliers)
predictions = isolation_forest.predict(features)
data["is_outlier"] = predictions
outliers = data[data["is_outlier"] == -1]

print(f"Number of outliers detected: {len(outliers)}")

# Visualize inliers vs. outliers
plt.figure(figsize=(8, 6))
sns.scatterplot(
    x=features.iloc[:, 0],
    y=features.iloc[:, 1],
    hue=predictions,
    palette={1: "blue", -1: "red"},
    legend="full"
)
plt.title("Isolation Forest Outlier Detection")
plt.xlabel(features.columns[0])
plt.ylabel(features.columns[1])
plt.savefig(f"{out_dir}/outliers.png")
print(f"Outlier visualization saved as '{out_dir}/outliers.png'")

# Clustering Analysis
print("\nPerforming Clustering Analysis:")
pca = PCA(n_components=2)
reduced_features = pca.fit_transform(features)
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(reduced_features)

# Visualize clusters
plt.figure(figsize=(8, 6))
sns.scatterplot(
    x=reduced_features[:, 0], y=reduced_features[:, 1], hue=clusters, palette="viridis")
plt.title("Clustering Visualization")
plt.savefig(f"{out_dir}/clustering.png")
print(f"Clustering visualization saved as '{out_dir}/clustering.png'")

# Use GPT-4o-Mini to narrate the story
print("\nGenerating README.md using GPT-4o-Mini...")
story_prompt = f"""
You are an expert data analyst. Write a story about the analysis of a dataset. Include:
1. A brief description of the dataset.
2. The types of analysis performed (missing values, outliers, clustering).
3. Key findings and insights.
4. Implications and suggestions based on the findings.

The dataset contains the following columns: {', '.join(data.columns)}.
The analysis included:
- Missing value handling.
- Correlation analysis.
- Outlier detection using Isolation Forest.
- Clustering using K-Means.

Provide the response in Markdown format.
"""

# Proxy API endpoint and headers
proxy_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AIPROXY_TOKEN}",
}

# Chat Completion Data
request_data = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "You are an expert data analyst."},
        {"role": "user", "content": story_prompt},
    ],
}

# API Request to the Proxy
response = requests.post(proxy_url, headers=headers, json=request_data)
if response.status_code == 200:
    readme_content = response.json()["choices"][0]["message"]["content"]
    with open(f"{out_dir}/README.md", "w") as f:
        f.write(readme_content)
    print(f"README.md generated and saved as '{out_dir}/README.md'")
else:
    print(f"Error: {response.status_code}, {response.text}")

