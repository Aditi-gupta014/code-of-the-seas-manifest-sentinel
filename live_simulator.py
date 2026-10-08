import pandas as pd
import numpy as np
import subprocess, sys

# Simulates a late-arriving live attack that is NOT injected by injector.py:
# impossible container count relative to weight.
df=pd.read_csv("suspect_manifest.csv")
rng=np.random.default_rng(99)
idx=rng.choice(df.index,5,replace=False)
df.loc[idx,"container_count"]=999
df.to_csv("live_feed.csv",index=False)
print("Created live_feed.csv with a novel attack pattern: impossible container count.")
