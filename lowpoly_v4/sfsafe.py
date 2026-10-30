# Sketchfab-safe conversion (same recipe as lowpoly_v3/build_sketchfab.py), applied in-memory before glTF export
import bpy
def _hx(h):
    h=h.lstrip('#');c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return [((x+0.055)/1.055)**2.4 if x>0.04045 else x/12.92 for x in c]+[1]
def face_single_material(F,palette_path):
    me=F.data;mats=list(me.materials);N=4;CS=4;S=N*CS
    img=bpy.data.images.new('FacePalette',S,S,alpha=False);px=[0.0]*(S*S*4)
    for i,m in enumerate(mats):
        c=[int(m['base'].lstrip('#')[k:k+2],16)/255 for k in (0,2,4)];cx,cy=i%N,i//N
        for y in range(cy*CS,cy*CS+CS):
            for x in range(cx*CS,cx*CS+CS): px[(y*S+x)*4:(y*S+x)*4+4]=c+[1]
    img.pixels=px;img.filepath_raw=palette_path;img.file_format='PNG';img.save();img.pack()
    uv=me.uv_layers.new(name='UVMap')
    for p in me.polygons:
        u,v=(p.material_index%N+0.5)/N,(p.material_index//N+0.5)/N
        for li in p.loop_indices: uv.data[li].uv=(u,v)
    m=bpy.data.materials.new('FacePalette');m.use_nodes=True;m['base']='#ffffff';m['tex']=img.name
    me.materials.clear();me.materials.append(m)
    for p in me.polygons: p.material_index=0
def flatten_materials():
    for o in bpy.data.objects:
        for md in list(o.modifiers):
            if md.type=='SOLIDIFY': o.modifiers.remove(md)
        if o.type=='MESH' and len(o.data.materials)>1:
            used={p.material_index for p in o.data.polygons}
            while len(o.data.materials)>1 and len(o.data.materials)-1 not in used: o.data.materials.pop(index=len(o.data.materials)-1)
    for mt in bpy.data.materials:
        if 'base' not in mt: continue
        nt=mt.node_tree;Nn=nt.nodes
        for n in list(Nn): Nn.remove(n)
        p=Nn.new('ShaderNodeBsdfPrincipled');p.inputs['Roughness'].default_value=0.9
        if mt.get('tex'):
            t=Nn.new('ShaderNodeTexImage');t.image=bpy.data.images[mt['tex']];t.interpolation='Closest';nt.links.new(t.outputs[0],p.inputs['Base Color'])
        else: p.inputs['Base Color'].default_value=_hx(mt['base'])
        nt.links.new(p.outputs[0],Nn.new('ShaderNodeOutputMaterial').inputs[0])
def skinned_to_root():
    for o in bpy.data.objects:
        if o.type=='MESH' and any(m.type=='ARMATURE' for m in o.modifiers) and o.parent:
            mw=o.matrix_world.copy();o.parent=None;o.matrix_world=mw
def export(path):
    for o in bpy.data.objects:
        if o.type=='MESH' and o.data.shape_keys:
            for kb in o.data.shape_keys.key_blocks: kb.value=0
    bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',export_apply=False,export_animation_mode='NLA_TRACKS',
        export_morph=True,export_morph_animation=True,export_try_sparse_sk=False,export_morph_normal=False,
        export_cameras=False,export_lights=False)
