# Lillith TRELLIS v2: limpieza, remesh, bake con cara proyectada del sprite, manos nuevas, rig 34 huesos, animaciones
import bpy,bmesh,math,colorsys,os
from mathutils import Vector as V, Quaternion as Q
from mathutils.bvhtree import BVHTree
OUT='/workspace/lillith-3d/trellis_v2/'
SPRITE='/workspace/lillith-patreon/assets/Suit/LM_Suit_V1.png'
VOX=float(os.environ.get('VOX','0.006'));TARGET=int(os.environ.get('TARGET','24000'))
bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene
bpy.ops.import_scene.gltf(filepath='/workspace/lillith-3d/trellis/model.glb')
src=[o for o in sc.objects if o.type=='MESH'][0]
mw=src.matrix_world.copy();src.parent=None;src.matrix_world=mw
for o in list(sc.objects):
    if o.type=='EMPTY': bpy.data.objects.remove(o)
def activate(o):
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
activate(src);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
# ---- 1. normalizar + limpiar
me=src.data;bm=bmesh.new();bm.from_mesh(me)
mn=V([min(v.co[i] for v in bm.verts) for i in range(3)]);mx=V([max(v.co[i] for v in bm.verts) for i in range(3)])
s=1.65/(mx.z-mn.z);c=(mn+mx)/2
for v in bm.verts: v.co=V(((v.co.x-c.x)*s,(v.co.y-c.y)*s,(v.co.z-mn.z)*s))
bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=0.0005)
bmesh.ops.dissolve_degenerate(bm,edges=bm.edges,dist=1e-6)
bm.verts.ensure_lookup_table();seen=set();isl=[]
for v in bm.verts:
    if v.index in seen: continue
    st=[v];cur=[];seen.add(v.index)
    while st:
        a=st.pop();cur.append(a)
        for e in a.link_edges:
            b=e.other_vert(a)
            if b.index not in seen: seen.add(b.index);st.append(b)
    isl.append(cur)
bmesh.ops.delete(bm,geom=[v for i in isl if len(i)<200 for v in i],context='VERTS')
bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
bm.to_mesh(me);bm.free();src.name='TRELLIS_src'
# ---- 2. manos deformes: borrar en una copia de forma (la fuente de textura queda intacta)
WR=V((-0.33,-0.30,1.175));WL=V((0.235,-0.13,0.975))
bm=bmesh.new();bm.from_mesh(src.data)
kill=[v for v in bm.verts if (v.co.x<-0.315 and v.co.z>1.18 and v.co.y<-0.17) or ((v.co-V((0.22,-0.14,0.91))).length<0.085 and v.co.z<WL.z-0.01)]
print('HAND VERTS REMOVED',len(kill));bmesh.ops.delete(bm,geom=kill,context='VERTS')
bm.verts.ensure_lookup_table();bm.verts.index_update();seen=set();dead=[]
for v in list(bm.verts):
    if v.index in seen: continue
    st=[v];cur=[];seen.add(v.index)
    while st:
        a=st.pop();cur.append(a)
        for e in a.link_edges:
            b=e.other_vert(a)
            if b.index not in seen: seen.add(b.index);st.append(b)
    if len(cur)<300: dead+=cur
print('LOOSE REMOVED',len(dead));bmesh.ops.delete(bm,geom=dead,context='VERTS')
bm.to_mesh(src.data);bm.free()
shape=src.copy();shape.data=src.data.copy();sc.collection.objects.link(shape);shape.name='Lillith_TRELLIS'
bm=bmesh.new();bm.from_mesh(shape.data);bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=300);bm.to_mesh(shape.data);bm.free()
# ---- 3. remesh voxel + suavizado leve + decimate
activate(shape)
r=shape.modifiers.new('vox','REMESH');r.mode='VOXEL';r.voxel_size=VOX;r.use_smooth_shade=True
bpy.ops.object.modifier_apply(modifier='vox')
sm=shape.modifiers.new('sm','SMOOTH');sm.factor=0.4;sm.iterations=2;bpy.ops.object.modifier_apply(modifier='sm')
tri=sum(len(p.vertices)-2 for p in shape.data.polygons);print('REMESH TRIS',tri)
d=shape.modifiers.new('dec','DECIMATE');d.ratio=min(1,TARGET/tri);bpy.ops.object.modifier_apply(modifier='dec')
for p in shape.data.polygons: p.use_smooth=True
shape.data.materials.clear()
print('FINAL BODY TRIS',sum(len(p.vertices)-2 for p in shape.data.polygons))
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=0.004);bpy.ops.object.mode_set(mode='OBJECT')
# ---- 4. material fuente: textura original con mas contraste + cara del sprite proyectada en frente
sm=src.data.materials[0];nt=sm.node_tree;N=nt.nodes;L=nt.links
tex=[n for n in N if n.type=='TEX_IMAGE'][0];out=[n for n in N if n.type=='OUTPUT_MATERIAL'][0]
bc=N.new('ShaderNodeBrightContrast');bc.inputs['Contrast'].default_value=0.05;L.new(tex.outputs[0],bc.inputs[0])
hs=N.new('ShaderNodeHueSaturation');hs.inputs['Saturation'].default_value=1.04;L.new(bc.outputs[0],hs.inputs['Color'])
geo=N.new('ShaderNodeNewGeometry');sep=N.new('ShaderNodeSeparateXYZ');L.new(geo.outputs['Position'],sep.inputs[0])
def math_(op,a,b=None):
    m=N.new('ShaderNodeMath');m.operation=op
    for i,x in enumerate((a,b)):
        if x is None: continue
        if isinstance(x,(int,float)): m.inputs[i].default_value=x
        else: L.new(x,m.inputs[i])
    return m.outputs[0]
u=math_('ADD',math_('MULTIPLY',sep.outputs[0],0.62793),0.50610)
vv=math_('ADD',math_('MULTIPLY',sep.outputs[2],0.55766),0.02027)
cmb=N.new('ShaderNodeCombineXYZ');L.new(u,cmb.inputs[0]);L.new(vv,cmb.inputs[1])
spr=N.new('ShaderNodeTexImage');spr.image=bpy.data.images.load(SPRITE);spr.extension='CLIP';spr.interpolation='Cubic';L.new(cmb.outputs[0],spr.inputs[0])
def rng(x,a,b):
    m=N.new('ShaderNodeMapRange');m.clamp=True;L.new(x,m.inputs[0]);m.inputs[1].default_value=a;m.inputs[2].default_value=b;return m.outputs[0]
sepn=N.new('ShaderNodeSeparateXYZ');L.new(geo.outputs['Normal'],sepn.inputs[0])
fz=rng(sep.outputs[2],1.33,1.38)
fx=math_('MULTIPLY',rng(sep.outputs[0],-0.24,-0.20),rng(sep.outputs[0],0.18,0.14))
fn=rng(math_('MULTIPLY',sepn.outputs[1],-1.0),0.45,0.8)
mask=math_('MULTIPLY',math_('MULTIPLY',math_('MULTIPLY',fz,fx),fn),spr.outputs['Alpha'])
mix=N.new('ShaderNodeMix');mix.data_type='RGBA';L.new(mask,mix.inputs['Factor']);L.new(hs.outputs[0],mix.inputs[6]);L.new(spr.outputs[0],mix.inputs[7])
em=N.new('ShaderNodeEmission');L.new(mix.outputs[2],em.inputs[0]);L.new(em.outputs[0],out.inputs[0])
# ---- 5. bake
img=bpy.data.images.new('Lillith_TRELLIS_baked',2048,2048);img.filepath_raw=OUT+'lillith_trellis_v2_albedo.png';img.file_format='PNG'
bmat=bpy.data.materials.new('TRELLIS_baked');bmat.use_nodes=True;bn=bmat.node_tree.nodes;it=bn.new('ShaderNodeTexImage');it.image=img;bn.active=it
shape.data.materials.append(bmat)
sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=1;sc.render.bake.use_selected_to_active=True;sc.render.bake.cage_extrusion=0.02;sc.render.bake.max_ray_distance=0.06;sc.render.bake.margin=8
bpy.ops.object.select_all(action='DESELECT');src.select_set(True);shape.select_set(True);bpy.context.view_layer.objects.active=shape
bpy.ops.object.bake(type='EMIT');img.save();print('BAKED')
bpy.data.objects.remove(src)
# ---- 6. medidas para el rig (cortes horizontales)
bv=[v.co.copy() for v in shape.data.vertices]
def slice_c(z,f=lambda p:True,t=0.012):
    pts=[p for p in bv if abs(p.z-z)<t and f(p)];return sum(pts,V())/len(pts) if pts else None
LEG={}
for S,sg in(('L',1),('R',-1)):
    LEG[S]=[slice_c(z,lambda p,sg=sg:p.x*sg>0.02 and p.y<0.12) for z in (0.80,0.45,0.13)]
    print('LEG',S,[tuple(round(c,3) for c in p) for p in LEG[S]])
ft={S:[p for p in bv if p.z<0.06 and p.x*sg>0.0] for S,sg in(('L',1),('R',-1))}
TOE={S:min(ft[S],key=lambda p:p.y) for S in ft};print('TOE',{k:tuple(round(c,3) for c in v) for k,v in TOE.items()})
# ---- 7. materiales toon + contorno
def hx(h):
    h=h.lstrip('#');c=[int(h[i:i+2],16)/255 for i in (0,2,4)];return [((x+0.055)/1.055)**2.4 if x>0.04045 else x/12.92 for x in c]+[1]
def toon_tex(name,image=None,color=None):
    m=bpy.data.materials.new(name);m.use_nodes=True;nt=m.node_tree;N=nt.nodes;L=nt.links
    for n in list(N): N.remove(n)
    o=N.new('ShaderNodeOutputMaterial');d=N.new('ShaderNodeBsdfDiffuse');s2=N.new('ShaderNodeShaderToRGB');r=N.new('ShaderNodeValToRGB')
    r.color_ramp.interpolation='CONSTANT';r.color_ramp.elements[0].color=(0.72,0.70,0.78,1);r.color_ramp.elements[1].position=0.3;r.color_ramp.elements[1].color=(1,1,1,1)
    mul=N.new('ShaderNodeMix');mul.data_type='RGBA';mul.blend_type='MULTIPLY';mul.inputs['Factor'].default_value=1
    if image: t=N.new('ShaderNodeTexImage');t.image=image;L.new(t.outputs[0],mul.inputs[6])
    else: mul.inputs[6].default_value=hx(color)
    e=N.new('ShaderNodeEmission');L.new(d.outputs[0],s2.inputs[0]);L.new(s2.outputs[0],r.inputs[0]);L.new(r.outputs[0],mul.inputs[7]);L.new(mul.outputs[2],e.inputs[0]);L.new(e.outputs[0],o.inputs[0])
    m['image']=image.name if image else '';m['color']=color or '';return m
OUTL=bpy.data.materials.new('Outline');OUTL.use_nodes=True;N=OUTL.node_tree.nodes;N.remove(N['Principled BSDF']);e=N.new('ShaderNodeEmission');e.inputs[0].default_value=(0.02,0.015,0.02,1)
OUTL.node_tree.links.new(e.outputs[0],N['Material Output'].inputs[0]);OUTL.use_backface_culling=True
BODY=toon_tex('Lillith_TRELLIS_toon',img);shape.data.materials.clear();shape.data.materials.append(BODY);shape.data.materials.append(OUTL)
SKIN=toon_tex('Skin_hands',color='#f2d2bf')
# ---- 8. manos nuevas con 5 dedos
def tube(bm,pts,rad,n=8):
    rings=[]
    for i,p in enumerate(pts):
        t=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized();ref=V((0,0,1)) if abs(t.z)<0.9 else V((1,0,0))
        a=t.cross(ref).normalized();b=t.cross(a).normalized();rx,ry=rad[i] if isinstance(rad[i],tuple) else (rad[i],rad[i])
        rings.append([bm.verts.new(p+a*math.cos(2*math.pi*k/n)*rx+b*math.sin(2*math.pi*k/n)*ry) for k in range(n)])
    for i in range(len(rings)-1):
        for k in range(n): bm.faces.new((rings[i][k],rings[i][(k+1)%n],rings[i+1][(k+1)%n],rings[i+1][k]))
    bm.faces.new(list(reversed(rings[0])));bm.faces.new(rings[-1])
def hand(name,w,f,nrm,curl=0.15,spread=0.12,scale=1.0):
    f=V(f).normalized();n=(V(nrm)-f*V(nrm).dot(f)).normalized();sd=f.cross(n);k=scale
    bm=bmesh.new()
    # palma
    bmesh.ops.create_cube(bm,size=1)
    for v in bm.verts:
        x,y,z=v.co;tap=1-0.15*(z+0.5)
        v.co=w+f*((z+0.5)*0.075*k-0.012*k)+sd*(x*0.058*k*tap)+n*(y*0.024*k)
    for i,(off,L_) in enumerate(((-0.021,0.048),(-0.007,0.056),(0.007,0.060),(0.021,0.054))):
        base=w+f*0.063*k+sd*off*k;dirf=(f+sd*off/0.021*spread).normalized()
        pts=[base];d=dirf
        for j in range(3):
            d=(d-n*curl).normalized();pts.append(pts[-1]+d*L_*k/3)
        tube(bm,pts,[0.0085*k,0.008*k,0.0075*k,0.006*k],6)
    tb=w+f*0.02*k-sd*0.028*k;td=(f*0.6-sd*0.8-n*0.3).normalized();pts=[tb,tb+td*0.025*k,tb+(td+f*0.5).normalized()*0.05*k]
    tube(bm,pts,[0.011*k,0.009*k,0.007*k],6)
    me=bpy.data.meshes.new(name);bm.to_mesh(me);bm.free();o=bpy.data.objects.new(name,me);sc.collection.objects.link(o)
    me.materials.append(SKIN);me.materials.append(OUTL);[setattr(p,'use_smooth',True) for p in me.polygons];return o
# derecha: mano levantada saludando (palma al frente); izquierda: en la cadera, dedos hacia abajo/atras
HR=hand('Hand_R',WR+V((0.004,0.0,-0.004)),(-0.30,-0.12,0.95),(0.05,-1,0.1),0.12,0.10,1.25)
HL=hand('Hand_L',WL+V((-0.005,0.0,-0.003)),(-0.25,0.15,-0.95),(-1,0.1,0.0),0.35,0.05,1.25)
# ---- 9. esqueleto 34 huesos (mismos nombres que low-poly v2)
arm=bpy.data.armatures.new('LillithRig');ao=bpy.data.objects.new('LillithRig',arm);sc.collection.objects.link(ao)
root=bpy.data.objects.new('Lillith',None);sc.collection.objects.link(root);ao.parent=root
activate(ao);bpy.ops.object.mode_set(mode='EDIT');EB=arm.edit_bones
def Bn(n,h,t,par=None,con=False):
    b=EB.new(n);b.head=V(h);b.tail=V(t);b.roll=0
    if par: b.parent=EB[par];b.use_connect=con
hipc=(LEG['L'][0]+LEG['R'][0])/2;HY=hipc.y
Bn('Root',(0,HY,0),(0,HY-0.2,0))
Bn('Hips',(0,HY,0.86),(0,HY-0.01,1.0),'Root');Bn('Spine',(0,HY-0.01,1.0),(0,HY-0.03,1.15),'Hips',True);Bn('Chest',(0,HY-0.03,1.15),(-0.01,HY-0.04,1.32),'Spine',True)
Bn('Neck',(-0.01,HY-0.04,1.32),(-0.03,HY-0.04,1.40),'Chest',True);Bn('Head',(-0.03,HY-0.04,1.40),(-0.03,HY-0.04,1.63),'Neck',True)
ARMS={'R':[V((-0.16,-0.12,1.30)),V((-0.31,-0.19,1.02)),WR],'L':[V((0.16,-0.10,1.30)),V((0.34,-0.07,1.11)),WL]}
HD={'R':(-0.30,-0.12,0.95),'L':(-0.25,0.15,-0.95)}
for S,sg in(('L',1),('R',-1)):
    sh,el,wr=ARMS[S]
    Bn('Shoulder.'+S,(0.03*sg,HY-0.06,1.30),sh,'Chest');Bn('UpperArm.'+S,sh,el,'Shoulder.'+S,True);Bn('LowerArm.'+S,el,wr,'UpperArm.'+S,True)
    Bn('Hand.'+S,wr,wr+V(HD[S]).normalized()*0.14,'LowerArm.'+S,True)
    h,k,a=LEG[S];h=V((h.x,h.y,0.86))
    Bn('UpperLeg.'+S,h,k,'Hips');Bn('LowerLeg.'+S,k,a+V((0,0,-0.04)),'UpperLeg.'+S,True)
    an=a+V((0,0,-0.04));Bn('Foot.'+S,an,(TOE[S]+an)/2+V((0,0,0.0)),'LowerLeg.'+S,True);Bn('Toes.'+S,(TOE[S]+an)/2,TOE[S]+V((0,0,0.01)),'Foot.'+S,True)
Bn('Ear.R',(-0.12,-0.02,1.57),(-0.15,-0.02,1.66),'Head');Bn('Ear.L',(0.06,-0.02,1.57),(0.09,-0.02,1.66),'Head')
Bn('SideLock.R',(-0.15,-0.05,1.48),(-0.38,0.02,1.05),'Head');Bn('SideLock.L',(0.12,-0.05,1.48),(0.30,0.02,1.0),'Head')
HB=[(-0.02,0.08,1.50),(0,0.18,1.28),(0,0.24,1.08),(0,0.22,0.92)]
for i in range(3): Bn('HairBack.%d'%i,HB[i],HB[i+1],'Head' if i==0 else 'HairBack.%d'%(i-1),i>0)
TP=[(0.05,0.08,0.85),(0.14,0.18,0.72),(0.22,0.26,0.58),(0.32,0.30,0.52),(0.40,0.30,0.60),(0.42,0.28,0.72)]
for i in range(5): Bn('Tail.%d'%i,TP[i],TP[i+1],'Hips' if i==0 else 'Tail.%d'%(i-1),i>0)
bpy.ops.object.mode_set(mode='OBJECT')
BON={b.name:(b.head_local.copy(),b.tail_local.copy()) for b in arm.bones}
# ---- 10. pesos: automaticos + limpieza por color (morado = pelo/cola/orejas)
shape.parent=root;HR.parent=root;HL.parent=root
bpy.ops.object.select_all(action='DESELECT');shape.select_set(True);ao.select_set(True);bpy.context.view_layer.objects.active=ao
try: bpy.ops.object.parent_set(type='ARMATURE_AUTO');print('AUTO OK')
except Exception as ex: print('AUTO FAIL',ex)
shape.parent=root;shape.matrix_parent_inverse.identity()
for md in list(shape.modifiers):
    if md.type=='ARMATURE': shape.modifiers.remove(md)
px=list(img.pixels);W_=img.size[0]
uvl=shape.data.uv_layers.active.data;vuv={}
for p in shape.data.polygons:
    for li,vi in zip(p.loop_indices,p.vertices): vuv.setdefault(vi,uvl[li].uv.copy())
HAIRB=['Head','HairBack.0','HairBack.1','HairBack.2','SideLock.L','SideLock.R','Ear.L','Ear.R']+['Tail.%d'%i for i in range(5)]
HAIRONLY=set(HAIRB)-{'Head'}
def segd(p,a,b):
    ab=b-a;t=max(0,min(1,(p-a).dot(ab)/ab.length_squared));return (p-(a+ab*t)).length
def dist_w(p,cands,soft=False):
    ds=sorted((segd(p,*BON[c]),c) for c in cands)[:2]
    if len(ds)<2 or (not soft and ds[1][0]-ds[0][0]>0.05): return {ds[0][1]:1.0}
    pw=1.5 if soft else 3
    w0=1/(ds[0][0]+0.02)**pw;w1=1/(ds[1][0]+0.02)**pw;return {ds[0][1]:w0/(w0+w1),ds[1][1]:w1/(w0+w1)}
G={b:(shape.vertex_groups.get(b) or shape.vertex_groups.new(name=b)) for b in BON}
gi={g.index:g.name for g in shape.vertex_groups};nh=0
for v in shape.data.vertices:
    uv=vuv.get(v.index,(0,0));x=min(W_-1,int(uv[0]*W_));y=min(W_-1,int(uv[1]*W_));i=(y*W_+x)*4
    r,g_,b=px[i:i+3];h,s_,val=colorsys.rgb_to_hsv(r,g_,b)
    purple=0.70<h<0.93 and s_>0.2 and val>0.12
    if purple and (v.co.z<0.42 or min(segd(v.co,*BON[b]) for b in HAIRB)>0.3): purple=False
    td_=min(segd(v.co,*BON['Tail.%d'%i]) for i in range(5))
    if not purple and td_<0.11 and td_<segd(v.co,*BON['UpperLeg.L'])-0.04 and td_<segd(v.co,*BON['Hips'])-0.03: purple=True
    cur={gi[e.group]:e.weight for e in v.groups if e.weight>0.001}
    p=v.co
    if purple:
        nh+=1
        # tronco/pelo: el pelo nunca sigue a brazos/piernas
        if p.z<1.1 and min(segd(p,*BON['Tail.%d'%i]) for i in range(5))<min(0.16,min(segd(p,*BON[b]) for b in ('HairBack.1','HairBack.2','SideLock.L','SideLock.R'))): new=dist_w(p,['Hips']+['Tail.%d'%i for i in range(5)],True)
        elif p.z>1.52 and abs(p.x+0.03)<0.2: new=dist_w(p,['Head','Ear.L','Ear.R']) if p.z>1.57 else {'Head':1.0}
        else: new=dist_w(p,['Head','HairBack.0','HairBack.1','HairBack.2','SideLock.L','SideLock.R'],True)
    else:
        new={k:w for k,w in cur.items() if k not in HAIRONLY}
        tot=sum(new.values())
        if tot<0.05: new=dist_w(p,[b for b in BON if b not in HAIRONLY and b!='Root'])
        else: new={k:w/tot for k,w in new.items()}
        if p.z<0.80:
            dL=min(segd(p,*BON[b+'.L']) for b in ('UpperLeg','LowerLeg','Foot','Toes'));dR=min(segd(p,*BON[b+'.R']) for b in ('UpperLeg','LowerLeg','Foot','Toes'))
            S='L' if dL<dR else 'R';O='R' if S=='L' else 'L'
            new={k:w for k,w in new.items() if not k.endswith('.'+O)}
            if p.z<0.6: new={k:w for k,w in new.items() if k.endswith('.'+S)}
            if sum(new.values())<0.05: new=dist_w(p,[b+'.'+S for b in ('UpperLeg','LowerLeg','Foot','Toes')])
            t_=sum(new.values());new={k:w/t_ for k,w in new.items()}
    for g in shape.vertex_groups: g.remove([v.index])
    for k,w in new.items(): G[k].add([v.index],w,'REPLACE')
print('PURPLE VERTS',nh,'of',len(shape.data.vertices))
for o,S in((shape,None),(HR,'R'),(HL,'L')):
    if S: g=o.vertex_groups.new(name='Hand.'+S);g.add([v.index for v in o.data.vertices],1.0,'REPLACE')
    md=o.modifiers.new('rig','ARMATURE');md.object=ao
    so=o.modifiers.new('outline','SOLIDIFY');so.thickness=0.005 if o==shape else 0.003;so.offset=1;so.use_flip_normals=True;so.use_rim=False;so.material_offset=1
# ---- 11. animaciones (adaptadas de low-poly v2 a la pose de TRELLIS)
for pb in ao.pose.bones: pb.rotation_mode='QUATERNION'
def wrot(bn,axis,deg):
    m=arm.bones[bn].matrix_local.to_3x3();return Q((m.inverted()@V(axis)).normalized(),math.radians(deg))
P=ao.pose.bones
def make_action(name,length,fn):
    act=bpy.data.actions.new(name);act.use_fake_user=True;ao.animation_data_create();ao.animation_data.action=act
    for f in range(1,length+2,2 if length<40 else 3):
        t=(f-1)/length
        for pb in P: pb.rotation_quaternion=(1,0,0,0);pb.location=(0,0,0)
        fn(t)
        for pb in P:
            pb.keyframe_insert('rotation_quaternion',frame=f)
            if pb.name in('Root','Hips'): pb.keyframe_insert('location',frame=f)
    for fc in act.fcurves: fc.modifiers.new('CYCLES')
    tr=ao.animation_data.nla_tracks.new();tr.name=name;tr.strips.new(name,1,act);tr.mute=True;ao.animation_data.action=None
def R(bn,axis,deg): P[bn].rotation_quaternion=wrot(bn,axis,deg)@P[bn].rotation_quaternion
def tail(t,amp=12,cyc=1):
    for i in range(5): R('Tail.%d'%i,(0,0,1),0.55*amp*math.sin(2*math.pi*cyc*t-i*0.6))
def hair(t,amp=2):
    for i in range(3): R('HairBack.%d'%i,(1,0,0),amp*math.sin(2*math.pi*t-i*0.5))
    for S in 'LR': R('SideLock.'+S,(1,0,0),amp*0.8*math.sin(2*math.pi*t-0.3))
def idle(t):
    b=math.sin(2*math.pi*t);R('Spine',(1,0,0),-1*b);R('Chest',(1,0,0),-2*b);R('Head',(0,1,0),3*math.sin(2*math.pi*t+1))
    R('Shoulder.L',(0,1,0),1.5*b);R('Shoulder.R',(0,1,0),-1.5*b);R('LowerArm.R',(0,1,0),3*b);hair(t);tail(t,10,1)
    for S in 'LR': R('Ear.'+S,(1,0,0),4*max(0,math.sin(2*math.pi*t*2-1))**8)
def wave(t):
    w=math.sin(2*math.pi*2*t);R('UpperArm.R',(0,1,0),8);R('LowerArm.R',(0,1,0),18*w);R('Hand.R',(0,1,0),12*w);R('Head',(0,1,0),-5);R('Head',(1,0,0),-3)
    hair(t,2);tail(t,16,2)
def walk(t):
    a=math.sin(2*math.pi*t)
    for S,sg in(('L',1),('R',-1)):
        ph=a*sg;R('UpperLeg.'+S,(1,0,0),15*ph);knee=max(0,-math.sin(2*math.pi*t+(0 if S=='L' else math.pi)+0.6));R('LowerLeg.'+S,(1,0,0),30*knee);R('Foot.'+S,(1,0,0),6*ph)
    P['Hips'].location=(0,0,0.01*math.cos(4*math.pi*t));R('Hips',(0,0,1),-4*a);R('Chest',(0,0,1),4*a);R('UpperArm.R',(1,0,0),-6*a)
    hair(t*2,3);tail(t,14,1)
make_action('Idle',72,idle);make_action('Wave',48,wave);make_action('Walk',24,walk);make_action('TailSway',48,lambda t:tail(t,12,1))
ao.animation_data.action=None
# ---- 12. escena
sun=bpy.data.objects.new('Sun',bpy.data.lights.new('Sun','SUN'));sun.data.energy=3;sun.rotation_euler=(math.radians(50),0,math.radians(-30));sc.collection.objects.link(sun)
w=bpy.data.worlds.new('W');sc.world=w;w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(0.85,0.86,0.9,1);w.node_tree.nodes['Background'].inputs[1].default_value=0.3
cam=bpy.data.objects.new('Cam',bpy.data.cameras.new('Cam'));sc.collection.objects.link(cam);sc.camera=cam
cam.data.type='ORTHO';cam.data.ortho_scale=1.9;cam.location=(0,-5,0.83);cam.rotation_euler=(math.radians(90),0,0)
sc.render.film_transparent=True;sc.render.engine='BLENDER_EEVEE_NEXT';sc.eevee.taa_render_samples=16;sc.view_settings.view_transform='Standard'
sc.frame_start=1;sc.frame_end=144;sc.render.fps=24
img.pack()
T={o.name:sum(len(p.vertices)-2 for p in o.data.polygons) for o in (shape,HR,HL)};print('TRIS',T,sum(T.values()),'BONES',len(arm.bones))
bpy.ops.wm.save_as_mainfile(filepath=OUT+'lillith_trellis_v2.blend')
# ---- 13. GLB (materiales Principled con la textura horneada)
for o in (shape,HR,HL):
    for md in o.modifiers:
        if md.type=='SOLIDIFY': md.show_viewport=md.show_render=False
for m in (BODY,SKIN):
    nt=m.node_tree;N=nt.nodes
    for n in list(N): N.remove(n)
    p=N.new('ShaderNodeBsdfPrincipled');p.inputs['Roughness'].default_value=0.9
    if m['image']: t=N.new('ShaderNodeTexImage');t.image=bpy.data.images[m['image']];nt.links.new(t.outputs[0],p.inputs['Base Color'])
    else: p.inputs['Base Color'].default_value=hx(m['color'])
    nt.links.new(p.outputs[0],N.new('ShaderNodeOutputMaterial').inputs[0])
for o in (shape,HR,HL):
    if len(o.data.materials)>1: o.data.materials.pop(index=1)
sc.frame_set(1)
bpy.ops.export_scene.gltf(filepath=OUT+'lillith_trellis_v2.glb',export_format='GLB',export_animations=True,export_animation_mode='ACTIONS',export_apply=False)
