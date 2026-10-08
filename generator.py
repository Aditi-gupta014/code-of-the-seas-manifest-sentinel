import pandas as pd
import numpy as np

SEED = 42
rng = np.random.default_rng(SEED)

N = 3000
cargo_types = ["Electronics","Textiles","Machinery","Food","Chemicals"]
owners = [f"OWNER_{i:03d}" for i in range(1,101)]
ports = ["Mumbai","Chennai","Kandla","Kochi","Singapore","Dubai","Colombo","Rotterdam"]

rows=[]
for i in range(1,N+1):
    origin, destination = rng.choice(ports,2,replace=False)
    ts = pd.Timestamp("2026-01-01") + pd.Timedelta(hours=int(rng.integers(0,24*180)))
    rows.append({
        "record_id": f"R{i:05d}",
        "cargo_type": rng.choice(cargo_types),
        "owner": rng.choice(owners),
        "origin": origin,
        "destination": destination,
        "current_location": origin,
        "weight_kg": round(float(rng.lognormal(7.5,0.65)),2),
        "container_count": int(rng.integers(1,8)),
        "declared_value": round(float(rng.lognormal(11.2,0.8)),2),
        "status": "IN_TRANSIT",
        "timestamp": ts
    })

df = pd.DataFrame(rows).sort_values("timestamp").reset_index(drop=True)
df.to_csv("clean_manifest.csv",index=False)
print("Generated",len(df),"clean records")
