"""Position/scale invariant fixed-width features for up to two ISL hands."""
import numpy as np
LANDMARKS_PER_HAND, HANDS = 21, 2
FEATURE_SIZE = LANDMARKS_PER_HAND * 3 * HANDS

def normalize_landmarks(landmarks):
    points = np.asarray(landmarks, dtype=np.float32).reshape(-1, 3)
    if len(points) != LANDMARKS_PER_HAND: raise ValueError("Expected 21 landmarks")
    centered = points - points[0]
    scale = np.max(np.linalg.norm(centered[:, :2], axis=1))
    return centered / max(float(scale), 1e-6)
def extract_features(hands):
    """Return 126 features; absent second hand is zero-padded."""
    if not hands or len(hands) > HANDS: raise ValueError("Expected one or two hands")
    result = np.zeros((HANDS, LANDMARKS_PER_HAND, 3), dtype=np.float32)
    for i, hand in enumerate(hands): result[i] = normalize_landmarks(hand)
    return result.ravel()
