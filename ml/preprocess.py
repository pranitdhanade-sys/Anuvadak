"""Validate and split collected JSONL landmark samples into compressed NumPy data."""
import argparse,json,numpy as np
from pathlib import Path
from backend.services.feature_extractor import extract_features
def load(raw):
    x=[]; y=[]
    for file in Path(raw).glob("*.jsonl"):
      for line in file.read_text().splitlines():
        row=json.loads(line); x.append(extract_features(row["hands"])); y.append(row["label"])
    if not x: raise SystemExit("No samples found. Run ml/collect_data.py first.")
    return np.asarray(x),np.asarray(y)
def main():
 p=argparse.ArgumentParser();p.add_argument("--raw",default="ml/dataset/raw");p.add_argument("--out",default="ml/dataset/processed/data.npz");a=p.parse_args(); x,y=load(a.raw);Path(a.out).parent.mkdir(parents=True,exist_ok=True);np.savez_compressed(a.out,X=x,y=y);print(f"Saved {len(y)} samples across {len(set(y))} labels")
if __name__=="__main__":main()
