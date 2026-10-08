import pandas as pd
import numpy as np

SEED = 42
rng = np.random.default_rng(SEED)

clean = pd.read_csv("clean_manifest.csv", parse_dates=["timestamp"])
suspect = clean.copy()
truth = []

# Modified records
for idx in rng.choice(suspect.index, 25, replace=False):
    old = suspect.loc[idx, "weight_kg"]
    suspect.loc[idx, "weight_kg"] = round(float(old * rng.uniform(2.5,5.0)),2)
    truth.append({"record_id":suspect.loc[idx,"record_id"],"type":"modified"})

# Duplicates
for idx in rng.choice(suspect.index, 20, replace=False):
    row = suspect.loc[[idx]].copy()
    row["record_id"] = row["record_id"].astype(str) + "_DUP"
    suspect = pd.concat([suspect,row],ignore_index=True)
    truth.append({"record_id":row.iloc[0]["record_id"],"type":"duplicated"})

# Fabricated records
for j in range(15):
    rid = f"FAKE{j+1:04d}"
    origin,destination = rng.choice(["Mumbai","Chennai","Kandla","Kochi","Singapore","Dubai"],2,replace=False)
    suspect.loc[len(suspect)] = {
        "record_id":rid,"cargo_type":rng.choice(["Electronics","Textiles","Machinery","Food","Chemicals"]),
        "owner":f"OWNER_{rng.integers(1,101):03d}","origin":origin,"destination":destination,
        "current_location":rng.choice(["Mumbai","Chennai","Kandla","Kochi","Singapore","Dubai","Mars"]),
        "weight_kg":float(rng.uniform(10,200000)),
        "container_count":int(rng.integers(1,20)),
        "declared_value":float(rng.uniform(100,1e9)),
        "status":"IN_TRANSIT","timestamp":pd.Timestamp("2030-01-01")
    }
    truth.append({"record_id":rid,"type":"fabricated"})

# Deleted records
for idx in rng.choice(clean.index, 20, replace=False):
    truth.append({"record_id":clean.loc[idx,"record_id"],"type":"deleted"})
    suspect = suspect[suspect["record_id"] != clean.loc[idx,"record_id"]]

# Harmless noise
noise_idx = rng.choice(suspect.index, 40, replace=False)
for idx in noise_idx:
    suspect.loc[idx,"owner"] = " " + str(suspect.loc[idx,"owner"]) + " "

suspect.to_csv("suspect_manifest.csv",index=False)
pd.DataFrame(truth).to_csv("private_injection_log.csv",index=False)
print("Generated suspect manifest:",len(suspect))
print("Private truth log:",len(truth),"events")
