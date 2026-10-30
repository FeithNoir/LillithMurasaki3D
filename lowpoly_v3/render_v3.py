import bpy,math,os,sys
D='/workspace/lillith-3d/lowpoly_v3/';sc=bpy.context.scene;root=bpy.data.objects['Lillith'];ao=bpy.data.objects['LillithRig']
F=bpy.data.objects['Face'];KB=F.data.shape_keys.key_blocks
ao.animation_data.action=None
for pb in ao.pose.bones: pb.rotation_quaternion=(1,0,0,0);pb.location=(0,0,0)
sc.world.node_tree.nodes['Background'].inputs[1].default_value=0.6
cam=sc.camera;sc.eevee.taa_render_samples=16
def setk(n):
    for k in KB: k.value=1.0 if k.name==n else 0.0
mode=sys.argv[-1]
if mode in('stills','all'):
    sc.render.resolution_x=sc.render.resolution_y=1000
    for n,a in [('front',0),('34',35)]:
        setk('Basis');root.rotation_euler=(0,0,math.radians(a));sc.render.filepath=f'{D}render_{n}_v3.png';bpy.ops.render.render(write_still=True)
    root.rotation_euler=(0,0,0)
    cam.data.ortho_scale=0.30;cam.location=(0,-5,1.49)
    sc.render.resolution_x=sc.render.resolution_y=500
    for n in ['Basis','Smile','Happy','Angry','Sad','Surprised','Blink','Wink']:
        setk(n);sc.render.filepath=f'/tmp/v3face_{n}.png';bpy.ops.render.render(write_still=True)
if mode in('video','all'):
    cam.data.ortho_scale=0.42;cam.location=(0,-5,1.47);setk('Basis')
    sc.render.resolution_x=sc.render.resolution_y=720;sc.eevee.taa_render_samples=8
    t=F.data.shape_keys.animation_data.nla_tracks['Expressions'];t.mute=False
    os.makedirs('/tmp/v3vid',exist_ok=True)
    for f in range(1,169):
        sc.frame_set(f);sc.render.filepath='/tmp/v3vid/f_%04d.png'%f;bpy.ops.render.render(write_still=True)
