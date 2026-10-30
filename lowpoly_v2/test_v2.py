# render rest views + poses
import bpy,math
sc=bpy.context.scene;sc.render.resolution_x=sc.render.resolution_y=700;root=bpy.data.objects['Lillith'];ao=bpy.data.objects['LillithRig']
out='/tmp/v2/'
def shot(n,a=0):
    root.rotation_euler=(0,0,math.radians(a));sc.render.filepath=out+n+'.png';bpy.ops.render.render(write_still=True)
ao.animation_data.action=None
for pb in ao.pose.bones: pb.rotation_quaternion=(1,0,0,0);pb.location=(0,0,0)
for n,a in [('front',0),('34',-45),('side',-90),('back',180),('34r',45)]: shot('rest_'+n,a)
for act,f in [('Wave',7),('Walk',7),('Walk',19),('Idle',19)]:
    ao.animation_data.action=bpy.data.actions[act];sc.frame_set(f);shot(f'{act}{f}',0);shot(f'{act}{f}_side',-90)
