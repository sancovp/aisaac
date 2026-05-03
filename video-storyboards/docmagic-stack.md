# Video Storyboard: DocMagic Stack
Source: blog/docmagic-stack.html
Diagram: blog/diagrams/docmagic-stack.png
Estimated length: 4min

## Scene 1: INTRO (0:00 - 0:15)
**Visual:** Isaac talking head (pre-recorded intro clip)
**Audio:** "I'm too lazy to make 400 pieces of content per week myself so I have AI crystallize them. You can do that too if you learn how on my channel. Here's GNOSYS on why AI-coded repos drift and what to do about it..."
**Text overlay:** DocMagic — Where It Sits in the Stack

## Scene 2: The Invisible Coupling Problem (0:15 - 1:15)
**Visual:** [AVATAR: GNOSYS, diagnosing] → [CUT TO: Excalidraw diagram]
**Voiceover:** "AI agents cannot safely edit what they cannot see. A repo isn't just files — it's overlapping execution surfaces. Source code, tests, docs, hooks, workflows, runtime side effects, state files. Human developers know these relationships implicitly. AI agents usually don't. They search, read a few visible files, infer a local story, and edit code as if the hidden causal system doesn't exist. That's how AI-coded repos drift. DocMagic scans for seven categories of invisible coupling: HTTP calls, file triggers, hook bridges, MCP references, cross-imports, state files, and multi-write drift. Every hidden connection gets a local, searchable, agent-readable breadcrumb."
**Remotion animation:** A code file with invisible red threads connecting to other files — hidden callers, state watchers, hook chains — all invisible until DocMagic "illuminates" them one by one
**AI-IMAGE prompt:** A code file with invisible connections illuminated - red lines showing hidden callers, blue lines showing state file watchers, green breadcrumb markers at each danger point, dark IDE aesthetic

## Scene 3: Three Roles (1:15 - 2:45)
**Visual:** [AVATAR: GNOSYS, hands-on] → [REMOTION-ANIMATION: three-role diagram]
**Voiceover:** "DocMagic fills three roles in the engineering stack simultaneously. Role 1 — Admissibility Engineering tool. Before the agent touches any file, DocMagic tells it: this file has three hidden callers you haven't read. This function writes to a state file watched by two daemons. Without DocMagic, the agent edits locally and hopes. With it, the agent knows its edit boundary before it starts. Role 2 — Concentration Engineering surface. The annotations keep the agent aware of nonlocal behavior at the EXACT point where it matters — in the source file, at the function definition, right where the cursor is. It's context injection AND attention anchoring simultaneously. Role 3 — Emergence Engineering repair loop. Every time DocMagic runs, it detects new hidden edges and patches the explanatory surfaces. The repo improves its own admissibility over time. Each scan makes the next edit safer."
**Remotion animation:** Three panels showing the same code file through three lenses — admissibility gates blocking unsafe edits, attention anchors highlighting context, and a repair loop where annotations grow denser over time
**AI-IMAGE prompt:** A repository shown as a living organism with glowing neural pathways connecting files, with DocMagic annotations appearing as bioluminescent markers at each hidden connection point

## Scene 4: Outro (2:45 - 4:00)
**Visual:** [AVATAR: GNOSYS]
**Voiceover:** "The hypebeast complaint is that AI coding agents make messy, brittle code. The technical answer: of course they do. The agent's visible context diverges from the repo's actual execution geometry. Repair the geometry, and the agent can act inside a better self-model. That's what DocMagic does — makes the invisible visible so agents can act safely. Open source, pip installable. Full post below."
**Text overlay:** aisaac.xyz/blog/docmagic-stack | Book a Call: cal.com/aisaac
