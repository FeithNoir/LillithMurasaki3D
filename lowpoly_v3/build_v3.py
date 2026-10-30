# Lillith low-poly v3: v2 + expression face with shape keys. Run: blender -b -P build_v3.py
# Reads ../lowpoly/build_v2.py (unmodified) and patches it in memory.
import os
D='/workspace/lillith-3d/lowpoly_v3/'
src=open('/workspace/lillith-3d/lowpoly/build_v2.py').read()
a=src.index("for side,vis in ((1,True),(-1,False)):");b=src.index("# hair")
src=src[:a]+"exec(open(D+'face_v3.py').read())\n"+src[b:]
src=src.replace("for x,z in ((0.04,1.53),(0.075,1.52),(0.01,1.545)):","for x,z in ((0.04,1.548),(0.075,1.54),(0.01,1.555)):")  # shorter bangs so brows read
src=src.replace("('Head','Eye','Iris'","('Head','Face','Eye','Iris'")
src=src.replace("tris=sum(","exec(open(D+'post_v3.py').read())\ntris=sum(",1)
src=src.replace("/workspace/lillith-3d/lowpoly/lillith_lowpoly_v2",D+"lillith_lowpoly_v3")
src=src.replace("export_animation_mode='ACTIONS'","export_animation_mode='NLA_TRACKS',export_morph=True,export_morph_animation=True")
# mirror bangs: hidden eye on her left (+x, clip side), visible eye on her right (-x), as in LM_Suit_V1
src=src.replace("tube('BangBig',[(0.01,-0.10,1.62),(-0.03,-0.115,1.55),(-0.05,-0.115,1.47),(-0.07,-0.10,1.41)]","tube('BangBig',[(-0.01,-0.10,1.62),(0.03,-0.115,1.55),(0.05,-0.115,1.47),(0.07,-0.10,1.41)]")
src=src.replace("for x,z in ((0.04,1.548),(0.075,1.54),(0.01,1.555)):","for x,z in ((-0.04,1.548),(-0.075,1.54),(-0.01,1.555)):")
assert "(0.07,-0.10,1.41)" in src and "(-0.075,1.54)" in src
exec(compile(src,'build_v2_patched','exec'))
