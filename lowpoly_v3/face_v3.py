# Expression-ready low-poly toon face (exec'd inside build_v2 namespace by build_v3.py)
IRIS3=toon('Iris3','#c48ad0','#8a5aa8');PUP3=toon('Pupil3','#3a1f4a','#26132f');LASH3=toon('Lash3','#1a1416','#0a0809')
BROW3=toon('Brow3','#5a3270','#3c2050');MOUTHIN=toon('MouthIn','#6e2232','#521826');TEETH=toon('Teeth','#ffffff','#e6e6ee')
TONGUE=toon('Tongue','#e3848f','#c0606c');HILITE=toon('EyeHi','#ffffff','#ffffff')
FMATS=[EYEW,IRIS3,PUP3,HILITE,LASH3,BROW3,MOUTHIN,TEETH,TONGUE]
MI={m.name:i for i,m in enumerate(FMATS)}
def proj(x,z,off):
    p,_=onhead(x,z,off);return p
def lerp(a,b,t): return a+(b-a)*t
NE=8
# ---- parameterised parts: each returns list of (x,z,off) in fixed topology
def eye_curves(cx,cz,s,P):
    w=0.052*P.get('ew',1);h=0.034*P.get('eh',1);o=P.get('open',1);arc=P.get('arc',0)
    sq=P.get('sq',0)  # angry squint: inner upper corner down
    U=[];Lo=[]
    for i in range(NE+1):
        t=i/NE;x=cx+s*(t-0.5)*w;q=math.sin(math.pi*t)
        inner=(1-t)  # t=0 inner side
        low=cz-h*0.42*q**0.8+0.004*(t-0.5)
        up=cz+h*0.58*q**0.7+0.006*(t-0.5)-sq*0.012*inner*q-P.get('droop',0)*0.008*t*q
        closed=cz-h*0.15*q+0.003*(t-0.5)   # blink line (slightly smiling)
        hap=cz-0.006+0.020*q               # ^ arch
        cl=lerp(closed,hap,arc)
        up=lerp(cl,up,o);low=lerp(cl,low,o) if o<1 else low
        if o<1: low=lerp(cl,low,o)
        U.append((x,up));Lo.append((x,low))
    return U,Lo
def eye_parts(cx,cz,s,P):
    U,Lo=eye_curves(cx,cz,s,P);V_=[]
    def clampz(x,z):
        t=min(NE,max(0,(x-U[0][0])/(U[-1][0]-U[0][0]+1e-9)*NE)) if s>0 else min(NE,max(0,(U[0][0]-x)/(U[0][0]-U[-1][0]+1e-9)*NE))
        i=min(NE-1,int(t));f=t-i
        u=lerp(U[i][1],U[i+1][1],f);l=lerp(Lo[i][1],Lo[i+1][1],f)
        return min(max(z,l),u)
    white=[(x,z,0.0016) for x,z in U]+[(x,z,0.0016) for x,z in Lo]
    ir=P.get('ir',1);icx=cx+s*0.002;icz=cz-0.001+P.get('iz',0)
    iris=[(icx,clampz(icx,icz),0.0026)]+[(icx+0.013*ir*math.cos(a),clampz(icx+0.013*ir*math.cos(a),icz+0.016*ir*math.sin(a)),0.0026) for a in [k*2*math.pi/10 for k in range(10)]]
    pr=P.get('pr',1)
    pup=[(icx,clampz(icx,icz),0.0033)]+[(icx+0.006*pr*math.cos(a),clampz(icx+0.006*pr*math.cos(a),icz+0.008*pr*math.sin(a)),0.0033) for a in [k*2*math.pi/8 for k in range(8)]]
    hx_,hz=icx-s*0.004,icz+0.006
    hi=[(hx_,clampz(hx_,hz),0.004)]+[(hx_+0.0035*math.cos(a),clampz(hx_+0.0035*math.cos(a),hz+0.0035*math.sin(a)),0.004) for a in [k*2*math.pi/6 for k in range(6)]]
    # upper lash: strip above U, thicker at outer end + wing
    th=0.0045
    lash=[(x,z+th*(0.5+0.8*i/NE),0.0046) for i,(x,z) in enumerate(U)]+[(x,z-0.0008,0.0046) for x,z in U]
    wx,wz=U[-1];lash.append((wx+s*0.008,wz+0.006+P.get('wing',0),0.0046))
    # lower lash thin (only outer half)
    llash=[(x,z-0.0006,0.0044) for x,z in Lo[NE//2:]]+[(x,z+0.0012,0.0044) for x,z in Lo[NE//2:]]
    return white,iris,pup,hi,lash,llash
def brow(cx,cz,s,P):
    pts=[];n=5;inner=P.get('bin',0);outer=P.get('bout',0);up=P.get('bup',0)
    for i in range(n):
        t=i/(n-1);x=cx+s*(t-0.5)*0.05;z=cz+0.032+up+0.004*math.sin(math.pi*t)+lerp(inner,outer,t)
        pts.append((x,z))
    return [(x,z+0.0028*(1-0.5*abs(i/(n-1)-0.3)),0.0035) for i,(x,z) in enumerate(pts)]+[(x,z-0.0028*(1-0.5*abs(i/(n-1)-0.3)),0.0035) for i,(x,z) in enumerate(pts)]
NM=8
def mouth(P):
    cx,cz=0.0,1.428;w=P['mw'];out=[]
    U=[];Lo=[]
    for i in range(NM+1):
        t=i/NM;s=2*t-1;x=cx+s*w/2;q=1-s*s
        if P.get('o'):  # round O
            r=math.sqrt(max(0,q))
            u=cz+0.004+P['ua']*r;l=cz+0.004-P['ld']*r
        else:
            u=cz+P['cl']*s*s+P.get('ua',0)*q;l=cz+P['cl']*s*s-P['ld']*q**0.9
        U.append((x,u));Lo.append((x,l))
    return U,Lo
def mouth_parts(P):
    U,Lo=mouth(P);rows=[0,0.2,0.24,0.68,1.0]  # teeth band, gap, dark, tongue
    grid=[]
    for r in rows:
        for (x,u),(_,l) in zip(U,Lo): grid.append((x,lerp(u,l,r),0.0016 if r in(0,1.0) else 0.0016))
    # lip line (always visible, follows mid of upper curve)
    line=[(x,u+0.0011,0.0024) for x,u in U]+[(x,u-0.0007,0.0024) for x,u in U]
    return grid,line
EXPR={
 'Basis':dict(eye={},br={},m=dict(mw=0.042,cl=0.008,ld=0.017)),
 'Smile':dict(eye=dict(open=0.85,arc=0.0),br=dict(bup=0.002),m=dict(mw=0.048,cl=0.010,ld=0.021)),
 'Happy':dict(eye=dict(open=0.0,arc=1.0),br=dict(bup=0.004),m=dict(mw=0.048,cl=0.008,ld=0.030,ua=0.001)),
 'Angry':dict(eye=dict(sq=1.0,open=0.9,ir=0.9,pr=0.75),br=dict(bin=-0.02,bout=0.006,bup=-0.004),m=dict(mw=0.036,cl=-0.006,ld=0.009,ua=0.003)),
 'Sad':dict(eye=dict(open=0.8,droop=1.0,iz=-0.002),br=dict(bin=0.016,bout=-0.008),m=dict(mw=0.032,cl=-0.008,ld=0.0015,ua=0.003)),
 'Surprised':dict(eye=dict(ew=1.08,eh=1.3,ir=0.85,pr=0.6),br=dict(bup=0.012),m=dict(mw=0.018,o=1,ua=0.006,ld=0.014)),
 'Blink':dict(eye=dict(open=0.0,arc=0.0),br={},m=None),
 'Wink':dict(eye={},eyeR=dict(open=0.0,arc=0.55),br={},brR=dict(bin=-0.004),m=dict(mw=0.046,cl=0.010,ld=0.019)),
 'Wink.L':dict(eye={},eyeL=dict(open=0.0,arc=0.55),br={},m=None),
 'Wink.R':dict(eye={},eyeR=dict(open=0.0,arc=0.55),br={},m=None),
}
def face_coords(E):
    base=EXPR['Basis'];m=E['m'] if E['m'] else base['m']
    pts=[];faces=[]
    def add(ps): pts.extend(ps)
    for s in (1,-1):
        cx,cz=0.037*s,1.488
        SD='L' if s>0 else 'R'
        for part in eye_parts(cx,cz,s,E.get('eye'+SD,E['eye'])): add(part)
        add(brow(cx,cz,s,E.get('br'+SD,E['br'])))
    for part in mouth_parts(m): add(part)
    return pts
def build_face():
    bm=bmesh.new();co=face_coords(EXPR['Basis']);vs=[bm.verts.new(proj(x,z,o)) for x,z,o in co];k=[0]
    def take(n): a=k[0];k[0]+=n;return vs[a:a+n]
    def strip(a,b,mat):
        for i in range(len(a)-1):
            f=bm.faces.new((a[i],a[i+1],b[i+1],b[i]));f.material_index=MI[mat]
    def fan(c,ring,mat):
        for i in range(len(ring)):
            f=bm.faces.new((c,ring[i],ring[(i+1)%len(ring)]));f.material_index=MI[mat]
    for s in (1,-1):
        w=take(2*(NE+1));strip(w[NE+1:],w[:NE+1],'EyeWhite') if s>0 else strip(w[:NE+1],w[NE+1:],'EyeWhite')
        ir=take(11);fan(ir[0],ir[1:],'Iris3') if True else None
        pu=take(9);fan(pu[0],pu[1:],'Pupil3')
        hi=take(7);fan(hi[0],hi[1:],'EyeHi')
        la=take(2*(NE+1)+1);strip(la[NE+1:2*NE+2],la[:NE+1],'Lash3');f=bm.faces.new((la[NE],la[2*NE+1],la[-1]) if s>0 else (la[-1],la[2*NE+1],la[NE]));f.material_index=MI['Lash3']
        ll=take(2*(NE//2+1));strip(ll[:NE//2+1],ll[NE//2+1:],'Lash3')
        br=take(10);strip(br[5:],br[:5],'Brow3')
    g=take(5*(NM+1));R=[g[r*(NM+1):(r+1)*(NM+1)] for r in range(5)]
    for r,mat in enumerate(['Teeth','MouthIn','MouthIn','Tongue']): strip(R[r+1],R[r],mat)
    ln=take(2*(NM+1));strip(ln[NM+1:],ln[:NM+1],'Lash3')
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
    for f in bm.faces:  # face the camera (-y)
        if f.normal.y>0: f.normal_flip()
    me=bpy.data.meshes.new('Face');bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new('Face',me);sc.collection.objects.link(o);o.parent=root
    for m in FMATS: me.materials.append(m)
    o.shape_key_add(name='Basis')
    for n in ('Smile','Happy','Angry','Sad','Surprised','Blink','Wink','Wink.L','Wink.R'):
        sk=o.shape_key_add(name=n,from_mix=False)
        for i,(x,z,off) in enumerate(face_coords(EXPR[n])): sk.data[i].co=proj(x,z,off)
    PARTS.append(o);return o
FACE=build_face()
