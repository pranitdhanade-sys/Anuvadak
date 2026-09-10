"""Capture real MediaPipe landmark samples. Press SPACE to save; Q to exit."""
import argparse,json
from pathlib import Path
import cv2
from backend.services.hand_detector import HandDetector
def main():
 p=argparse.ArgumentParser();p.add_argument('label');p.add_argument('--output',default='ml/dataset/raw');a=p.parse_args();out=Path(a.output)/f'{a.label}.jsonl';out.parent.mkdir(parents=True,exist_ok=True);cap=cv2.VideoCapture(0)
 if not cap.isOpened(): raise SystemExit('Camera unavailable')
 d=HandDetector(); count=0
 while True:
  ok,frame=cap.read()
  if not ok: break
  ok_,encoded=cv2.imencode('.jpg',frame);hands=d.detect(encoded.tobytes())
  cv2.putText(frame,f'{a.label}: {count} | SPACE save | Q quit',(12,32),cv2.FONT_HERSHEY_SIMPLEX,.7,(0,255,0),2);cv2.imshow('Collect ISL data',frame); key=cv2.waitKey(1)&255
  if key==32 and hands:
   with out.open('a') as f:f.write(json.dumps({'label':a.label,'hands':hands})+'\n')
   count+=1
  if key==ord('q'):break
 cap.release();cv2.destroyAllWindows()
if __name__=='__main__':main()
