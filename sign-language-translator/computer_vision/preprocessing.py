import cv2
def jpeg_frame(frame, quality=80):
    ok, data=cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,quality])
    if not ok: raise ValueError('Frame encoding failed')
    return data.tobytes()
