#!/usr/bin/env python3
"""Repeatable product checks; credentials remain process-local and never printed."""
import os,json,time,uuid,hashlib,tempfile,base64,urllib.request,urllib.error,urllib.parse
from pathlib import Path
base=os.environ['BASE_URL'].rstrip('/')
phase=os.environ.get('SMOKE_PHASE','boot')
state=Path(os.environ.get('SMOKE_STATE_FILE',str(Path(tempfile.gettempdir())/('railway-smoke-'+hashlib.sha256(base.encode()).hexdigest()[:16]+'.json'))))
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
def pdf_fixture():
 objects=[b'<< /Type /Catalog /Pages 2 0 R >>',b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>']
 stream=b'BT /F1 16 Tf 72 720 Td (Railway PDF parser proof) Tj ET'
 objects.append(b'<< /Length '+str(len(stream)).encode()+b' >>\nstream\n'+stream+b'\nendstream')
 data=b'%PDF-1.4\n'; offsets=[0]
 for i,obj in enumerate(objects,1):
  offsets.append(len(data));data+=str(i).encode()+b' 0 obj\n'+obj+b'\nendobj\n'
 xref=len(data);data+=b'xref\n0 6\n0000000000 65535 f \n'
 for offset in offsets[1:]:data+=('%010d 00000 n \n'%offset).encode()
 return data+b'trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n'+str(xref).encode()+b'\n%%EOF\n'
pdf=pdf_fixture()
assert 'Railway PDF parser proof' in good(req('/tika',method='PUT',data=pdf,auth=auth,headers={'Content-Type':'application/pdf','Accept':'text/plain'}))
pdfmeta=good(req('/meta',method='PUT',data=pdf,auth=auth,headers={'Content-Type':'application/pdf','Accept':'application/json'}))
assert 'application/pdf' in pdfmeta
bad=req('/tika',method='PUT',data=b'%PDF-1.4\ninvalid objects\n%%EOF',auth=auth,headers={'Content-Type':'application/pdf','Accept':'text/plain'})
assert bad[0] in (400,422), 'malformed PDF unexpectedly accepted/status='+str(bad[0])

print(json.dumps({'phase':phase,'pdf_extraction':True,'malformed_pdf_rejected':True,'product':'tika','extraction':True,'metadata':True,'negative_auth':True,'persistence':'stateless'}))
