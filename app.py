import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Manifest Sentinel",layout="wide")
st.title("🚢 Manifest Sentinel")
st.caption("Cargo Tampering Detection & Reconstruction — Code of the Seas")

p=Path("analysis_output.csv")
if not p.exists():
    st.error("Run generator.py, injector.py and detector.py first.")
    st.stop()

df=pd.read_csv(p)
c1,c2,c3,c4=st.columns(4)
c1.metric("Records analysed",len(df))
c2.metric("Suspicious",int((df.label=="Suspicious").sum()))
c3.metric("Needs review",int((df.label=="Review").sum()))
c4.metric("High confidence",int((df.confidence>=.5).sum()))

st.subheader("Tampering overview")
st.bar_chart(df[df.suspected_tampering!="none"]["suspected_tampering"].value_counts())

st.subheader("Suspicious records")
view=df[df.label!="Normal"].sort_values(["confidence","score"],ascending=False)
st.dataframe(view[["record_id","label","confidence","suspected_tampering",
                   "owner","origin","destination","current_location",
                   "weight_kg","declared_value","timestamp","reconstruction_status","reasons"]],
             use_container_width=True)

st.subheader("Attack timeline")
timeline=df[df.label!="Normal"].copy()
timeline["timestamp"]=pd.to_datetime(timeline.timestamp)
timeline=timeline.set_index("timestamp").resample("7D").size()
st.line_chart(timeline)

st.info("Explainability: every flag has a rule/statistical reason; reconstruction never silently changes a record.")
