"""Publish the committed main tree using gh's authenticated Git data API."""
import subprocess,json,base64
from pathlib import Path
root=Path(__file__).resolve().parents[1]
repo='Percivalbeep/consseau-public-speaking-assistant'
def run(*args):return subprocess.check_output(args,cwd=root,text=True).strip()
def api(path,data=None):
 args=['gh','api',f'repos/{repo}/'+path]
 if data is not None:args+=['-X','POST','--input','-']
 p=subprocess.run(args,input=json.dumps(data) if data is not None else None,text=True,capture_output=True,cwd=root)
 if p.returncode:raise RuntimeError(p.stderr)
 return json.loads(p.stdout)
head=api('git/ref/heads/main')['object']['sha']
local=run('git','rev-parse','HEAD')
if head==local:print('Already published');raise SystemExit
try:names=run('git','diff','--name-only',head,local).splitlines()
except subprocess.CalledProcessError:names=run('git','ls-files').splitlines()
tree=[]
for name in names:
 p=root/name
 if not p.is_file():tree.append({'path':name,'mode':'100644','type':'blob','sha':None});continue
 blob=api('git/blobs',{'content':base64.b64encode(p.read_bytes()).decode(),'encoding':'base64'})
 tree.append({'path':name,'mode':'100644','type':'blob','sha':blob['sha']})
if not tree:print('No changes');raise SystemExit
base=api('git/commits/'+head)['tree']['sha']
t=api('git/trees',{'base_tree':base,'tree':tree})
c=api('git/commits',{'message':'Update Consseau speaking practice','tree':t['sha'],'parents':[head]})
p=subprocess.run(['gh','api',f'repos/{repo}/git/refs/heads/main','-X','PATCH','--input','-'],input=json.dumps({'sha':c['sha'],'force':False}),text=True,capture_output=True,cwd=root)
if p.returncode:raise RuntimeError(p.stderr)
print('Published '+c['sha'],flush=True)
