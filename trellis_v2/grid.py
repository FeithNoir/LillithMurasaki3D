import sys;from PIL import Image,ImageDraw
for f in sys.argv[1:]:
    im=Image.open(f).convert('RGBA');b=Image.new('RGBA',im.size,(255,255,255,255));b.alpha_composite(im);d=ImageDraw.Draw(b)
    for k in range(-9,10):
        x=(k*0.1+0.9)/1.8*900;d.line([(x,0),(x,900)],fill=(255,0,0,90));d.text((x+2,2),'%.1f'%(k/10),fill='red')
    for k in range(0,18):
        y=900-(k*0.1+0.9-0.825)/1.8*900;d.line([(0,y),(900,y)],fill=(0,0,255,90));d.text((2,y-10),'%.1f'%(k/10),fill='blue')
    b.convert('RGB').save(f.replace('.png','_g.png'))
