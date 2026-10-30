# Office + Lillith v4 spinning in the office chair. blender -b ../office/lillith_office.blend -P scene_v4.py -- [render|test|export]
import bpy,math,sys,os
from mathutils import Vector as V
D='/workspace/lillith-3d/lowpoly_v4/';sc=bpy.context.scene;mode=sys.argv[-1]
with bpy.data.libraries.load(D+'lillith_lowpoly_v4.blend',link=False) as (src,dst): dst.objects=list(src.objects)
keep=[]
for o in dst.objects:
    top=o
    while top.parent: top=top.parent
    if top.name.startswith('Lillith'): sc.collection.objects.link(o);keep.append(o)
    else: bpy.data.objects.remove(o)
L=bpy.data.objects['Lillith'];ao=bpy.data.objects['LillithRig'];F=bpy.data.objects['Face']
chair=bpy.data.objects['Chair'];base_rz=chair.rotation_euler.z
# spinning top part of the chair (seat/back/arms); legs+wheels stay
top=bpy.data.objects.new('ChairTop',None);sc.collection.objects.link(top);top.parent=chair;bpy.context.view_layer.update()
for o in list(chair.children):
    if o.name.startswith(('Chair_Seat','Chair_Back','Chair_Arm')): mw=o.matrix_world.copy();o.parent=top;o.matrix_world=mw
L.location=chair.matrix_world.translation+V((0,0,0));L.rotation_euler.z=base_rz
# animation: armature ChairSpin (Root bone spin), face ChairSpin, ChairTop spin keyed with the same curve
def spin_angle(f):
    u=min(1,max(0,(f-25)/120));e=u*u*(3-2*u);return 720*e
ao.animation_data.action=bpy.data.actions['ChairSpin']
K=F.data.shape_keys;K.animation_data.action=bpy.data.actions['ChairSpin_Face']
for t in ao.animation_data.nla_tracks: t.mute=True
for t in K.animation_data.nla_tracks: t.mute=True
top.animation_data_create();act=bpy.data.actions.new('ChairSpin_Chair');top.animation_data.action=act
for f in range(1,170):
    top.rotation_euler.z=math.radians(spin_angle(f));top.keyframe_insert('rotation_euler',index=2,frame=f)
for fc in act.fcurves:
    for kp in fc.keyframe_points: kp.interpolation='LINEAR'
sc.frame_start=1;sc.frame_end=168;sc.render.fps=24
cam=bpy.data.objects.new('Cam_Spin',bpy.data.cameras.new('Cam_Spin'));sc.collection.objects.link(cam);sc.camera=cam
tgt=chair.matrix_world.translation+V((0,0,0.82));cam.location=tgt+V((-1.15,-2.55,0.42));cam.data.lens=32
cam.rotation_euler=(tgt-cam.location).to_track_quat('-Z','Y').to_euler()
sc.render.resolution_x=1280;sc.render.resolution_y=720;sc.eevee.taa_render_samples=8;sc.view_settings.view_transform='Standard'
if mode=='test':
    for f in (1,60,85,110,150):
        sc.frame_set(f);sc.render.filepath=f'/tmp/spin_{f:03d}.png';bpy.ops.render.render(write_still=True)
if mode=='render':
    os.makedirs('/tmp/spinvid',exist_ok=True)
    for f in range(1,169):
        sc.frame_set(f);sc.render.filepath='/tmp/spinvid/f_%04d.png'%f;bpy.ops.render.render(write_still=True)
if mode=='export':
    sc.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=D+'office_chair_spin_v4.blend',copy=True)
    # glTF: name the three ChairSpin pieces as same-named NLA tracks so they merge into one animation
    ao.animation_data.action=None;K.animation_data.action=None;top.animation_data.action=None
    for t in ao.animation_data.nla_tracks: t.mute=False
    t=top.animation_data.nla_tracks.new();t.name='ChairSpin';t.strips.new('ChairSpin',1,act)
    exec(open(D+'sfsafe.py').read())
    face_single_material(F,D+'face_palette_v4_scene.png');skinned_to_root();flatten_materials()
    for c in [o for o in bpy.data.objects if o.type=='CAMERA']: pass
    export(D+'lillith_office_chairspin_v4.glb')
