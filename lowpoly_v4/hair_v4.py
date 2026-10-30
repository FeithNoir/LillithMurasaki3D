# v4 hair: long flowing, layered spiky strands flaring at shoulder/elbow height + top volume (exec'd in build namespace)
def strand(name,pts,w,th=0.022,mat=None):
    tube(name,pts,[(w,th),(w*0.85,th*0.85),(w*0.45,th*0.6),(0.0,0.0)][:len(pts)-1]+[(0.0,0.0)],mat or HAIR,6,(True,False),0.008,k=2)
for s in (1,-1):
    S='L' if s>0 else 'R'
    # back layer, flaring out to the sides (behind the arms)
    strand('StrandShoulder'+S,[(0.07*s,0.07,1.53),(0.18*s,0.12,1.40),(0.27*s,0.15,1.30),(0.33*s,0.16,1.22)],0.05)
    strand('StrandElbow'+S,[(0.06*s,0.09,1.46),(0.19*s,0.15,1.26),(0.30*s,0.17,1.12),(0.36*s,0.17,1.04)],0.055,mat=HAIRH)
    strand('StrandLow'+S,[(0.05*s,0.10,1.38),(0.15*s,0.16,1.16),(0.24*s,0.17,1.02),(0.28*s,0.16,0.95)],0.05)
    strand('StrandInner'+S,[(0.03*s,0.11,1.30),(0.09*s,0.16,1.12),(0.13*s,0.16,1.00),(0.15*s,0.15,0.93)],0.045,mat=HAIRH)
    strand('StrandMid'+S,[(0.08*s,0.05,1.50),(0.17*s,0.10,1.32),(0.22*s,0.13,1.16),(0.23*s,0.14,1.08)],0.04)
    # over the shoulder (above the jacket shoulder)
    strand('StrandTop'+S,[(0.10*s,0.01,1.56),(0.17*s,0.04,1.45),(0.24*s,0.07,1.37),(0.29*s,0.08,1.33)],0.035,0.018,mat=HAIRH)
    # a spike off the side of the head
    strand('StrandSide'+S,[(0.11*s,0.03,1.60),(0.17*s,0.04,1.57),(0.22*s,0.05,1.55)],0.03,0.016)
# long centre-back strands
strand('StrandBackC',[(0.0,0.10,1.32),(0.02,0.13,1.12),(0.03,0.125,1.0),(0.04,0.12,0.94)],0.06)
strand('StrandBackL',[(0.05,0.10,1.25),(0.08,0.135,1.08),(0.09,0.13,0.98)],0.04,mat=HAIRH)
# volume on top between the ears
tube('HairTop0',[(0.0,-0.01,1.615),(0.012,-0.02,1.672),(0.03,-0.03,1.705)],[(0.04,0.03),(0.022,0.016),(0.0,0.0)],HAIR,6,(True,False),0.008)
tube('HairTop1',[(-0.025,0.02,1.62),(-0.035,0.015,1.67),(-0.05,0.01,1.695)],[(0.035,0.03),(0.018,0.014),(0.0,0.0)],HAIR,6,(True,False),0.008)
tube('HairTop2',[(0.03,0.04,1.62),(0.035,0.05,1.665),(0.045,0.06,1.69)],[(0.03,0.025),(0.016,0.012),(0.0,0.0)],HAIRH,6,(True,False),0.008)
# extra bang layer over the covered eye (+x) and a short one by the visible eye
tube('BangSweep',[(-0.03,-0.10,1.63),(0.02,-0.12,1.58),(0.06,-0.12,1.50),(0.085,-0.105,1.44)],[(0.03,0.01),(0.035,0.012),(0.025,0.01),(0.0,0.0)],HAIRH,6,(True,False))
tube('BangShort',[(-0.055,-0.10,1.62),(-0.075,-0.105,1.565)],[(0.02,0.008),(0.0,0.0)],HAIR,6,(True,False))
