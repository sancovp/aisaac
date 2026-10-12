"""build_pop.py — THE POP: the agent comes out of the door, hops three times at the spot, and goes back in. Same scene, camera
and door as the lasso (agent.blend), so the button box is the same; frames 1–19 and 48–74 are the lasso's own (out · nod ·
home); the work between them is three hops on the agent's own `jump` clip, lifted on an arc, with the door held open. At the
size it plays in the app its limbs move a few pixels, so the beat is carried by the whole body. Run: Blender -b agent.blend -P build_pop.py   (writes frames/p_NNN.png; then python3 pack_pop.py)"""
import bpy, os
HERE = os.path.dirname(os.path.abspath(__file__))
S = bpy.context.scene
arm = [o for o in S.objects if o.type == 'ARMATURE'][0]
body = [o for o in S.objects if o.type == 'MESH' and o.parent == arm][0]
hinge = S.objects['hinge']
show, show_slot = arm.animation_data.action, arm.animation_data.action_slot
vis, vis_slot = body.animation_data.action, body.animation_data.action_slot
hact, hslot = hinge.animation_data.action, hinge.animation_data.action_slot

# the agent's own clip, from its model (the scene keeps only the actions it uses)
before_o, before_a = set(bpy.data.objects), set(bpy.data.actions)
bpy.ops.import_scene.gltf(filepath=os.path.join(HERE, 'character-oobi.glb'))
clip = lambda name: [a for a in bpy.data.actions if a not in before_a and a.name.startswith(name)][0]
hop = clip('jump')
for a in (hop,):
    a.use_fake_user = True
    # the clips hold the root and torso level, which turns the visor away from this camera: drop their keys, so the body
    # keeps the pose it lands in (tipped back, facing us) and the clip moves only the legs and arms
    for bag in a.layers[0].strips[0].channelbags:
        for fc in [f for f in bag.fcurves if f.data_path.startswith(('pose.bones["root"]', 'pose.bones["torso"]'))]: bag.fcurves.remove(fc)
for o in [o for o in bpy.data.objects if o not in before_o]: bpy.data.objects.remove(o, do_unlink=True)

S.frame_set(20)   # where it stands once it has hopped down — the work happens here
place = (arm.location.copy(), arm.rotation_euler.copy(), arm.scale.copy())
held = {b: (arm.pose.bones[b].location.copy(), arm.pose.bones[b].rotation_quaternion.copy(), arm.pose.bones[b].rotation_euler.copy(), arm.pose.bones[b].scale.copy()) for b in ('root', 'torso')}

def lasso_frame(g):
    arm.animation_data.action = show; arm.animation_data.action_slot = show_slot
    body.animation_data.action = vis; body.animation_data.action_slot = vis_slot
    hinge.animation_data.action = hact; hinge.animation_data.action_slot = hslot
    S.frame_set(g)

def work_frame(act, t, lift):
    arm.animation_data.action = act
    if act.slots: arm.animation_data.action_slot = act.slots[0]
    body.animation_data.action = None; body.hide_render = False
    hinge.animation_data.action = None; hinge.rotation_euler = (0, 0, 1.833)
    arm.location, arm.rotation_euler, arm.scale = place[0].copy(), place[1].copy(), place[2].copy()
    arm.location.z += lift
    for b, pose in held.items():
        pb = arm.pose.bones[b]; pb.location, pb.rotation_quaternion, pb.rotation_euler, pb.scale = (v.copy() for v in pose)
    S.frame_set(t)

import math
HOP = 10        # frames per hop
seq = [('l', g) for g in range(1, 20)]
seq += [('w', hop, round(12 * u / HOP), 0.3 * math.sin(math.pi * u / HOP)) for _ in range(3) for u in range(HOP)]   # three hops
seq += [('l', g) for g in range(48, 75)]
os.makedirs(os.path.join(HERE, 'frames'), exist_ok=True)
for i, item in enumerate(seq, 1):
    lasso_frame(item[1]) if item[0] == 'l' else work_frame(*item[1:])
    S.render.filepath = os.path.join(HERE, 'frames', 'p_%03d.png' % i)
    bpy.ops.render.render(write_still=True)
print('DONE pop frames', len(seq))
