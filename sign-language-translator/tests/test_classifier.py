import joblib,numpy as np
from sklearn.ensemble import RandomForestClassifier
from backend.services.gesture_classifier import GestureClassifier
def test_model_loading_and_prediction(tmp_path):
 x=np.vstack([np.zeros(126),np.ones(126),np.zeros(126)+.01,np.ones(126)*.99]);m=RandomForestClassifier(n_estimators=5,random_state=1).fit(x,['A','B','A','B']);path=tmp_path/'m.joblib';joblib.dump(m,path);c=GestureClassifier(str(path));label,confidence=c.predict(np.zeros(126));assert c.available and label=='A' and confidence>.5
def test_missing_model_is_reported(tmp_path): assert not GestureClassifier(str(tmp_path/'missing')).available
