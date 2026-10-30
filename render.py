import bpy,sys,math,mathutils
glb,out=sys.argv[-2],sys.argv[-1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
ms=[o for o in bpy.context.scene.objects if o.type=='MESH']
print('TRIS',sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in ms))
def bb():
  bpy.context.view_layer.update()
  pts=[o.matrix_world@mathutils.Vector(c) for o in ms for c in o.bound_box]
  return mathutils.Vector([min(p[i] for p in pts) for i in range(3)]),mathutils.Vector([max(p[i] for p in pts) for i in range(3)])
piv=bpy.data.objects.new('piv',None);bpy.context.scene.collection.objects.link(piv)
for o in bpy.context.scene.objects:
  if o.parent is None and o!=piv: o.parent=piv
mn,mx=bb(); e=mx-mn
base=mathutils.Euler((math.radians(90),0,0)) if e[1]>e[2] else mathutils.Euler((0,0,0))
piv.rotation_euler=base; mn,mx=bb(); ctr=(mn+mx)/2; size=max(mx-mn)
sc=bpy.context.scene; sc.render.engine='BLENDER_EEVEE_NEXT'; sc.render.resolution_x=sc.render.resolution_y=800
w=bpy.data.worlds.new('w');sc.world=w;w.use_nodes=True;w.node_tree.nodes['Background'].inputs[1].default_value=3.0
cam=bpy.data.objects.new('c',bpy.data.cameras.new('c'));sc.collection.objects.link(cam);sc.camera=cam
cam.data.type='ORTHO';cam.data.ortho_scale=size*1.1
cam.location=ctr+mathutils.Vector((0,-size*3,0));cam.rotation_euler=(math.radians(90),0,0)
for name,a in [('front',0),('34',45),('side',90),('back',180)]:
  piv.rotation_euler=base; piv.rotation_euler.z=math.radians(-a) if False else 0
  piv.matrix_world=mathutils.Matrix.Translation(ctr)@mathutils.Matrix.Rotation(math.radians(a),4,'Z')@mathutils.Matrix.Translation(-ctr)@base.to_matrix().to_4x4()
  sc.render.filepath=f'{out}_{name}.png';bpy.ops.render.render(write_still=True)
