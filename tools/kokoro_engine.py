"""Local Kokoro inference, using the project's isolated Python environment."""
from pathlib import Path
import argparse,re
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
ROOT=Path(__file__).resolve().parents[1]
def create(text,output,rate=135,voice='af_heart',engine=None):
 engine=engine or Kokoro(str(ROOT/'.work/kokoro/model.onnx'),str(ROOT/'.work/kokoro/voices.bin'))
 segments=[];sr=24000
 paragraphs=[p.strip() for p in re.split(r'\n\s*\n',text) if p.strip()]
 for pi,paragraph in enumerate(paragraphs):
  sentences=re.split(r'(?<=[.!?])\s+',paragraph);chunks=[];chunk=''
  for sentence in sentences:
   if chunk and len(chunk)+len(sentence)>430:chunks.append(chunk);chunk=''
   chunk=(chunk+' '+sentence).strip()
  if chunk:chunks.append(chunk)
  for ci,chunk in enumerate(chunks):
   audio,sr=engine.create(chunk,voice=voice,speed=max(.72,min(1.05,rate/170)),lang='en-us')
   if not len(audio):raise ValueError('Kokoro未生成音频')
   segments.append(audio)
   if ci<len(chunks)-1:segments.append(np.zeros(int(sr*.18),dtype=np.float32))
  if pi<len(paragraphs)-1:segments.append(np.zeros(int(sr*.45),dtype=np.float32))
 if not segments:raise ValueError('正文为空')
 sf.write(str(output),np.concatenate(segments),sr)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('text');parser.add_argument('output');parser.add_argument('--rate',type=int,default=135);parser.add_argument('--voice',default='af_heart');a=parser.parse_args()
 create(Path(a.text).read_text(),a.output,a.rate,a.voice)
