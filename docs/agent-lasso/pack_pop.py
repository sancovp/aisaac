"""pack_pop.py — frames/p_*.png → agent-pop.webp + agent-pop.json (the button box from the lasso's render: same camera)."""
from PIL import Image
import glob, json, os
R = json.load(open('frames/render.json'))
files = sorted(glob.glob('frames/p_*.png')); ims = [Image.open(f).convert('RGBA') for f in files]
box = None
for im in ims:
    b = im.getchannel('A').getbbox()
    if b: box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
box = (max(0, box[0] - 3), max(0, box[1] - 3), min(R['res'][0], box[2] + 3), min(R['res'][1], box[3] + 3))
W, H = box[2] - box[0], box[3] - box[1]; COLS = 10; rows = -(-len(ims) // COLS)
sheet = Image.new('RGBA', (COLS * W, rows * H), (0, 0, 0, 0))
for i, im in enumerate(ims): sheet.paste(im.crop(box), ((i % COLS) * W, (i // COLS) * H))
sheet.save('agent-pop.webp', quality=88, method=6)
b = R['button']
meta = {'cell': [W, H], 'cols': COLS, 'fps': 24, 'frames': len(ims),
        'button': {k: (v - box[0] if k in ('left', 'right') else v - box[1]) for k, v in b.items()},
        'beats': {'out': [0, 19], 'work': [19, 49], 'home': [49, len(ims)]}}
json.dump(meta, open('agent-pop.json', 'w'))
print(W, H, meta['button'], len(ims), os.path.getsize('agent-pop.webp'))
