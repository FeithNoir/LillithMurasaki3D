# shape-key animations: blink in Idle, Expressions cycle; NLA tracks named like the armature ones so glTF merges them
K=FACE.data.shape_keys;K.name='FaceKeys'
def sk_action(name,keys,length):
    act=bpy.data.actions.new(name+'_Face');act.use_fake_user=True;K.animation_data_create()
    for n,pts in keys.items():
        fc=act.fcurves.new(f'key_blocks["{n}"].value')
        for f,v in pts: fc.keyframe_points.insert(f,v).interpolation='BEZIER'
    tr=K.animation_data.nla_tracks.new();tr.name=name;tr.strips.new(name,1,act);tr.mute=True
    return act
sk_action('Idle',{'Blink':[(1,0),(30,0),(32,1),(34,0),(62,0),(64,1),(66,0),(73,0)]},72)
seq=['Smile','Happy','Wink','Angry','Sad','Surprised','Blink'];L=24;keys={n:[] for n in seq}
for i,n in enumerate(seq):
    s=1+i*L
    for m in seq: keys[m]+= [(s,0.0),(s+6,1.0 if m==n else 0.0),(s+18,1.0 if m==n else 0.0),(s+L-1,0.0)]
sk_action('Expressions',keys,L*len(seq))
# armature placeholder track so 'Expressions' plays with a gentle idle body
make_action('Expressions',L*len(seq),lambda t:(armsdown(),tail(t,8,3)))
for kb in K.key_blocks: kb.value=0
