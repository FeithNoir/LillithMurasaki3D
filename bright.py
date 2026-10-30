import bpy,sys,math,mathutils
exec(open('/workspace/lillith-3d/render.py').read().split("sc=bpy.context.scene")[0])
for m in bpy.data.materials:
    nt=m.node_tree;p=[n for n in nt.nodes if n.type=='BSDF_PRINCIPLED']
    if not p: continue
    p=p[0];out=[n for n in nt.nodes if n.type=='OUTPUT_MATERIAL'][0]
    e=nt.nodes.new('ShaderNodeEmission');lk=p.inputs['Base Color'].links
    if lk: nt.links.new(lk[0].from_socket,e.inputs[0])
    else: e.inputs[0].default_value=p.inputs['Base Color'].default_value
    nt.links.new(e.outputs[0],out.inputs[0])
sc=bpy.context.scene;sc.render.engine='BLENDER_EEVEE_NEXT';sc.render.resolution_x=sc.render.resolution_y=1000;sc.view_settings.view_transform='Standard'
w=bpy.data.worlds.new('w');sc.world=w;w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(0.9,0.9,0.93,1)
cam=bpy.data.objects.new('c',bpy.data.cameras.new('c'));sc.collection.objects.link(cam);sc.camera=cam
cam.data.type='ORTHO';cam.data.ortho_scale=size*1.1;cam.location=ctr+mathutils.Vector((0,-size*3,0));cam.rotation_euler=(math.radians(90),0,0)
for name,a in [('front',0),('34',45),('side',90),('back',180)]:
  piv.matrix_world=mathutils.Matrix.Translation(ctr)@mathutils.Matrix.Rotation(math.radians(a),4,'Z')@mathutils.Matrix.Translation(-ctr)@base.to_matrix().to_4x4()
  sc.render.filepath=f'/workspace/lillith-3d/trellis/render_bright_{name}.png';bpy.ops.render.render(write_still=True)
