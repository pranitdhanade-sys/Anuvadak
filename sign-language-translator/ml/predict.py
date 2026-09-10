"""Run model prediction from a supplied JSON hand-landmark sample."""
import argparse,json,joblib
from backend.services.feature_extractor import extract_features
def main():
 p=argparse.ArgumentParser();p.add_argument('sample');p.add_argument('--model',default='ml/models/gesture_classifier.joblib');a=p.parse_args();row=json.load(open(a.sample));m=joblib.load(a.model);prob=m.predict_proba([extract_features(row['hands'])])[0];i=prob.argmax();print(m.classes_[i],float(prob[i]))
if __name__=='__main__':main()
