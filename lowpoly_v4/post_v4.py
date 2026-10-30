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
# ---------------- v4: Sit pose + ChairSpin ----------------
SEAT_DROP=0.315  # hips 0.93 -> ~0.615 (office chair seat top 0.525 + thigh)
def hips_loc(delta):
    m=arm.bones['Hips'].matrix_local.to_3x3().inverted();P['Hips'].location=m@V(delta)
def sit_pose(t,sway=1.0,spin_v=0.0):
    hips_loc((0,0.03,-SEAT_DROP))
    for S,s in(('L',1),('R',-1)):
        P['UpperLeg.'+S].rotation_quaternion=wrot('UpperLeg.'+S,(1,0,0),-86)@wrot('UpperLeg.'+S,(0,1,0),-4*s)
        P['LowerLeg.'+S].rotation_quaternion=wrot('LowerLeg.'+S,(1,0,0),78)
        P['Foot.'+S].rotation_quaternion=wrot('Foot.'+S,(1,0,0),8)
        P['UpperArm.'+S].rotation_quaternion=wrot('UpperArm.'+S,(1,0,0),-32)@wrot('UpperArm.'+S,(0,1,0),16*s)
        P['LowerArm.'+S].rotation_quaternion=wrot('LowerArm.'+S,(1,0,0),-38)
    b=math.sin(2*math.pi*t)
    P['Spine'].rotation_quaternion=wrot('Spine',(1,0,0),-4)
    P['Chest'].rotation_quaternion=wrot('Chest',(1,0,0),-1.5*b*sway)
    P['Head'].rotation_quaternion=wrot('Head',(0,1,0),4*math.sin(2*math.pi*t+1)*sway)
    # tail out to her left side (avoids the chair back), lags behind the spin
    for i in range(5):
        base=(wrot('Tail.0',(0,0,1),75)@wrot('Tail.0',(1,0,0),-25)) if i==0 else Q()
        P['Tail.%d'%i].rotation_quaternion=wrot('Tail.%d'%i,(0,0,1),8*sway*math.sin(2*math.pi*t-i*0.6)-spin_v*(6+3*i))@base
    for i in range(3):
        P['HairBack.%d'%i].rotation_quaternion=wrot('HairBack.%d'%i,(0,0,1),-spin_v*(4+3*i))@wrot('HairBack.%d'%i,(1,0,0),-spin_v*2)
    for S,s in(('L',1),('R',-1)):
        P['SideLock.'+S].rotation_quaternion=wrot('SideLock.'+S,(0,0,1),-spin_v*5)
        P['Ear.'+S].rotation_quaternion=wrot('Ear.'+S,(0,1,0),-spin_v*4*s)
make_action('Sit',48,lambda t:sit_pose(t,0.6))
SPIN_LEN=168;TURNS=2
def spin_angle(f):  # frames 1..169: settle 24f, spin 2 turns with ease in/out (120f), settle
    u=min(1,max(0,(f-25)/120));e=u*u*(3-2*u);return 360*TURNS*e
def spin_vel(f): return (spin_angle(f+1)-spin_angle(f-1))/2/9.0  # ~1.0 at peak
act=bpy.data.actions.new('ChairSpin');act.use_fake_user=True;ao.animation_data.action=act;prev={}
for f in range(1,SPIN_LEN+2):
    for pb in ao.pose.bones: pb.rotation_quaternion=(1,0,0,0);pb.location=(0,0,0)
    sit_pose((f-1)/48,0.5,spin_vel(f))
    P['Root'].rotation_quaternion=wrot('Root',(0,0,1),spin_angle(f))
    for pb in ao.pose.bones:
        q=pb.rotation_quaternion.copy()
        if pb.name in prev and prev[pb.name].dot(q)<0: q.negate()
        pb.rotation_quaternion=q;prev[pb.name]=q.copy()
        pb.keyframe_insert('rotation_quaternion',frame=f)
        if pb.name in('Root','Hips'): pb.keyframe_insert('location',frame=f)
for fc in act.fcurves:
    for kp in fc.keyframe_points: kp.interpolation='LINEAR'
tr=ao.animation_data.nla_tracks.new();tr.name='ChairSpin';tr.strips.new('ChairSpin',1,act);tr.mute=True;ao.animation_data.action=None
sk_action('Sit',{'Smile':[(1,0.4),(49,0.4)],'Blink':[(1,0),(20,0),(22,1),(24,0),(49,0)]},48)
sk_action('ChairSpin',{'Happy':[(1,0),(30,0),(40,1),(120,1),(132,0),(169,0)],'Wink':[(1,0),(132,0),(140,1),(160,1),(168,0),(169,0)],
  'Smile':[(1,0.5),(30,0.5),(40,0),(132,0),(140,0.6),(169,0.5)]},SPIN_LEN)
