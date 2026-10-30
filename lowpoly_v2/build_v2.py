import bpy,bmesh,math,sys
from mathutils import Vector as V, Matrix
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
def hx(h):
    h=h.lstrip('#');c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return [((x+0.055)/1.055)**2.4 if x>0.04045 else x/12.92 for x in c]+[1]
MATS={}
def toon(name,base,shadow=None):
    if name in MATS: return MATS[name]
    m=bpy.data.materials.new(name);m.use_nodes=True;nt=m.node_tree;N=nt.nodes;L=nt.links
    for n in list(N): N.remove(n)
    out=N.new('ShaderNodeOutputMaterial');d=N.new('ShaderNodeBsdfDiffuse');s2r=N.new('ShaderNodeShaderToRGB')
    r=N.new('ShaderNodeValToRGB');r.color_ramp.interpolation='CONSTANT'
    b=hx(base);sh=hx(shadow) if shadow else [c*0.6 for c in b[:3]]+[1]
    r.color_ramp.elements[0].color=sh;r.color_ramp.elements[1].position=0.35;r.color_ramp.elements[1].color=b
    e=N.new('ShaderNodeEmission')
    L.new(d.outputs[0],s2r.inputs[0]);L.new(s2r.outputs[0],r.inputs[0]);L.new(r.outputs[0],e.inputs[0]);L.new(e.outputs[0],out.inputs[0])
    m['base']=base;m.diffuse_color=b;MATS[name]=m;return m
OUT=bpy.data.materials.new('Outline');OUT.use_nodes=True
N=OUT.node_tree.nodes;N.remove(N['Principled BSDF']);e=N.new('ShaderNodeEmission');e.inputs[0].default_value=(0.02,0.015,0.02,1)
OUT.node_tree.links.new(e.outputs[0],N['Material Output'].inputs[0]);OUT.use_backface_culling=True;OUT['base']='#050405'
root=bpy.data.objects.new('Lillith',None);sc.collection.objects.link(root)
PARTS=[]
def finish(bm,name,mat,outline=0.009,smooth=True):
    me=bpy.data.meshes.new(name);bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new(name,me);sc.collection.objects.link(o);o.parent=root
    o.data.materials.append(mat);o.data.materials.append(OUT)
    for p in me.polygons: p.use_smooth=smooth
    if outline:
        s=o.modifiers.new('outline','SOLIDIFY');s.thickness=outline;s.offset=1;s.use_flip_normals=True;s.use_rim=False;s.material_offset=1
    PARTS.append(o);return o
def resample(pts,rad,k):
    P=[V(p) for p in pts];R=[r if isinstance(r,(tuple,list)) else (r,r) for r in rad];op=[];orr=[]
    for i in range(len(P)-1):
        p0=P[max(i-1,0)];p1=P[i];p2=P[i+1];p3=P[min(i+2,len(P)-1)]
        for j in range(k):
            t=j/k;t2=t*t;t3=t2*t
            op.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3))
            orr.append(tuple(R[i][q]*(1-t)+R[i+1][q]*t for q in (0,1)))
    op.append(P[-1]);orr.append(R[-1]);return op,orr
def tube(name,pts,rad,mat,n=10,cap=(True,True),outline=0.009,twist=0,k=1):
    if k>1: pts,rad=resample(pts,rad,k)
    bm=bmesh.new();rings=[];pts=[V(p) for p in pts]
    up=V((0,0,1))
    for i,p in enumerate(pts):
        t=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized()
        ref=V((0,1,0)) if abs(t.z)>0.7 else V((0,0,1))
        a=t.cross(ref).normalized();b=t.cross(a).normalized()
        rx,ry=(rad[i] if isinstance(rad[i],(tuple,list)) else (rad[i],rad[i]))
        ring=[]
        for k in range(n):
            th=2*math.pi*k/n+twist
            if abs(t.z)>0.7: vv=p+V((math.cos(th)*rx,math.sin(th)*ry,0))
            else: vv=p+a*math.cos(th)*rx+b*math.sin(th)*ry
            ring.append(bm.verts.new(vv))
        rings.append(ring)
    for i in range(len(rings)-1):
        for k in range(n):
            bm.faces.new((rings[i][k],rings[i][(k+1)%n],rings[i+1][(k+1)%n],rings[i+1][k]))
    if cap[0]: bm.faces.new(list(reversed(rings[0])))
    if cap[-1]: bm.faces.new(rings[-1])
    bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=1e-5)
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
    return finish(bm,name,mat,outline)
def ell(name,c,r,mat,seg=16,rings=10,outline=0.009,cut=None):
    bm=bmesh.new();bmesh.ops.create_uvsphere(bm,u_segments=seg,v_segments=rings,radius=1)
    for v in bm.verts: v.co=V((v.co.x*r[0]+c[0],v.co.y*r[1]+c[1],v.co.z*r[2]+c[2]))
    if cut: bmesh.ops.delete(bm,geom=[v for v in bm.verts if cut(v.co)],context='VERTS')
    return finish(bm,name,mat,outline)
def disc(name,c,r,mat,normal=(0,-1,0),n=12,rot=0):
    bm=bmesh.new();bmesh.ops.create_circle(bm,cap_ends=True,segments=n,radius=1)
    for v in bm.verts: x,y=v.co.x*r[0],v.co.y*r[1];x,y=x*math.cos(rot)-y*math.sin(rot),x*math.sin(rot)+y*math.cos(rot);v.co=V((x,y,0))
    q=V((0,0,1)).rotation_difference(V(normal));bmesh.ops.rotate(bm,verts=bm.verts,matrix=q.to_matrix());bmesh.ops.translate(bm,verts=bm.verts,vec=V(c))
    return finish(bm,name,mat,0,False)
HAIR=toon('Hair','#9a68b0','#784c8b');HAIRL=toon('HairLight','#e8b8e9','#b581bf')
SKIN=toon('Skin','#f0d7c5','#c9907e');JACK=toon('Jacket','#504944','#292c38');SHIRT=toon('Shirt','#f4f5f5','#d6e5e9')
SKIRT=toon('Skirt','#3a3d45','#1f2024');TIGHT=toon('Tights','#4a3631','#382925');SHOE=toon('Heels','#1f2024','#0a0c10')
EYEW=toon('EyeWhite','#ffffff','#d6e5e9');IRIS=toon('Iris','#85b2c6','#5e709a');DARK=toon('Dark','#1a1416','#0a0809')
ORG=toon('Clip','#d88948','#a85e2a');MOUTH=toon('Mouth','#b06060','#804040');BADGE=toon('Badge','#f4f5f5','#9bc0cf');BLUE=toon('Lanyard','#5e709a','#43444d')
# head
HC=V((0,0,1.50));HR=(0.105,0.10,0.12)
ell('Head',HC,HR,SKIN,20,14)
tube('Neck',[(0,0.01,1.33),(0,0.01,1.42)],[0.035,0.035],SKIN,8)
def onhead(x,z,off=0.002):
    dx,dz=(x-HC.x)/HR[0],(z-HC.z)/HR[2];y=-HR[1]*math.sqrt(max(0,1-dx*dx-dz*dz))
    nrm=V((dx/HR[0],y/HR[1]**2*HR[1]/HR[1],dz/HR[2])).normalized();nrm=V(((x-HC.x)/HR[0]**2,y/HR[1]**2,(z-HC.z)/HR[2]**2)).normalized()
    return V((x,y+HC.y,z))+nrm*off,nrm
for side,vis in ((1,True),(-1,False)):
    x=0.042*side;p,nm=onhead(x,1.49,0.002)
    disc('EyeWhite'+str(side),p,(0.022,0.017),EYEW,nm)
    p2,_=onhead(x,1.488,0.004);disc('Iris'+str(side),p2,(0.012,0.015),IRIS,nm)
    p3,_=onhead(x,1.488,0.006);disc('Pupil'+str(side),p3,(0.005,0.008),DARK,nm)
    p4,_=onhead(x,1.506,0.005);disc('Lash'+str(side),p4,(0.025,0.004),DARK,nm,rot=-0.15*side)
pm,nm=onhead(0,1.425,0.003);disc('Mouth',pm,(0.014,0.005),MOUTH,nm)
# hair
ell('HairCap',(0,0.008,1.515),(0.118,0.115,0.135),HAIR,20,14,cut=lambda c:c.y<-0.045 and c.z<1.565 and abs(c.x)<0.07)
tube('HairBack',[(0,0.05,1.58),(0,0.075,1.45),(0,0.085,1.25),(0,0.075,1.05),(0,0.06,0.92)],[(0.125,0.08),(0.15,0.07),(0.15,0.055),(0.13,0.04),(0.07,0.02)],HAIR,14,k=2)
for s in (1,-1):
    tube('SideLock'+str(s),[(0.095*s,-0.05,1.60),(0.11*s,-0.055,1.52),(0.115*s,-0.05,1.40),(0.12*s,-0.06,1.25),(0.10*s,-0.07,1.12)],[(0.03,0.035),(0.035,0.04),0.035,0.03,0.0],HAIR,8,(True,False),k=2)
    tube('SideHair'+str(s),[(0.085*s,-0.06,1.63),(0.11*s,-0.03,1.56),(0.125*s,0.0,1.47),(0.13*s,0.03,1.34)],[(0.035,0.03),(0.04,0.05),(0.035,0.055),(0.0,0.0)],HAIR,8,(True,False),k=2)
    tube('TempleHair'+str(s),[(0.075*s,-0.095,1.62),(0.093*s,-0.088,1.55),(0.10*s,-0.085,1.47)],[(0.03,0.012),(0.025,0.012),(0.0,0.0)],HAIR,6,(True,False))
# bangs: cover her right eye (-x)
tube('BangBig',[(0.01,-0.10,1.62),(-0.03,-0.115,1.55),(-0.05,-0.115,1.47),(-0.07,-0.10,1.41)],[(0.045,0.012),(0.05,0.014),(0.04,0.012),(0.0,0.0)],HAIR,8,(True,False))
for x,z in ((0.04,1.53),(0.075,1.52),(0.01,1.545)):
    tube('Bang',[(x*0.6,-0.105,1.625),(x,-0.112,z)],[(0.022,0.008),(0.0,0.0)],HAIR,6,(True,False))
# ears
for s in (1,-1):
    tube('Ear'+str(s),[(0.065*s,0.01,1.60),(0.085*s,0.01,1.68),(0.10*s,0.015,1.74)],[(0.045,0.022),(0.03,0.016),(0.0,0.0)],HAIR,6,(True,False))
    tube('EarInner'+str(s),[(0.067*s,-0.006,1.615),(0.085*s,-0.006,1.675),(0.096*s,-0.003,1.715)],[(0.03,0.008),(0.018,0.006),(0.0,0.0)],HAIRL,6,(True,False),0)
# clip (orange skull) on her left
ell('Clip',(0.075,-0.09,1.60),(0.02,0.01,0.018),ORG,8,6,0.003)
for dx in (-0.007,0.007): disc('ClipEye',(0.075+dx,-0.101,1.602),(0.004,0.004),DARK,(0,-1,0),6)
# torso
tube('Jacket',[(0,0.0,0.97),(0,0.0,1.06),(0,0.0,1.20),(0,0.0,1.30),(0,0.005,1.36)],[(0.15,0.10),(0.13,0.085),(0.155,0.10),(0.165,0.09),(0.06,0.05)],JACK,12)
bm=bmesh.new();vs=[bm.verts.new(v) for v in ((-0.05,-0.093,1.34),(0.05,-0.093,1.34),(0,-0.104,1.14))];bm.faces.new(vs);finish(bm,'Shirt',SHIRT,0,False)
tube('Collar',[(0,0.005,1.355),(0,0.005,1.375)],[(0.06,0.05),(0.055,0.045)],SHIRT,10,(False,False),0.004)
# lanyard + badge
tube('Lanyard',[(-0.045,-0.03,1.37),(-0.03,-0.097,1.30),(0.0,-0.112,1.17),(0.03,-0.097,1.30),(0.045,-0.03,1.37)],[0.004]*5,BLUE,4,(False,False),0)
bm=bmesh.new();bmesh.ops.create_cube(bm,size=1)
for v in bm.verts: v.co=V((v.co.x*0.045,v.co.y*0.005-0.115,v.co.z*0.06+1.13))
finish(bm,'Badge',BADGE,0.003,False)
disc('BadgeStripe',(0,-0.1185,1.15),(0.02,0.006),BLUE,(0,-1,0),4)
# skirt
tube('Skirt',[(0,0,1.0),(0,0,0.90),(0,0,0.78)],[(0.16,0.11),(0.185,0.125),(0.20,0.135)],SKIRT,16)
# legs + pumps (heel ~6.5cm, foot angled)
for s in (1,-1):
    X=0.10*s
    tube('Leg'+str(s),[(0.075*s,0,0.95),(0.08*s,0,0.78),(0.088*s,-0.005,0.55),(0.093*s,0.0,0.43),(0.10*s,0.005,0.15),(X,0.01,0.10)],[0.085,0.08,0.05,0.056,0.03,0.03],TIGHT,12,k=2)
    # foot in tights (instep) angled down to toes
    tube('Foot'+str(s),[(X,0.025,0.095),(X,-0.02,0.07),(X,-0.07,0.035),(X,-0.11,0.022)],[(0.028,0.028),(0.028,0.024),(0.03,0.016),(0.0,0.0)],TIGHT,10,(True,False),0.006,k=2)
    # shoe upper / toe box
    tube('Shoe'+str(s),[(X,0.04,0.105),(X,0.0,0.08),(X,-0.05,0.045),(X,-0.10,0.025),(X,-0.135,0.022),(X,-0.145,0.022)],[(0.033,0.03),(0.034,0.034),(0.036,0.026),(0.034,0.02),(0.022,0.014),(0.0,0.0)],SHOE,12,(True,False),0.006,k=2)
    # sole
    tube('Sole'+str(s),[(X,0.045,0.072),(X,0.0,0.05),(X,-0.05,0.018),(X,-0.10,0.004),(X,-0.145,0.006)],[(0.03,0.006),(0.031,0.006),(0.034,0.006),(0.034,0.006),(0.02,0.005)],SHOE,8,(True,True),0.005,k=2)
    # block heel (tapered)
    bm=bmesh.new();bmesh.ops.create_cube(bm,size=1)
    for v in bm.verts:
        top=v.co.z>0;w=0.026 if top else 0.019;d=0.03 if top else 0.022
        v.co=V((X+v.co.x*2*w*0.5*2,0.045+v.co.y*d,0.072 if top else 0.0))
    finish(bm,'BlockHeel'+str(s),SHOE,0.005,False)
# arms A-pose
ARM={}
for s in (1,-1):
    sh,el,wr=V((0.165*s,0.0,1.30)),V((0.25*s,0.01,1.07)),V((0.31*s,0.0,0.87));ARM[s]=(sh,el,wr)
    tube('Sleeve'+str(s),[sh,(sh+el)/2,el,(el+wr)/2,wr],[0.05,0.045,0.04,0.039,0.038],JACK,10)
    tube('Cuff'+str(s),[wr,wr+(wr-el).normalized()*0.02],[0.039,0.036],SHIRT,10)
    ell('Hand'+str(s),wr+(wr-el).normalized()*0.06,(0.03,0.02,0.045),SKIN,10,8)
TP=[(0.04,0.10,0.95),(0.14,0.20,0.86),(0.27,0.24,0.92),(0.35,0.22,1.08),(0.36,0.19,1.22),(0.33,0.17,1.30)]
tube('Tail',TP[:5],[0.03,0.085,0.11,0.105,0.075],HAIR,14,(True,False),k=3)
tube('TailTip',TP[3:],[0.09,0.08,0.0],HAIRL,14,(False,False),k=3)
# ---------------- skeleton ----------------
arm=bpy.data.armatures.new('LillithRig');ao=bpy.data.objects.new('LillithRig',arm);sc.collection.objects.link(ao);ao.parent=root
bpy.context.view_layer.objects.active=ao;bpy.ops.object.mode_set(mode='EDIT')
EB=arm.edit_bones
def B(n,h,t,par=None,con=False):
    b=EB.new(n);b.head=V(h);b.tail=V(t);b.roll=0
    if par: b.parent=EB[par];b.use_connect=con
    return b
B('Root',(0,0,0),(0,-0.2,0))
B('Hips',(0,0,0.93),(0,0,1.05),'Root');B('Spine',(0,0,1.05),(0,0,1.18),'Hips',True);B('Chest',(0,0,1.18),(0,0,1.33),'Spine',True)
B('Neck',(0,0.01,1.33),(0,0.01,1.42),'Chest',True);B('Head',(0,0.01,1.42),(0,0.01,1.66),'Neck',True)
for s,S in ((1,'L'),(-1,'R')):
    sh,el,wr=ARM[s];hd=wr+(wr-el).normalized()*0.10
    B('Shoulder.'+S,(0.03*s,0,1.31),sh,'Chest');B('UpperArm.'+S,sh,el,'Shoulder.'+S,True);B('LowerArm.'+S,el,wr,'UpperArm.'+S,True);B('Hand.'+S,wr,hd,'LowerArm.'+S,True)
    X=0.10*s
    B('UpperLeg.'+S,(0.08*s,0,0.93),(0.09*s,-0.005,0.52),'Hips');B('LowerLeg.'+S,(0.09*s,-0.005,0.52),(X,0.01,0.10),'UpperLeg.'+S,True)
    B('Foot.'+S,(X,0.01,0.10),(X,-0.07,0.035),'LowerLeg.'+S,True);B('Toes.'+S,(X,-0.07,0.035),(X,-0.145,0.02),'Foot.'+S,True)
    B('Ear.'+S,(0.067*s,0.01,1.60),(0.10*s,0.015,1.74),'Head')
    B('SideLock.'+S,(0.105*s,-0.05,1.55),(0.10*s,-0.07,1.12),'Head')
HB=[(0,0.06,1.55),(0,0.08,1.38),(0,0.085,1.18),(0,0.06,0.92)]
for i in range(3): B('HairBack.%d'%i,HB[i],HB[i+1],'Head' if i==0 else 'HairBack.%d'%(i-1),i>0)
for i in range(5): B('Tail.%d'%i,TP[i],TP[i+1],'Hips' if i==0 else 'Tail.%d'%(i-1),i>0)
bpy.ops.object.mode_set(mode='OBJECT')
BONES={b.name:(b.head_local.copy(),b.tail_local.copy()) for b in arm.bones}
def segd(p,a,b):
    ab=b-a;t=max(0,min(1,(p-a).dot(ab)/ab.length_squared));return (p-(a+ab*t)).length
def cands(n):
    S='L' if n.endswith('1') and not n.endswith('-1') else 'R'
    for k in ('Head','Eye','Iris','Pupil','Lash','Mouth','HairCap','Bang','Clip','TempleHair'):
        if n.startswith(k): return ['Head']
    if n.startswith('SideHair'): return ['Head']
    if n=='Neck': return ['Chest','Neck','Head']
    if n.startswith('SideLock'): return ['Head','SideLock.'+S]
    if n=='HairBack': return ['Head','HairBack.0','HairBack.1','HairBack.2']
    if n.startswith('Ear'): return ['Ear.'+S]
    if n=='Jacket': return ['Hips','Spine','Chest','Neck']
    if n in('Shirt','Lanyard','Badge','BadgeStripe'): return ['Chest']
    if n=='Collar': return ['Neck']
    if n=='Skirt': return ['Hips','UpperLeg.L','UpperLeg.R']
    if n.startswith('Leg'): return ['Hips','UpperLeg.'+S,'LowerLeg.'+S,'Foot.'+S]
    if n.startswith(('Foot','Shoe','Sole')): return ['Foot.'+S,'Toes.'+S]
    if n.startswith('BlockHeel'): return ['Foot.'+S]
    if n.startswith('Sleeve'): return ['Chest','UpperArm.'+S,'LowerArm.'+S]
    if n.startswith('Cuff'): return ['LowerArm.'+S]
    if n.startswith('Hand'): return ['Hand.'+S]
    if n.startswith('Tail'): return ['Hips']+['Tail.%d'%i for i in range(5)]
    raise Exception('no map '+n)
def fixname(o):  # names like Leg1 / Leg-1 -> side
    return o.name
for o in PARTS:
    n=o.name.split('.')[0];S='L' if n.endswith('1') and not n.endswith('-1') else ('R' if n.endswith('-1') else None)
    cs=cands(n)
    if S is None: cs=[c for c in cs]
    else: cs=[c.replace('.L','.'+S).replace('.R','.'+S) if c.startswith(('UpperLeg','LowerLeg','Foot','Toes','UpperArm','LowerArm','Hand','Ear','SideLock')) and n!='Skirt' else c for c in cs]
    gs={c:o.vertex_groups.new(name=c) for c in cs}
    for v in o.data.vertices:
        p=V(v.co);ds=sorted(((segd(p,*BONES[c]),c) for c in cs))[:2]
        if len(ds)==1 or ds[1][0]-ds[0][0]>0.04: gs[ds[0][1]].add([v.index],1.0,'REPLACE')
        else:
            w0=1/(ds[0][0]+0.01)**3;w1=1/(ds[1][0]+0.01)**3
            gs[ds[0][1]].add([v.index],w0/(w0+w1),'REPLACE');gs[ds[1][1]].add([v.index],w1/(w0+w1),'REPLACE')
    md=o.modifiers.new('rig','ARMATURE');md.object=ao;o.modifiers.move(len(o.modifiers)-1,0)
# ---------------- animations ----------------
from mathutils import Quaternion as Q
for pb in ao.pose.bones: pb.rotation_mode='QUATERNION'
def wrot(bn,axis,deg):
    """rotation about an armature-space axis, expressed for the bone"""
    m=arm.bones[bn].matrix_local.to_3x3();ax=(m.inverted()@V(axis)).normalized()
    return Q(ax,math.radians(deg))
def make_action(name,length,fn):
    act=bpy.data.actions.new(name);act.use_fake_user=True;ao.animation_data_create();ao.animation_data.action=act
    for f in range(1,length+2,2 if length<40 else 3):
        t=(f-1)/length
        for pb in ao.pose.bones: pb.rotation_quaternion=(1,0,0,0);pb.location=(0,0,0)
        fn(t)
        for pb in ao.pose.bones:
            pb.keyframe_insert('rotation_quaternion',frame=f)
            if pb.name in('Root','Hips'): pb.keyframe_insert('location',frame=f)
    for fc in act.fcurves:
        fc.modifiers.new('CYCLES')
    tr=ao.animation_data.nla_tracks.new();tr.name=name;st=tr.strips.new(name,1,act);tr.mute=True
    ao.animation_data.action=None;return act
P=ao.pose.bones
def tail(t,amp=12,cyc=1):
    for i in range(5): P['Tail.%d'%i].rotation_quaternion=wrot('Tail.%d'%i,(0,0,1),amp*math.sin(2*math.pi*cyc*t-i*0.6))@P['Tail.%d'%i].rotation_quaternion
def armsdown():
    for S,s in(('L',1),('R',-1)): P['UpperArm.'+S].rotation_quaternion=wrot('UpperArm.'+S,(0,1,0),12*s)
def idle(t):
    b=math.sin(2*math.pi*t)
    P['Chest'].rotation_quaternion=wrot('Chest',(1,0,0),-2*b);P['Spine'].rotation_quaternion=wrot('Spine',(1,0,0),-1*b)
    P['Head'].rotation_quaternion=wrot('Head',(0,1,0),3*math.sin(2*math.pi*t+1))
    for S in 'LR': P['Shoulder.'+S].rotation_quaternion=wrot('Shoulder.'+S,(0,1,0),(1.5 if S=='L' else -1.5)*b)
    armsdown();P['HairBack.1'].rotation_quaternion=wrot('HairBack.1',(1,0,0),2*b)
    tail(t,10,1)
def wave(t):
    w=math.sin(2*math.pi*2*t)
    P['UpperArm.R'].rotation_quaternion=wrot('UpperArm.R',(0,1,0),115)
    P['LowerArm.R'].rotation_quaternion=wrot('LowerArm.R',(0,1,0),40+25*w)
    P['UpperArm.L'].rotation_quaternion=wrot('UpperArm.L',(0,1,0),12)
    P['Head'].rotation_quaternion=wrot('Head',(0,1,0),-6)
    tail(t,15,2)
def walk(t):
    a=math.sin(2*math.pi*t)
    for S,sg in(('L',1),('R',-1)):
        ph=a*sg
        P['UpperLeg.'+S].rotation_quaternion=wrot('UpperLeg.'+S,(1,0,0),16*ph)
        knee=max(0,-math.sin(2*math.pi*t*1+ (0 if S=='L' else math.pi)+0.6))
        P['LowerLeg.'+S].rotation_quaternion=wrot('LowerLeg.'+S,(1,0,0),35*knee)
        P['Foot.'+S].rotation_quaternion=wrot('Foot.'+S,(1,0,0),8*ph)
        P['UpperArm.'+S].rotation_quaternion=wrot('UpperArm.'+S,(1,0,0),-18*ph)@wrot('UpperArm.'+S,(0,1,0),12*(1 if S=='L' else -1))
        P['LowerArm.'+S].rotation_quaternion=wrot('LowerArm.'+S,(1,0,0),10)
    P['Hips'].location=(0,0,0.012*math.cos(4*math.pi*t))
    P['Chest'].rotation_quaternion=wrot('Chest',(0,0,1),5*a);P['Hips'].rotation_quaternion=wrot('Hips',(0,0,1),-5*a)
    tail(t,14,1)
make_action('Idle',72,idle);make_action('Wave',48,wave);make_action('Walk',24,walk);make_action('TailSway',48,lambda t:tail(t,12,1))
ao.animation_data.action=bpy.data.actions['Idle']
sc.frame_start=1;sc.frame_end=144;sc.render.fps=24;sc.frame_set(1)
# scene
sun=bpy.data.objects.new('Sun',bpy.data.lights.new('Sun','SUN'));sun.data.energy=3;sun.rotation_euler=(math.radians(50),0,math.radians(-30));sc.collection.objects.link(sun)
w=bpy.data.worlds.new('W');sc.world=w;w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(0.85,0.86,0.9,1);w.node_tree.nodes['Background'].inputs[1].default_value=0.3
cam=bpy.data.objects.new('Cam',bpy.data.cameras.new('Cam'));sc.collection.objects.link(cam);sc.camera=cam
cam.data.type='ORTHO';cam.data.ortho_scale=1.95;cam.location=(0,-5,0.9);cam.rotation_euler=(math.radians(90),0,0)
sc.render.film_transparent=True;sc.render.engine='BLENDER_EEVEE_NEXT';sc.eevee.taa_render_samples=16;sc.view_settings.view_transform='Standard'
tris=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in PARTS);print('TRIS',tris,'PARTS',len(PARTS),'BONES',len(arm.bones))
bpy.ops.wm.save_as_mainfile(filepath='/workspace/lillith-3d/lowpoly/lillith_lowpoly_v2.blend')
for o in PARTS:
    for md in o.modifiers:
        if md.type=='SOLIDIFY': md.show_viewport=False;md.show_render=False
for m in list(MATS.values())+[OUT]:
    nt=m.node_tree;N=nt.nodes
    for n in list(N): N.remove(n)
    p=N.new('ShaderNodeBsdfPrincipled');p.inputs['Base Color'].default_value=hx(m['base']);p.inputs['Roughness'].default_value=0.9
    nt.links.new(p.outputs[0],N.new('ShaderNodeOutputMaterial').inputs[0])
ao.animation_data.action=None;sc.frame_set(1)
bpy.ops.export_scene.gltf(filepath='/workspace/lillith-3d/lowpoly/lillith_lowpoly_v2.glb',export_format='GLB',export_animations=True,export_animation_mode='ACTIONS',export_apply=False)
