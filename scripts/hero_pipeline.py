"""Plumber hero pipeline: generate reference image + Veo 3.1 video loop."""
import os, time
from google import genai
from google.genai import types
from PIL import Image as PILImage
from io import BytesIO

# SECURITY (2026-07-06): the hardcoded key that lived here was committed to this
# PUBLIC repo (5740fafe) and must be treated as BURNED — rotate it in the Google
# console. The script now requires the key from the environment, never inline.
assert os.environ.get('GOOGLE_API_KEY'), 'set GOOGLE_API_KEY in the environment'
client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

ref_prompt = """Photorealistic cinematic photograph of a master plumber in a clean blue work shirt standing in front of his white service van in a bright suburban driveway in Acworth, Georgia at golden hour. He holds a chrome pipe wrench casually at his side and smiles confidently. The house behind has warm window light. The driveway is clean concrete. The scene is well-lit, NOT dark, NOT moody - the lighting should feel like a successful local business owner at the end of a good day. Photorealistic, no AI-glow, natural skin, no smoothing. Shot on 50mm lens, golden hour warmth, residential exterior."""

print("=== Step 1: Generating reference image (Gemini Pro Image) ===", flush=True)
resp = client.models.generate_content(
    model='gemini-3-pro-image-preview',
    contents=ref_prompt,
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(image_size='2K')
    )
)
ref_image_path = '/tmp/plumber-hero-ref.png'
saved = False
for part in resp.parts:
    if part.text is not None:
        print(f"  text: {part.text[:200]}", flush=True)
    if part.inline_data is not None:
        img_data = part.inline_data.data
        if isinstance(img_data, str):
            import base64
            img_data = base64.b64decode(img_data)
        img = PILImage.open(BytesIO(img_data))
        img.convert('RGB').save(ref_image_path, 'PNG')
        print(f"  Reference image saved: {ref_image_path} ({img.size})", flush=True)
        saved = True
        break

if not saved:
    print("ERROR: No image in response", flush=True)
    raise SystemExit(1)

print("\n=== Step 2: Generating Veo 3.1 video ===", flush=True)
with open(ref_image_path, 'rb') as f:
    img_bytes = f.read()

video_prompt = """The master plumber turns his head slightly and gives a confident smile. He lifts the pipe wrench in a subtle gesture of skill. Wind gently moves his shirt collar. Golden hour light flickers across the scene as leaves blow in the background trees. Subtle camera push-in. Cinematic, smooth, broadcast-quality motion."""

operation = client.models.generate_videos(
    model='veo-3.1-generate-preview',
    image=types.Image(image_bytes=img_bytes, mime_type='image/png'),
    config=types.GenerateVideosConfig(
        person_generation='allow_all',
        aspect_ratio='16:9',
    ),
    prompt=video_prompt,
)
print(f"Video operation started: {operation.name}", flush=True)

video_path = '/tmp/plumber-hero-video.mp4'
deadline = time.time() + 300
while time.time() < deadline:
    if operation.done:
        break
    time.sleep(15)
    try:
        operation = client.operations.get(operation)
    except Exception as e:
        print(f"poll error: {e}", flush=True)
    print(f"Polling... done={operation.done}", flush=True)

if not operation.done:
    print("Timed out", flush=True)
    raise SystemExit(2)

print(f"Operation complete", flush=True)
result = operation.result
if hasattr(result, 'videos') and result.videos:
    vid = result.videos[0]
    print(f"Downloading video: {vid}", flush=True)
    file_content = client.files.download(file=vid)
    with open(video_path, 'wb') as f:
        f.write(file_content)
    print(f"Video saved: {video_path} ({os.path.getsize(video_path)} bytes)", flush=True)
