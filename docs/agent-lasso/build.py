"""build.py — put the films' AI agent (Kenney platformer `character-oobi`, CC0) into the gnome-lasso scene in place
of the gnome, keeping its camera, door, button and timeline; render frames 1–74 + record the hand per frame.
Run: Blender -b ../gnome-lasso/gnome.blend -P build.py   (writes agent.blend, frames/a_NNN.png, frames/render.json)"""
import bpy, json, os
from bpy_extras.object_utils import world_to_camera_view as w2c
HERE = os.path.dirname(os.path.abspath(__file__))
GLB = os.path.join(HERE, 'character-oobi.glb')
S = bpy.context.scene; cam = S.objects['cam']; RX, RY = S.render.resolution_x, S.render.resolution_y
def px(p):
    v = w2c(S, cam, p); return [v.x * RX, (1 - v.y) * RY]

# the gnome's crop offset, so the button box gnome.json gives can be carried into this render's pixels
S.frame_set(1); gh = px(S.objects['hand'].matrix_world.translation)
G = json.load(open(os.path.join(HERE, '..', 'gnome-lasso', 'gnome.json')))
off = [gh[0] - G['hands'][0][0], gh[1] - G['hands'][0][1]]
button = {k: v + (off[0] if k in ('left', 'right') else off[1]) for k, v in G['button'].items()}

gnome = S.objects['character-male-b']; show = gnome.animation_data.action; slot = gnome.animation_data.action_slot
vis = S.objects['body-mesh'].animation_data.action
outline = bpy.data.materials['outline']; solid = S.objects['body-mesh'].modifiers['Solidify'] if 'Solidify' in S.objects['body-mesh'].modifiers else [m for m in S.objects['body-mesh'].modifiers if m.type == 'SOLIDIFY'][0]
thick = solid.thickness
hand = S.objects['hand']

before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=GLB)
new = [o for o in bpy.data.objects if o not in before]
arm = [o for o in new if o.type == 'ARMATURE'][0]; body = [o for o in new if o.type == 'MESH'][0]
for o in new:
    if o.animation_data: o.animation_data.action = None
    if o.animation_data:
        for t in list(o.animation_data.nla_tracks): o.animation_data.nla_tracks.remove(t)

# a little under the gnome-with-hat height (≈ 0.47), so the agent fits the door it walks out of; the agent is 0.907 tall
R = 0.40 / 0.907 / 0.6
cb = show.layers[0].strips[0].channelbags[0]
for f in cb.fcurves:
    if f.data_path == 'scale':
        for k in f.keyframe_points: k.co[1] *= R; k.handle_left[1] *= R; k.handle_right[1] *= R
arm.animation_data_create(); arm.animation_data.action = show; arm.animation_data.action_slot = slot
body.animation_data_create(); body.animation_data.action = vis
body.animation_data.action_slot = S.objects['body-mesh'].animation_data.action_slot
m = body.modifiers.new('Solidify', 'SOLIDIFY'); m.thickness = thick; m.use_flip_normals = True; m.material_offset = 1
body.data.materials.append(outline)
hand.parent = arm; hand.parent_type = 'BONE'; hand.parent_bone = 'arm-right'; hand.location = (0, 0, 0)

for n in ('character-male-b', 'body-mesh', 'head-mesh', 'hat'):
    bpy.data.objects.remove(S.objects[n], do_unlink=True)
bpy.ops.file.pack_all()

S.frame_start, S.frame_end = 1, 74
hands = []
os.makedirs(os.path.join(HERE, 'frames'), exist_ok=True)
for f in range(1, 75):
    S.frame_set(f); hands.append(px(hand.matrix_world.translation))
    S.render.filepath = os.path.join(HERE, 'frames', 'a_%03d.png' % f); bpy.ops.render.render(write_still=True)
json.dump({'res': [RX, RY], 'button': button, 'hands': hands}, open(os.path.join(HERE, 'frames', 'render.json'), 'w'))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, 'agent.blend'), compress=True)
print('DONE scale', R, 'button', button, 'hand1', hands[0])
