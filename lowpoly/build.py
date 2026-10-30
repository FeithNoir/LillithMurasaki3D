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
ell('HairCap',(0,0.008,1.515),(0.118,0.115,0.135),HAIR,20,14,cut=lambda c:c.y<-0.045 and c.z<1.565 and abs(c.x)<0.095)
tube('HairBack',[(0,0.05,1.58),(0,0.075,1.45),(0,0.085,1.25),(0,0.075,1.05),(0,0.06,0.92)],[(0.125,0.08),(0.15,0.07),(0.15,0.055),(0.13,0.04),(0.07,0.02)],HAIR,14,k=2)
for s in (1,-1):
    tube('SideLock'+str(s),[(0.10*s,-0.03,1.55),(0.115*s,-0.05,1.40),(0.12*s,-0.06,1.25),(0.10*s,-0.07,1.12)],[0.03,0.035,0.028,0.0],HAIR,6,(True,False))
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
# legs + heels
for s in (1,-1):
    tube('Leg'+str(s),[(0.075*s,0,0.95),(0.08*s,0,0.78),(0.088*s,-0.005,0.55),(0.093*s,0.0,0.43),(0.10*s,0.005,0.14),(0.10*s,0.0,0.07)],[0.085,0.08,0.05,0.056,0.03,0.03],TIGHT,12,k=2)
    bm=bmesh.new();bmesh.ops.create_cube(bm,size=1)
    for v in bm.verts:
        x,y,z=v.co.x*0.055,v.co.y*0.14,v.co.z*0.035
        if y<0: z-=0.0
        else: z+=0.04*(y/0.07)
        v.co=V((x+0.10*s,y-0.035,z+0.025+ (0.0 if y<0 else 0.0)))
    finish(bm,'Heel'+str(s),SHOE,0.004,False)
    tube('HeelSpike'+str(s),[(0.10*s,0.03,0.08),(0.10*s,0.03,0.0)],[0.012,0.007],SHOE,6)
# arms A-pose
for s in (1,-1):
    sh,el,wr=V((0.165*s,0.0,1.30)),V((0.25*s,0.01,1.07)),V((0.31*s,0.0,0.87))
    tube('Sleeve'+str(s),[sh,(sh+el)/2,el,wr],[0.05,0.045,0.04,0.038],JACK,10)
    tube('Cuff'+str(s),[wr,wr+(wr-el).normalized()*0.02],[0.039,0.036],SHIRT,10)
    ell('Hand'+str(s),wr+(wr-el).normalized()*0.06,(0.03,0.02,0.045),SKIN,10,8)
# tail with light tip
TP=[(0.04,0.10,0.95),(0.14,0.20,0.86),(0.27,0.24,0.92),(0.35,0.22,1.08),(0.36,0.19,1.22),(0.33,0.17,1.30)]
tube('Tail',TP[:5],[0.03,0.085,0.11,0.105,0.075],HAIR,14,(True,False),k=3)
tube('TailTip',TP[3:],[0.09,0.08,0.0],HAIRL,14,(False,False),k=3)
# armature tail
arm=bpy.data.armatures.new('TailRig');ao=bpy.data.objects.new('TailRig',arm);sc.collection.objects.link(ao);ao.parent=root
bpy.context.view_layer.objects.active=ao;bpy.ops.object.mode_set(mode='EDIT')
prev=None;bones=[]
for i in range(len(TP)-1):
    b=arm.edit_bones.new('tail%d'%i);b.head=TP[i];b.tail=TP[i+1]
    if prev: b.parent=prev;b.use_connect=True
    prev=b;bones.append(b.name)
bpy.ops.object.mode_set(mode='OBJECT')
for on in ('Tail','TailTip'):
    o=bpy.data.objects[on];gs=[o.vertex_groups.new(name=n) for n in bones]
    for v in o.data.vertices:
        d=[(V(v.co)-(V(TP[i])+V(TP[i+1]))/2).length for i in range(len(bones))];i=d.index(min(d))
        gs[i].add([v.index],1.0,'REPLACE')
    md=o.modifiers.new('rig','ARMATURE');md.object=ao
    bpy.ops.object.select_all(action='DESELECT')
    o.modifiers.move(len(o.modifiers)-1,0)
ao.animation_data_create();sc.frame_start=1;sc.frame_end=144;sc.render.fps=24
for f in range(1,145,6):
    for i,bn in enumerate(bones):
        pb=ao.pose.bones[bn];pb.rotation_mode='XYZ'
        ang=math.radians(10)*math.sin(2*math.pi*(f-1)/48-i*0.6)
        pb.rotation_euler=(0,0,ang);pb.keyframe_insert('rotation_euler',frame=f)
# turntable on root
root.rotation_euler=(0,0,0);root.keyframe_insert('rotation_euler',frame=1)
root.rotation_euler=(0,0,2*math.pi);root.keyframe_insert('rotation_euler',frame=145)
for fc in root.animation_data.action.fcurves:
    for k in fc.keyframe_points: k.interpolation='LINEAR'
sc.frame_set(1)
# scene
sun=bpy.data.objects.new('Sun',bpy.data.lights.new('Sun','SUN'));sun.data.energy=3;sun.rotation_euler=(math.radians(50),0,math.radians(-30));sc.collection.objects.link(sun)
w=bpy.data.worlds.new('W');sc.world=w;w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(0.85,0.86,0.9,1);w.node_tree.nodes['Background'].inputs[1].default_value=0.3
cam=bpy.data.objects.new('Cam',bpy.data.cameras.new('Cam'));sc.collection.objects.link(cam);sc.camera=cam
cam.data.type='ORTHO';cam.data.ortho_scale=1.95;cam.location=(0,-5,0.9);cam.rotation_euler=(math.radians(90),0,0)
sc.render.film_transparent=True;sc.render.engine='BLENDER_EEVEE_NEXT';sc.eevee.taa_render_samples=16;sc.view_settings.view_transform='Standard'
tris=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in PARTS);print('TRIS',tris,'PARTS',len(PARTS))
bpy.ops.wm.save_as_mainfile(filepath='/workspace/lillith-3d/lowpoly/lillith_lowpoly.blend')
# GLB export: swap to principled copies
import copy
for o in PARTS:
    for md in o.modifiers:
        if md.type=='SOLIDIFY': md.show_viewport=False;md.show_render=False
saved={}
for m in list(MATS.values())+[OUT]:
    nt=m.node_tree;N=nt.nodes
    for n in list(N): N.remove(n)
    p=N.new('ShaderNodeBsdfPrincipled');p.inputs['Base Color'].default_value=hx(m['base']);p.inputs['Roughness'].default_value=0.9
    nt.links.new(p.outputs[0],N.new('ShaderNodeOutputMaterial').inputs[0])
sc.frame_set(1);root.rotation_euler=(0,0,0)
bpy.ops.export_scene.gltf(filepath='/workspace/lillith-3d/lowpoly/lillith_lowpoly.glb',export_format='GLB',export_animations=True,export_apply=False)
