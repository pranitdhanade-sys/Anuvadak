import numpy as np
from backend.services.feature_extractor import normalize_landmarks,extract_features
def hand(offset=0): return [[offset+i*.01,offset+i*.02,0] for i in range(21)]
def test_normalization_is_translation_invariant(): assert np.allclose(normalize_landmarks(hand()),normalize_landmarks(hand(3)))
def test_feature_width_and_padding():
 f=extract_features([hand()]);assert f.shape==(126,);assert not f[0:63].any()==False;assert np.allclose(f[63:],0)
def test_two_hand_features(): assert extract_features([hand(),hand(1)]).shape==(126,)
