import sys,shutil,os,traceback
from gradio_client import Client, handle_file
m=sys.argv[1]; img='/workspace/lillith-patreon/assets/Suit/LM_Suit_V1.png'; os.makedirs(m,exist_ok=True)
def save(p,n):
  p=p if isinstance(p,str) else (p.get('value') or p.get('path') if isinstance(p,dict) else p)
  shutil.copy(p,f'{m}/{n}'); print('SAVED',m,n)
try:
  if m=='trellis':
    c=Client('trellis-community/TRELLIS',verbose=False); c.predict(api_name='/start_session')
    r=c.predict(handle_file(img),[],0,7.5,12,3.0,12,'stochastic',0.95,1024,api_name='/generate_and_extract_glb'); save(r[2],'model.glb')
  if m=='trellis2':
    c=Client('microsoft/TRELLIS.2',verbose=False); c.predict(api_name='/start_session')
    p=c.predict(handle_file(img),api_name='/preprocess_image')
    c.predict(handle_file(p if isinstance(p,str) else p['path']),0,'1024',api_name='/image_to_3d')
    r=c.predict(200000,2048,api_name='/extract_glb'); save(r[1],'model.glb')
  if m=='sf3d':
    c=Client('stabilityai/stable-fast-3d',verbose=False)
    r=c.predict(handle_file(img),0.85,'None',-1,1024,api_name='/run_button'); save(r[1],'model.glb')
  if m=='hunyuan21':
    c=Client('tencent/Hunyuan3D-2.1',verbose=False)
    r=c.predict(image=handle_file(img),api_name='/generation_all'); print(r); save(r[1],'model.glb'); save(r[0],'shape.glb')
  if m=='instantmesh':
    c=Client('TencentARC/InstantMesh',verbose=False)
    p=c.predict(handle_file(img),True,api_name='/preprocess'); c.predict(handle_file(p),75,42,api_name='/generate_mvs')
    r=c.predict(api_name='/make3d'); save(r[1],'model.glb')
except Exception as e: print('FAIL',m,repr(e)[:400])
