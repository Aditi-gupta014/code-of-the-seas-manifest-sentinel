import pandas as pd

truth=pd.read_csv("private_injection_log.csv")
out=pd.read_csv("analysis_output.csv")

truth_ids=set(truth.record_id)
pred_ids=set(out.loc[out.label!="Normal","record_id"])

tp=len(truth_ids & pred_ids)
fp=len(pred_ids-truth_ids)
fn=len(truth_ids-pred_ids)

precision=tp/(tp+fp) if tp+fp else 0
recall=tp/(tp+fn) if tp+fn else 0
false_alarm_rate=fp/len(out) if len(out) else 0

print(f"TP={tp} FP={fp} FN={fn}")
print(f"Precision={precision:.3f}")
print(f"Recall={recall:.3f}")
print(f"False-alarm rate={false_alarm_rate:.3f}")

truth_counts=truth.type.value_counts().to_dict()
pred_counts=out[out.label!="Normal"].suspected_tampering.value_counts().to_dict()
print("Ground truth:",truth_counts)
print("Detected:",pred_counts)
