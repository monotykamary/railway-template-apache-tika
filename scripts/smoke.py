#!/usr/bin/env python3
"""Repeatable product checks; credentials remain process-local and never printed."""
import os,json,time,uuid,hashlib,tempfile,base64,urllib.request,urllib.error,urllib.parse
from pathlib import Path
base=os.environ['BASE_URL'].rstrip('/')
phase=os.environ.get('SMOKE_PHASE','boot')
state=Path(tempfile.gettempdir())/('railway-smoke-'+hashlib.sha256(base.encode()).hexdigest()[:16]+'.json')
def req(path,method='GET',data=None,auth=None,headers=None):
 h=dict(headers or {})
 if auth:
  h['Authorization']='Basic '+base64.b64encode((':'.join(auth)).encode()).decode() if isinstance(auth,tuple) else 'Bearer '+auth
 if isinstance(data,dict):h['Content-Type']='application/json';data=json.dumps(data).encode()
 if isinstance(data,str):data=data.encode()
 r=urllib.request.Request(base+path,data=data,headers=h,method=method)
 try:
  with urllib.request.urlopen(r,timeout=45) as x:return x.status,x.read().decode()
 except urllib.error.HTTPError as e:return e.code,e.read().decode()
def good(result,codes=(200,)):
 assert result[0] in codes, 'unexpected HTTP status '+str(result[0])
 return result[1]
def asjson(result,codes=(200,)):return json.loads(good(result,codes))

auth=(os.environ['BASIC_AUTH_USER'],os.environ['BASIC_AUTH_PASSWORD'])
assert 'Apache Tika' in good(req('/healthz'))
assert req('/tika',method='PUT',data='private')[0]==401
assert req('/tika',auth=(auth[0],'incorrect-password'))[0]==401
text='Railway Tika extraction product probe'
assert text in good(req('/tika',method='PUT',data=text,auth=auth,headers={'Content-Type':'text/plain','Accept':'text/plain'}))
metadata=good(req('/meta',method='PUT',data=text,auth=auth,headers={'Content-Type':'text/plain','Accept':'application/json'}))
assert 'text/plain' in metadata
print(json.dumps({'phase':phase,'product':'tika','extraction':True,'metadata':True,'negative_auth':True,'persistence':'stateless'}))
