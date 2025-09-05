import pandas as pd
from urllib.parse import urlparse

# Read CSV
df = pd.read_csv("./top-1m 07 July 2025 to 05 August 2025 (30 days).csv")

# Convert Rank to numeric
df["no"] = pd.to_numeric(df["no"], errors="coerce")

# ✅ Deduplicate by Privacy Policy domain (internal only)
df = df.loc[
    df.groupby(df["domain"].str.lower().str.replace("^www\.", "", regex=True))["no"].idxmin()
]

# Define rank ranges
ranges = [
    ((1, 2000), 2000),
    ((2500, 100000), 22000),
    ((100001, 1000000), 30000),
]

# Collect samples
samples = []
for (low, high), n in ranges:
    subset = df[(df["no"] >= low) & (df["no"] <= high)]
    
    if len(subset) < n:
        print(f"⚠️ Range {low}-{high} only has {len(subset)} rows, sampling all instead of {n}.")
        sample = subset  # take all if not enough
    else:
        sample = subset.sample(n=n, random_state=42)
    
    samples.append(sample)

# Combine results
final_df = pd.concat(samples)

# Sort by rank
final_df = final_df.sort_values(by="no")

# Save without extra columns
final_df.to_csv("random_stratified_websites.csv", index=False)

print("✅ Saved random_stratified_websites.csv with unique Privacy Policy domains (lowest rank kept)")
