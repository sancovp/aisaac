from PIL import Image, ImageDraw
import glob, json, os
R=json.load(open('frames/render.json')); btn=R['button']
clips=['strike']
fr={c:sorted(f for f in glob.glob(f'frames/{c}_*.png')) for c in clips}
ims={c:[Image.open(f).convert('RGBA') for f in fr[c]] for c in clips}
bot=int(round(btn['bottom']))
box=None
for c in clips:
    for im in ims[c]:
        b=im.crop((0,0,im.width,bot)).getchannel('A').getbbox()
        if not b: continue
        box=b if box is None else (min(box[0],b[0]),min(box[1],b[1]),max(box[2],b[2]),max(box[3],b[3]))
x0=min(box[0], int(btn['left'])); x1=max(box[2], int(btn['right'])+1)
box=(max(0,x0-2), max(0,box[1]-2), min(280,x1+2), bot)
W,H=box[2]-box[0],box[3]-box[1]
COLS=12; total=sum(len(ims[c]) for c in clips); rows=-(-total//COLS)
back=Image.new('RGBA',(COLS*W,rows*H),(0,0,0,0)); front=Image.new('RGBA',(COLS*W,rows*H),(0,0,0,0))
meta={'cell':[W,H],'cols':COLS,'fps':24,'clips':{},'front':[], 'button':{'top':btn['top']-box[1],'bottom':btn['bottom']-box[1],'left':btn['left']-box[0],'right':btn['right']-box[0]}}
i=0
for c in clips:
    meta['clips'][c]=[i,len(ims[c])]
    for j,im in enumerate(ims[c]):
        back.paste(im.crop(box),((i%COLS)*W,(i//COLS)*H))
        fp=f'frames/front_{c}_{j:03d}.png'
        if os.path.exists(fp):
            front.paste(Image.open(fp).convert('RGBA').crop(box),((i%COLS)*W,(i//COLS)*H)); meta['front'].append(i)
        i+=1
back.save('pop-back.webp',quality=88,method=6); front.save('pop-front.webp',quality=88,method=6)
json.dump(meta,open('pop.json','w'),indent=1)
print(meta['cell'],meta['clips'],meta['button'],len(meta['front']),os.path.getsize('pop-back.webp'),os.path.getsize('pop-front.webp'))
