import argparse,joblib,numpy as np
from sklearn.metrics import classification_report,accuracy_score
def main():
 p=argparse.ArgumentParser();p.add_argument('--data',default='ml/dataset/processed/data.npz');p.add_argument('--model',default='ml/models/gesture_classifier.joblib');a=p.parse_args();d=np.load(a.data);m=joblib.load(a.model);pred=m.predict(d['X']);print('Accuracy:',accuracy_score(d['y'],pred));print(classification_report(d['y'],pred))
if __name__=='__main__':main()
