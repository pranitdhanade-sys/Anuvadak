import argparse,joblib,numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
def main():
 p=argparse.ArgumentParser();p.add_argument("--data",default="ml/dataset/processed/data.npz");p.add_argument("--model",default="ml/models/gesture_classifier.joblib");a=p.parse_args();d=np.load(a.data); X,y=d['X'],d['y']
 if len(set(y))<2: raise SystemExit("Training needs at least two gesture labels.")
 Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,stratify=y,random_state=42); m=RandomForestClassifier(n_estimators=250,max_depth=None,min_samples_leaf=1,n_jobs=-1,random_state=42,class_weight='balanced');m.fit(Xtr,ytr);Path(a.model).parent.mkdir(parents=True,exist_ok=True);joblib.dump(m,a.model);print(f"Validation accuracy: {accuracy_score(yte,m.predict(Xte)):.3f}")
if __name__=="__main__":main()
