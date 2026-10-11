from PIL import Image, ImageDraw
import glob, json, os
clips=['idle','hover','press','release']
ims={c:[Image.open(f).convert('RGBA') for f in sorted(glob.glob(f'frames/{c}_*.png'))] for c in clips}
box=None
for c in clips:
    for im in ims[c]:
        b=im.getchannel('A').getbbox()
        box=b if box is None else (min(box[0],b[0]),min(box[1],b[1]),max(box[2],b[2]),max(box[3],b[3]))
pad=4; box=(max(0,box[0]-pad),max(0,box[1]-pad),min(360,box[2]+pad),min(360,box[3]+pad))
W,H=box[2]-box[0],box[3]-box[1]
COLS=12; total=sum(len(ims[c]) for c in clips); rows=-(-total//COLS)
sheet=Image.new('RGBA',(COLS*W,rows*H),(0,0,0,0)); meta={'cell':[W,H],'cols':COLS,'fps':24,'clips':{}}
i=0
for c in clips:
    meta['clips'][c]=[i,len(ims[c])]
    for im in ims[c]:
        sheet.paste(im.crop(box),((i%COLS)*W,(i//COLS)*H)); i+=1
# the press point: the lowest cyan pixel of the deepest press frame, in cell coordinates
deep=ims['press'][5].crop(box); px=deep.load(); best=None
for y in range(H):
    for x in range(W):
        r,g,b,a=px[x,y]
        if a>200 and b>180 and r<90: best=(x,y) if best is None or y>best[1] else best
meta['press_point']=best
rest=ims['idle'][0].crop(box); a=rest.getchannel('A'); bb=a.getbbox()
band=a.crop((0,bb[3]-14,W,bb[3])).getbbox()
meta['base']={'left':band[0],'right':band[2],'bottom':bb[3]}
sheet.save('arm-sheet.webp',quality=88,method=6)
json.dump(meta,open('arm-sheet.json','w'),indent=1)
print('base',meta['base'],'box',box,'cell',W,H,'press_point',best,'bytes',os.path.getsize('arm-sheet.webp'),meta['clips'])
rowsI=[]
for c in clips:
    sel=ims[c][::3]
    r=Image.new('RGB',(len(sel)*W//2+60,H//2+18),'white'); d=ImageDraw.Draw(r); d.text((4,4),c,fill='black')
    for j,im in enumerate(sel):
        t=im.crop(box).resize((W//2,H//2)); r.paste(t,(60+j*W//2,18),t)
    rowsI.append(r)
cw=max(r.width for r in rowsI); cs=Image.new('RGB',(cw,sum(r.height for r in rowsI)),'white'); y=0
for r in rowsI: cs.paste(r,(0,y)); y+=r.height
cs.save('contact.png')
