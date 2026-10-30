import bpy,math,os
sc=bpy.context.scene;root=bpy.data.objects['Lillith'];ao=bpy.data.objects['LillithRig'];A=bpy.data.actions
L='/workspace/lillith-3d/trellis_v2/'
sc.render.resolution_x=sc.render.resolution_y=1000;ao.animation_data.action=None
for pb in ao.pose.bones: pb.rotation_quaternion=(1,0,0,0);pb.location=(0,0,0)
for n,a in [('front',0),('34',-45),('side',-90),('back',180)]:
    root.rotation_euler=(0,0,math.radians(a));sc.render.filepath=f'{L}render_{n}.png';bpy.ops.render.render(write_still=True)
sc.render.resolution_x=sc.render.resolution_y=720;sc.eevee.taa_render_samples=8
# turntable with idle
ao.animation_data.action=A['Idle'];os.makedirs('/tmp/ttT',exist_ok=True)
for f in range(1,145):
    sc.frame_set(f);root.rotation_euler=(0,0,2*math.pi*(f-1)/144);sc.render.filepath='/tmp/ttT/f_%04d.png'%f;bpy.ops.render.render(write_still=True)
root.rotation_euler=(0,0,math.radians(-30));os.makedirs('/tmp/pvT',exist_ok=True);k=1
for act,n in (('Idle',72),('Wave',48),('Walk',72)):
    ao.animation_data.action=A[act]
    for f in range(1,n+1):
        sc.frame_set(f);sc.render.filepath='/tmp/pvT/f_%04d.png'%k;k+=1;bpy.ops.render.render(write_still=True)
