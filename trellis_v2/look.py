import bpy,math,sys
blend,out=sys.argv[-2],sys.argv[-1]
sc=bpy.context.scene
for m in bpy.data.materials:
    if not m.use_nodes: continue
    nt=m.node_tree;p=[n for n in nt.nodes if n.type=='BSDF_PRINCIPLED']
    if p:
        p=p[0];o=[n for n in nt.nodes if n.type=='OUTPUT_MATERIAL'][0];e=nt.nodes.new('ShaderNodeEmission');l=p.inputs['Base Color'].links
        if l: nt.links.new(l[0].from_socket,e.inputs[0])
        nt.links.new(e.outputs[0],o.inputs[0])
sc.render.engine='BLENDER_EEVEE_NEXT';sc.render.resolution_x=sc.render.resolution_y=900;sc.view_settings.view_transform='Standard';sc.render.film_transparent=True
cam=bpy.data.objects.new('lc',bpy.data.cameras.new('lc'));sc.collection.objects.link(cam);sc.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=1.8
for n,loc,rot in [('front',(0,-5,0.825),(90,0,0)),('side',(5,0,0.825),(90,0,90)),('back',(0,5,0.825),(90,0,180))]:
    cam.location=loc;cam.rotation_euler=[math.radians(a) for a in rot];sc.render.filepath=f'{out}_{n}.png';bpy.ops.render.render(write_still=True)
