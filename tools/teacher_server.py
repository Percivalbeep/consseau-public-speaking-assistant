"""Local-only teacher studio. Run: python3 tools/teacher_server.py"""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import json,subprocess,threading,uuid,secrets,io,zipfile,base64,re,xml.etree.ElementTree as ET
from datetime import date
ROOT=Path(__file__).resolve().parents[1]
PRIVATE=ROOT/'.work/studio';PRIVATE.mkdir(parents=True,exist_ok=True)
TOKEN=secrets.token_urlsafe(32);JOBS={};LOCK=threading.Lock()
def speech(job,text,rate):
 try:
  JOBS[job]['status']='generating'
  text=text.replace('[[','').replace(']]','')
  words=len(re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)*",text))
  paragraphs=len([p for p in re.split(r'\n\s*\n',text) if p.strip()])
  text=' [[slnc 450]] '.join(p.strip() for p in re.split(r'\n\s*\n',text) if p.strip())
  src=PRIVATE/f'{job}.txt';src.write_text(text)
  subprocess.run(['say','-v','Samantha','-r',str(rate),'-f',str(src),'-o',str(PRIVATE/f'{job}.aiff')],check=True,timeout=120)
  normal=PRIVATE/f'{job}.mp3';slow=PRIVATE/f'{job}-slow.mp3'
  raw=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(PRIVATE/f'{job}.aiff')]))
  target=words/rate*60+max(0,paragraphs-1)*.45
  tempo=max(.5,min(1.5,raw/target)) if words>=15 and target else 1
  subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(PRIVATE/f'{job}.aiff'),'-filter:a',f'atempo={tempo}','-codec:a','libmp3lame','-q:a','3',str(normal)],check=True,timeout=120)
  subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(normal),'-filter:a','atempo=0.85','-codec:a','libmp3lame','-q:a','3',str(slow)],check=True,timeout=120)
  duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(normal)]))
  if duration<.3:raise ValueError('没有生成有效音频，请检查系统语音。')
  JOBS[job].update(status='ready',duration=round(duration,1),audio=f'/private/{job}.mp3',slow=f'/private/{job}-slow.mp3')
 except Exception as e:JOBS[job].update(status='error',message=str(e))
def publish(job,student):
 try:
  with LOCK:
   j=JOBS[job];j['publish']='publishing'
   import shutil
   for suffix in ['', '-slow']:shutil.copy(PRIVATE/f'{job}{suffix}.mp3',ROOT/f'assets/stories/{job}{suffix}.mp3')
   f=ROOT/'stories.json';data=json.loads(f.read_text()) if f.exists() else {}
   entry={'title':j['title'],'audio':f'assets/stories/{job}.mp3','slow':f'assets/stories/{job}-slow.mp3','date':date.today().isoformat()}
   entries=data.setdefault(student,[])
   if not any(e['audio']==entry['audio'] for e in entries):entries.append(entry)
   f.write_text(json.dumps(data,ensure_ascii=False,indent=2))
   subprocess.run(['git','add','stories.json',f'assets/stories/{job}.mp3',f'assets/stories/{job}-slow.mp3'],cwd=ROOT,check=True)
   subprocess.run(['git','commit','-m','Add reviewed speech audio for '+student],cwd=ROOT,check=True,capture_output=True)
   subprocess.run(['python3','tools/publish.py'],cwd=ROOT,check=True,timeout=240,capture_output=True)
   j.update(publish='published',link='https://percivalbeep.github.io/consseau-public-speaking-assistant/?student='+student)
 except Exception as e:JOBS[job].update(publish='error',message=str(e))
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def safe(self):return self.headers.get('Host') in ['127.0.0.1:8766','localhost:8766']
 def reply(self,data,code=200):
  b=json.dumps(data,ensure_ascii=False).encode();self.send_response(code);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(b)
 def do_GET(self):
  if not self.safe():return self.send_error(403)
  path=self.path.split('?')[0]
  if path=='/api/jobs':return self.reply(JOBS)
  if path=='/teacher':
   b=(ROOT/'teacher.html').read_text().replace('__LOCAL_TOKEN__',TOKEN).encode();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Cache-Control','no-store');self.end_headers();return self.wfile.write(b)
  if path.startswith('/private/'):
   name=path.split('/')[-1]
   if not re.fullmatch(r'[a-f0-9]{32}(-slow)?\.mp3',name):return self.send_error(404)
   p=PRIVATE/name
   if not p.exists():return self.send_error(404)
   self.send_response(200);self.send_header('Content-Type','audio/mpeg');self.send_header('Content-Length',str(p.stat().st_size));self.end_headers();return self.wfile.write(p.read_bytes())
  if path.startswith('/.'):return self.send_error(404)
  return super().do_GET()
 def do_POST(self):
  if not self.safe() or self.headers.get('X-Studio-Token')!=TOKEN:return self.reply({'error':'仅限本机教师页面操作'},403)
  try:
   n=int(self.headers.get('Content-Length','0'))
   if n>8_000_000:raise ValueError('文件太大，请使用5MB以内的稿件')
   d=json.loads(self.rfile.read(n))
   if self.path=='/api/extract':
    b=base64.b64decode(d['content']);name=d['name'].lower()
    if len(b)>5_000_000:raise ValueError('文件超过5MB')
    if name.endswith('.docx'):
     with zipfile.ZipFile(io.BytesIO(b)) as z:
      info=z.getinfo('word/document.xml')
      if info.file_size>5_000_000:raise ValueError('文档内容过大')
      x=ET.fromstring(z.read(info));ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
      text='\n\n'.join(''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in x.findall('.//w:p',ns))
    elif name.endswith('.txt'):text=b.decode('utf-8-sig')
    else:raise ValueError('请上传DOCX或UTF-8 TXT，也可以直接粘贴文字')
    return self.reply({'text':text})
   if self.path=='/api/generate':
    text=d.get('text','').strip();title=d.get('title','').strip()[:100] or 'Speech practice';rate=int(d.get('rate',135))
    if not 1<=len(text)<=15000:raise ValueError('请输入稿件，最多15000字符')
    if rate not in [110,135,155]:raise ValueError('语速设置无效')
    job=uuid.uuid4().hex;JOBS[job]={'status':'queued','title':title,'publish':None};threading.Thread(target=speech,args=(job,text,rate),daemon=True).start();return self.reply({'job':job})
   if self.path=='/api/publish':
    job=d['job'];student=d['student']
    if student not in ['mia','amy'] or job not in JOBS or JOBS[job]['status']!='ready':raise ValueError('请先生成并试听音频')
    if JOBS[job]['publish'] in ['publishing','published']:raise ValueError('这段音频已在发布或已发布')
    if d.get('confirm') is not True:raise ValueError('请先确认允许公开音频内容')
    threading.Thread(target=publish,args=(job,student),daemon=True).start();return self.reply({'ok':True})
   self.reply({'error':'Not found'},404)
  except Exception as e:self.reply({'error':str(e)},400)
if __name__=='__main__':
 print('Teacher studio: http://127.0.0.1:8766/teacher',flush=True)
 ThreadingHTTPServer(('127.0.0.1',8766),Handler).serve_forever()
