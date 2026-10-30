# Rebuilds Lillith's low-poly office. blender -b -P build.py
import bpy,bmesh,math
from mathutils import Vector as V
D='/workspace/lillith-3d/office/'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
def hx(h):
    h=h.lstrip('#');c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return [((x+0.055)/1.055)**2.4 if x>0.04045 else x/12.92 for x in c]+[1]
MATS={}
def toon(name,base,shadow=None):  # same toon graph as lowpoly/build_v2.py
    if name in MATS: return MATS[name]
    m=bpy.data.materials.new(name);m.use_nodes=True;nt=m.node_tree;N=nt.nodes;L=nt.links
    for n in list(N): N.remove(n)
    out=N.new('ShaderNodeOutputMaterial');d=N.new('ShaderNodeBsdfDiffuse');s2r=N.new('ShaderNodeShaderToRGB')
    r=N.new('ShaderNodeValToRGB');r.color_ramp.interpolation='CONSTANT'
    b=hx(base);sh=hx(shadow) if shadow else [c*0.72 for c in b[:3]]+[1]
    r.color_ramp.elements[0].color=sh;r.color_ramp.elements[1].position=0.25;r.color_ramp.elements[1].color=b
    e=N.new('ShaderNodeEmission')
    L.new(d.outputs[0],s2r.inputs[0]);L.new(s2r.outputs[0],r.inputs[0]);L.new(r.outputs[0],e.inputs[0]);L.new(e.outputs[0],out.inputs[0])
    m['base']=base;m.diffuse_color=b;MATS[name]=m;return m
def flat(name,base):  # unlit flat (sky / city)
    m=bpy.data.materials.new(name);m.use_nodes=True;N=m.node_tree.nodes;N.remove(N['Principled BSDF'])
    e=N.new('ShaderNodeEmission');e.inputs[0].default_value=hx(base);m.node_tree.links.new(e.outputs[0],N['Material Output'].inputs[0])
    m['base']=base;MATS[name]=m;return m
OUT=bpy.data.materials.new('Outline');OUT.use_nodes=True
N=OUT.node_tree.nodes;N.remove(N['Principled BSDF']);e=N.new('ShaderNodeEmission');e.inputs[0].default_value=(0.02,0.015,0.02,1)
OUT.node_tree.links.new(e.outputs[0],N['Material Output'].inputs[0]);OUT.use_backface_culling=True;OUT['base']='#050405'
root=bpy.data.objects.new('Office',None);sc.collection.objects.link(root)
PARTS=[]
CEIL=toon('Ceiling','#7e8c94');WALL=toon('Wall','#9b9a91');PILL=toon('Pillar','#b9b3a5')
FRAME=toon('WindowFrame','#5e7480','#45586a');FLOOR=toon('Floor','#56616a');DESK=toon('DeskTop','#a37c54','#735235')
METAL=toon('Cabinet','#8d9da1','#6f7f86');CHAIR=toon('Chair','#45586a','#2c3a48');BLK=toon('Black','#1e2126')
PAPER=toon('Paper','#e4e6e6','#b8c0c4');COVER=toon('BookCover','#5e7480');CUP=toon('Cup','#a8a4a2');LID=toon('Lid','#4f5f46')
SKY=flat('Sky','#8fb3c1');CITY=flat('City','#3e4a54');CITY2=flat('CityFar','#7a8d97');GLASS=None
def box(name,c,s,mat,outline=0.02,par=root,rz=0):
    bm=bmesh.new();bmesh.ops.create_cube(bm,size=1)
    for v in bm.verts: v.co=V((v.co.x*s[0],v.co.y*s[1],v.co.z*s[2]))
    me=bpy.data.meshes.new(name);bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new(name,me);sc.collection.objects.link(o);o.parent=par;o.location=c;o.rotation_euler.z=rz
    o.data.materials.append(mat);o.data.materials.append(OUT)
    if outline:
        m=o.modifiers.new('outline','SOLIDIFY');m.thickness=outline;m.offset=1;m.use_flip_normals=True;m.use_rim=False;m.material_offset=1
    PARTS.append(o);return o
def cyl(name,c,r,h,mat,n=8,outline=0.008,par=root,r2=None):
    bpy.ops.mesh.primitive_cone_add(vertices=n,radius1=r,radius2=r2 if r2 is not None else r,depth=h,location=c)
    o=bpy.context.object;o.name=name;o.parent=par;o.data.materials.append(mat);o.data.materials.append(OUT)
    if outline:
        m=o.modifiers.new('outline','SOLIDIFY');m.thickness=outline;m.offset=1;m.use_flip_normals=True;m.use_rim=False;m.material_offset=1
    PARTS.append(o);return o
# ---- shell: window wall on y=WY, room spans x -3.4..6.5, ceiling 2.9
WY=3.5;H=2.9;X0,X1=-3.4,6.5
box('Floor',((X0+X1)/2,0.5,-0.05),(X1-X0+0.4,7,0.1),FLOOR,0)
box('Ceiling',((X0+X1)/2,0.5,H+0.05),(X1-X0+0.4,7,0.1),CEIL,0)
box('RightWall',(X1+0.1,0.5,H/2),(0.2,7,H),WALL,0)
box('LeftWall',(X0-0.1,0.5,H/2),(0.2,7,H),WALL,0)
def window_wall(x0,x1,y,panes,name):
    sill,top=0.95,2.45
    box(name+'_Below',((x0+x1)/2,y,sill/2),(x1-x0,0.2,sill),WALL)
    box(name+'_Soffit',((x0+x1)/2,y-0.1,(top+H)/2),(x1-x0,0.4,H-top),WALL)
    box(name+'_Trim',((x0+x1)/2,y-0.31,top-0.02),(x1-x0,0.03,0.04),PILL,0.006)
    box(name+'_Sill',((x0+x1)/2,y-0.06,sill+0.02),(x1-x0,0.22,0.05),FRAME)
    box(name+'_Head',((x0+x1)/2,y-0.04,top-0.03),(x1-x0,0.14,0.07),FRAME)
    w=(x1-x0)/panes
    for i in range(panes+1):
        box(f'{name}_Mullion{i}',(x0+i*w,y-0.04,(sill+top)/2),(0.09 if 0<i<panes else 0.07,0.14,top-sill),FRAME)
        if 0<i<panes: box(f'{name}_MullionB{i}',(x0+i*w+0.08,y-0.02,(sill+top)/2),(0.05,0.1,top-sill),FRAME,0.006)
    for i in range(panes):  # inner stop lines
        cx=x0+(i+0.5)*w
        box(f'{name}_StopB{i}',(cx,y-0.01,sill+0.08),(w-0.1,0.04,0.04),FRAME,0.005)
window_wall(-0.05,X1,WY,3,'WinR')
window_wall(X0,-0.85,WY-0.55,1,'WinL')
box('WinL_Side',(-0.85,WY-0.27,H/2),(0.02,0.55,H),WALL,0)
box('Pillar',(-0.45,WY-0.6,H/2),(0.8,0.5,H),PILL)
box('Pillar_Back',(-0.45,WY-0.2,H/2),(0.8,0.4,H),WALL,0)
# ---- outside: sky + blocky city with stepped towers
box('SkyBackdrop',(1.5,70,10),(200,1,80),SKY,0)
import random;random.seed(7)
for i,(x,y,w,h) in enumerate([(-14,30,8,12),(-8,34,6,16),(-8,34,9,9),(4,30,5,20),(4,30,8,14),(4,30,11,8),(18,32,6,22),(18,32,10,14),(28,30,8,10),(34,36,6,20),(-20,45,10,30),(12,50,10,35)]):
    t=h*0.5-1;box(f'Bldg{i}',(x,y,(t-10)/2),(w,w*0.8,t+10),CITY if y<40 else CITY2,0)
# ---- left desk with cabinets, book stack
def desk(name,cx,cy,w,d,rz=0):
    p=bpy.data.objects.new(name,None);sc.collection.objects.link(p);p.parent=root;p.location=(cx,cy,0);p.rotation_euler.z=rz
    box(name+'_Top',(0,0,0.735),(w,d,0.04),DESK,par=p)
    for sx in (-1,1):
        box(name+f'_Ped{sx}',(sx*(w/2-0.22),0.02,0.36),(0.42,d-0.08,0.71),METAL,par=p)
        for k,z in enumerate((0.55,0.2)):
            box(name+f'_Drw{sx}{k}',(sx*(w/2-0.22),-d/2+0.01,z),(0.38,0.02,0.3),METAL,0.006,par=p)
            box(name+f'_Hdl{sx}{k}',(sx*(w/2-0.22),-d/2-0.005,z+0.07),(0.12,0.02,0.03),CHAIR,0.004,par=p)
    box(name+'_Modesty',(0,d/2-0.06,0.45),(w-0.86,0.03,0.5),METAL,par=p)
    return p
d1=desk('DeskL',-1.6,1.9,2.0,0.8,math.radians(-4))
for k in range(3): box(f'Book{k}',(-0.15,0.0+0.01*k,0.77+k*0.03),(0.5,0.34,0.03),PAPER if k<2 else COVER,0.005,par=d1,rz=0.04*k)
box('BookTop',(-0.15,0.0,0.865),(0.52,0.36,0.012),COVER,0.005,par=d1)
# monitor on left desk edge (cut off in ref)
box('MonL',(-0.75,0.05,1.0),(0.6,0.04,0.38),BLK,par=d1,rz=0.3)
box('MonL_Stand',(-0.75,0.1,0.8),(0.06,0.06,0.13),BLK,par=d1)
d2=desk('DeskR',4.2,2.75,1.6,0.75)
box('MonR',(0.3,0.15,1.02),(0.55,0.04,0.36),BLK,par=d2,rz=-0.4)
box('MonR_Stand',(0.3,0.18,0.8),(0.06,0.06,0.13),BLK,par=d2)
for k in range(3): box(f'PaperR{k}',(-0.45,-0.05,0.765+k*0.025),(0.36,0.27,0.025),PAPER,0.004,par=d2,rz=0.03*k)
box('PaperR_Top',(-0.45,-0.05,0.84),(0.38,0.28,0.01),COVER,0.004,par=d2)
c=cyl('Cup',(0,0,0),0.04,0.12,CUP,par=d2,r2=0.035);c.location=(-0.1,-0.05,0.815)
c=cyl('CupLid',(0,0,0),0.044,0.02,LID,par=d2);c.location=(-0.1,-0.05,0.885)
# ---- office chair
ch=bpy.data.objects.new('Chair',None);sc.collection.objects.link(ch);ch.parent=root;ch.location=(1.6,1.7,0);ch.rotation_euler.z=math.radians(-25)
box('Chair_Seat',(0,0,0.48),(0.5,0.5,0.09),CHAIR,par=ch)
b=box('Chair_Back',(0,0.27,0.92),(0.46,0.09,0.66),CHAIR,par=ch);b.rotation_euler.x=math.radians(-10)
for sx in (-1,1):
    box(f'Chair_ArmPad{sx}',(sx*0.28,0.0,0.68),(0.08,0.32,0.04),CHAIR,par=ch)
    box(f'Chair_ArmPost{sx}',(sx*0.28,0.05,0.58),(0.04,0.04,0.17),BLK,par=ch)
cyl('Chair_Gas',(0,0,0.29),0.03,0.3,BLK,par=ch)
for k in range(5):
    a=k*2*math.pi/5;l=box(f'Chair_Leg{k}',(0.15*math.sin(a),0.15*math.cos(a),0.07),(0.04,0.3,0.035),BLK,par=ch,rz=-a)
    cyl(f'Chair_Wheel{k}',(0.29*math.sin(a),0.29*math.cos(a),0.03),0.03,0.03,BLK,n=6,par=ch)
# ---- lights
sun=bpy.data.objects.new('Sun',bpy.data.lights.new('Sun','SUN'));sun.data.energy=4
sun.rotation_euler=(math.radians(55),0,math.radians(160));sc.collection.objects.link(sun)
w=bpy.data.worlds.new('W');sc.world=w;w.use_nodes=True
w.node_tree.nodes['Background'].inputs[0].default_value=(0.85,0.88,0.92,1);w.node_tree.nodes['Background'].inputs[1].default_value=0.6
for o in PARTS:
    if o.type=='MESH' and o.data.materials and o.data.materials[0]['base'] not in ('#8fb3c1',): pass
cam=bpy.data.objects.new('Cam_Ref',bpy.data.cameras.new('Cam_Ref'));sc.collection.objects.link(cam);sc.camera=cam
cam.location=(-1.0,-0.9,1.45);cam.rotation_euler=(math.radians(92),0,math.radians(-20));cam.data.lens=18;cam.data.shift_y=0.04
cam2=bpy.data.objects.new('Cam_Wide',bpy.data.cameras.new('Cam_Wide'));sc.collection.objects.link(cam2)
cam2.location=(-3.0,-2.6,2.4);cam2.rotation_euler=(math.radians(78),0,math.radians(-38));cam2.data.lens=16
sc.render.engine='BLENDER_EEVEE_NEXT';sc.eevee.taa_render_samples=16;sc.view_settings.view_transform='Standard'
sc.render.resolution_x=1000;sc.render.resolution_y=750
dg=bpy.context.evaluated_depsgraph_get()
tris=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in PARTS)
print('TRIS(base)',tris,'OBJS',len(PARTS))
bpy.ops.wm.save_as_mainfile(filepath=D+'lillith_office.blend')
# renders
for cm,fn in ((cam,'render_ref_view.png'),(cam2,'render_wide_34.png')):
    sc.camera=cm;sc.render.filepath=D+fn;bpy.ops.render.render(write_still=True)
# with Lillith (GLB import; toon look not reapplied -> flat Principled)
bpy.ops.import_scene.gltf(filepath='/workspace/lillith-3d/lowpoly/lillith_lowpoly_v2.glb')
imp=[o for o in bpy.context.selected_objects];top=[o for o in imp if o.parent is None]
for o in top: o.location=(0.9,1.3,0);o.rotation_euler.z=math.radians(-20)
sc.camera=cam2;sc.render.filepath=D+'render_with_lillith.png';bpy.ops.render.render(write_still=True)
for o in imp: bpy.data.objects.remove(o,do_unlink=True)
# GLB: strip outlines, flat Principled colors
for o in PARTS:
    for md in list(o.modifiers): o.modifiers.remove(md)
for m in list(MATS.values())+[OUT]:
    nt=m.node_tree;N=nt.nodes
    for n in list(N): N.remove(n)
    p=N.new('ShaderNodeBsdfPrincipled');p.inputs['Base Color'].default_value=hx(m['base']);p.inputs['Roughness'].default_value=0.9
    nt.links.new(p.outputs[0],N.new('ShaderNodeOutputMaterial').inputs[0])
bpy.ops.export_scene.gltf(filepath=D+'lillith_office.glb',export_format='GLB',use_selection=False,export_cameras=False,export_lights=False)
# comparison
import subprocess
subprocess.run(['python3','-c',f"""
from PIL import Image
a=Image.open('/workspace/lillith-patreon/assets/BG/office_bg.png').convert('RGB').resize((1000,750));b=Image.open('{D}render_ref_view.png').convert('RGB')
c=Image.new('RGB',(2010,750),'white');c.paste(a,(0,0));c.paste(b,(1010,0));c.save('{D}comparison.png')"""])
