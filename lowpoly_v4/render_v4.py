import bpy,math,os,sys
D='/workspace/lillith-3d/lowpoly_v4/';sc=bpy.context.scene;root=bpy.data.objects['Lillith'];ao=bpy.data.objects['LillithRig']
F=bpy.data.objects['Face'];KB=F.data.shape_keys.key_blocks;KA=F.data.shape_keys.animation_data
sc.world.node_tree.nodes['Background'].inputs[1].default_value=0.6;cam=sc.camera;sc.eevee.taa_render_samples=16
def rest():
    ao.animation_data.action=None
    for pb in ao.pose.bones: pb.rotation_quaternion=(1,0,0,0);pb.location=(0,0,0)
def setk(n):
    for k in KB: k.value=1.0 if k.name==n else 0.0
mode=sys.argv[-1];rest()
if mode in('stills','all'):
    sc.render.resolution_x=sc.render.resolution_y=1000
    for n,a in [('front',0),('34',35),('side',90)]:
        setk('Basis');root.rotation_euler=(0,0,math.radians(a));sc.render.filepath=f'{D}render_{n}_v4.png';bpy.ops.render.render(write_still=True)
    root.rotation_euler=(0,0,0);cam.data.ortho_scale=0.30;cam.location=(0,-5,1.49);sc.render.resolution_x=sc.render.resolution_y=500
    for n in ['Basis','Smile','Happy','Wink','Angry','Sad','Surprised','Blink']:
        setk(n);sc.render.filepath=f'/tmp/v4face_{n}.png';bpy.ops.render.render(write_still=True)
if mode in('poses','all'):  # deformation check: one frame of each action, front + side
    cam.data.ortho_scale=1.95;cam.location=(0,-5,0.9);sc.render.resolution_x=sc.render.resolution_y=500;setk('Basis');sc.eevee.taa_render_samples=8
    for an,fr in [('Idle',19),('Wave',13),('Walk',7),('Walk',19),('TailSway',13),('Expressions',40),('Sit',1),('ChairSpin',70)]:
        ao.animation_data.action=bpy.data.actions[an];sc.frame_set(fr)
        for v,a in (('f',0),('s',90)):
            root.rotation_euler=(0,0,math.radians(a));sc.render.filepath=f'/tmp/v4pose_{an}{fr}_{v}.png';bpy.ops.render.render(write_still=True)
    root.rotation_euler=(0,0,0)
