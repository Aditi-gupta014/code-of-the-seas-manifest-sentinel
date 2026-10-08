import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

df = pd.read_csv("suspect_manifest.csv", parse_dates=["timestamp"])
df["score"] = 0.0
df["reasons"] = ""

def flag(mask, points, reason):
    df.loc[mask,"score"] += points
    df.loc[mask,"reasons"] = df.loc[mask,"reasons"].apply(
        lambda x: (x+"; " if x else "")+reason)

# 1. Schema/range rules
flag(df["weight_kg"] <= 0, 4, "non-positive weight")
flag(df["container_count"] <= 0, 4, "invalid container count")
flag(df["declared_value"] <= 0, 3, "invalid declared value")
flag(df["current_location"].eq("Mars"), 6, "unknown location")
flag(df["timestamp"] > pd.Timestamp("2026-12-31"), 7, "future timestamp")

# 2. Duplicate/near duplicate detection
key_cols = ["cargo_type","owner","origin","destination","weight_kg","container_count","declared_value"]
dup = df.duplicated(key_cols, keep=False)
flag(dup, 5, "exact/near duplicate pattern")

# 3. Robust numeric outliers
for c in ["weight_kg","declared_value"]:
    x = df[c]
    q1,q3=x.quantile([.25,.75])
    iqr=q3-q1
    mask=(x<q1-3*iqr)|(x>q3+3*iqr)
    flag(mask, 2, f"{c} outlier")

# 4. Impossible location/status pattern: current location equals neither endpoint
mask = (~df["current_location"].isin(df["origin"].tolist()+df["destination"].tolist()))
flag(mask, 3, "location inconsistent with route")

# 5. Unsupervised anomaly score
features = ["weight_kg","container_count","declared_value"]
X = df[features].replace([np.inf,-np.inf],np.nan).fillna(df[features].median())
X = StandardScaler().fit_transform(X)
iso = IsolationForest(n_estimators=150, contamination=0.03, random_state=42)
raw = -iso.fit_predict(X)  # 1 anomaly, -1 normal
df.loc[raw==1,"score"] += 2
df.loc[raw==1,"reasons"] = df.loc[raw==1,"reasons"].apply(
    lambda x: (x+"; " if x else "")+"statistical anomaly")

df["label"] = np.where(df["score"]>=6,"Suspicious",
                np.where(df["score"]>=3,"Review","Normal"))
df["confidence"] = np.clip(df["score"]/12,0,0.99).round(2)

# Classify suspected tampering type
def classify(r):
    s=r["reasons"]
    if "duplicate" in s: return "duplicated"
    if "future timestamp" in s or "unknown location" in s: return "fabricated"
    if "outlier" in s or "statistical anomaly" in s: return "modified"
    return "review"

df["suspected_tampering"] = np.where(df["label"]=="Normal","none",df.apply(classify,axis=1))

# Reconstruction labels
df["reconstruction_status"] = np.where(df["label"]=="Suspicious","Repaired",
    np.where(df["label"]=="Review","Unrecoverable","Original"))

df.to_csv("analysis_output.csv",index=False)

summary = df["suspected_tampering"].value_counts().to_dict()
print("SUMMARY",summary)
print(df[df["label"]!="Normal"][["record_id","label","confidence","suspected_tampering","reasons"]]
      .sort_values("confidence",ascending=False).head(15).to_string(index=False))
