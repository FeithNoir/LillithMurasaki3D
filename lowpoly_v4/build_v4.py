# Lillith low-poly v4 = v2 source + v3 face/bangs + v4 body/clip/sit. blender -b -P build_v4.py
D='/workspace/lillith-3d/lowpoly_v4/'
src=open('/workspace/lillith-3d/lowpoly/build_v2.py').read()
def R(a,b):
    global src
    assert a in src,a;src=src.replace(a,b)
a=src.index("for side,vis in ((1,True),(-1,False)):");b=src.index("# hair")
src=src[:a]+"exec(open(D+'face_v4.py').read())\n"+src[b:]
# v3: mirrored + shorter bangs
R("tube('BangBig',[(0.01,-0.10,1.62),(-0.03,-0.115,1.55),(-0.05,-0.115,1.47),(-0.07,-0.10,1.41)]","tube('BangBig',[(-0.01,-0.10,1.62),(0.03,-0.115,1.55),(0.05,-0.115,1.47),(0.07,-0.10,1.41)]")
R("for x,z in ((0.04,1.53),(0.075,1.52),(0.01,1.545)):","for x,z in ((-0.04,1.548),(-0.075,1.54),(-0.01,1.555)):")
R("('Head','Eye','Iris'","('Head','Face','Pin','Eye','Iris'")
# v4 palette (closer to sprite: darker charcoal suit, near-black skirt)
R("JACK=toon('Jacket','#504944','#292c38')","JACK=toon('Jacket','#45444b','#2a2a33');SILVER=toon('Silver','#b4bccb','#7d8597')")
R("SKIRT=toon('Skirt','#3a3d45','#1f2024')","SKIRT=toon('Skirt','#2e2f36','#1a1b1f')")
# v4 skull clip: on top of the bangs over the covered eye (as in LM_Suit_V1), bigger; + 2 silver pins on the other side
R("ell('Clip',(0.075,-0.09,1.60),(0.02,0.01,0.018),ORG,8,6,0.003)","ell('Clip',(0.058,-0.117,1.598),(0.027,0.011,0.022),ORG,8,6,0.004)")
R("for dx in (-0.007,0.007): disc('ClipEye',(0.075+dx,-0.101,1.602),(0.004,0.004),DARK,(0,-1,0),6)",
  "for dx in (-0.009,0.009): disc('ClipEye',(0.058+dx,-0.1295,1.602),(0.006,0.0055),DARK,(0,-1,0),6)\n"
  "for i in range(2): disc('Pin%d'%i,(-0.05-0.006*i,-0.127,1.596-0.016*i),(0.016,0.0035),SILVER,(-0.3,-1,0.15),4,rot=0.45)")
# v4 body: bust + narrower waist (jacket), wider hips (skirt), thicker thighs
R("tube('Jacket',[(0,0.0,0.97),(0,0.0,1.06),(0,0.0,1.20),(0,0.0,1.30),(0,0.005,1.36)],[(0.15,0.10),(0.13,0.085),(0.155,0.10),(0.165,0.09),(0.06,0.05)],JACK,12)",
  "tube('Jacket',[(0,0.0,0.97),(0,0.0,1.06),(0,-0.008,1.14),(0,-0.016,1.21),(0,-0.004,1.29),(0,0.005,1.36)],[(0.172,0.11),(0.122,0.085),(0.148,0.108),(0.158,0.122),(0.166,0.095),(0.06,0.05)],JACK,14)")
R("vs=[bm.verts.new(v) for v in ((-0.05,-0.093,1.34),(0.05,-0.093,1.34),(0,-0.104,1.14))]","vs=[bm.verts.new(v) for v in ((-0.05,-0.103,1.345),(0.05,-0.103,1.345),(0,-0.141,1.215))]")
R("tube('Lanyard',[(-0.045,-0.03,1.37),(-0.03,-0.097,1.30),(0.0,-0.112,1.17),(0.03,-0.097,1.30),(0.045,-0.03,1.37)],[0.004]*5","tube('Lanyard',[(-0.045,-0.03,1.37),(-0.035,-0.112,1.30),(-0.012,-0.146,1.21),(0.0,-0.142,1.15),(0.012,-0.146,1.21),(0.035,-0.112,1.30),(0.045,-0.03,1.37)],[0.004]*7")
R("v.co=V((v.co.x*0.045,v.co.y*0.005-0.115,v.co.z*0.06+1.13))","v.co=V((v.co.x*0.045,v.co.y*0.005-0.142,v.co.z*0.06+1.115))")
R("disc('BadgeStripe',(0,-0.1185,1.15)","disc('BadgeStripe',(0,-0.1455,1.135)")
R("tube('Skirt',[(0,0,1.0),(0,0,0.90),(0,0,0.78)],[(0.16,0.11),(0.185,0.125),(0.20,0.135)],SKIRT,16)",
  "tube('Skirt',[(0,0.0,1.0),(0,0.005,0.92),(0,0.005,0.85),(0,0.005,0.77)],[(0.168,0.115),(0.212,0.14),(0.218,0.142),(0.206,0.135)],SKIRT,16)")
R("tube('Leg'+str(s),[(0.075*s,0,0.95),(0.08*s,0,0.78),(0.088*s,-0.005,0.55),(0.093*s,0.0,0.43),(0.10*s,0.005,0.15),(X,0.01,0.10)],[0.085,0.08,0.05,0.056,0.03,0.03],TIGHT,12,k=2)",
  "tube('Leg'+str(s),[(0.082*s,0,0.95),(0.097*s,0,0.80),(0.095*s,-0.004,0.66),(0.09*s,-0.005,0.55),(0.093*s,0.0,0.43),(0.10*s,0.005,0.15),(X,0.01,0.10)],[0.09,0.093,0.075,0.054,0.057,0.03,0.03],TIGHT,12,k=2)")

R("tube('HairBack',[(0,0.05,1.58),(0,0.075,1.45),(0,0.085,1.25),(0,0.075,1.05),(0,0.06,0.92)],[(0.125,0.08),(0.15,0.07),(0.15,0.055),(0.13,0.04),(0.07,0.02)],HAIR,14,k=2)",
  "HAIRH=toon('HairHi','#b385c8','#8e5fa6')\n"
  "tube('HairBack',[(0,0.045,1.60),(0,0.08,1.45),(0,0.105,1.26),(0,0.11,1.10),(0,0.10,1.00)],[(0.13,0.085),(0.18,0.08),(0.21,0.07),(0.19,0.05),(0.09,0.02)],HAIR,14,k=2)\n"
  "exec(open(D+'hair_v4.py').read())")
R("for k in ('Head','Face','Pin'","for k in ('Head','Face','Pin','HairTop'")
R("    if n=='HairBack': return","    if n.startswith('Strand'): return ['Head','HairBack.0','HairBack.1','HairBack.2','SideLock.L','SideLock.R']\n    if n=='HairBack': return")
# hips/thigh bones follow the wider stance
R("B('UpperLeg.'+S,(0.08*s,0,0.93)","B('UpperLeg.'+S,(0.09*s,0,0.93)")
# hooks: post (actions) before tri count; stop after .blend save (GLB done Sketchfab-safe below)
R("tris=sum(","exec(open(D+'post_v4.py').read())\ntris=sum(")
R("/workspace/lillith-3d/lowpoly/lillith_lowpoly_v2",D+"lillith_lowpoly_v4")
src=src[:src.index("\n",src.index("bpy.ops.wm.save_as_mainfile"))]
exec(compile(src,'build_v2_patched_v4','exec'))
# ---- Sketchfab-safe GLB (character alone)
exec(open(D+'sfsafe.py').read())
face_single_material(bpy.data.objects['Face'],D+'face_palette_v4.png')
skinned_to_root();flatten_materials()
export(D+'lillith_lowpoly_v4.glb')
