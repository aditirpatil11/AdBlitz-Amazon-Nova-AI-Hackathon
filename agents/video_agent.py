import json
from agents._json_utils import parse_json_response
from services.bedrock import call_nova_text

VIDEO_SYSTEM_PROMPT = """You are a world-class commercial video director.
You will be given a Brand Brief and a TikTok script.
Write a video generation prompt for Amazon Nova Reel.

You MUST respond with ONLY valid JSON - no markdown, no explanation, no extra text.

Return this exact JSON structure:
{
    "video_prompt": "Under 500 characters. One continuous cinematic scene.",
    "duration_seconds": 6,
    "text_overlays": [
        {
            "text": "Short tagline",
            "time_start": "0s",
            "time_end": "3s",
            "position": "center"
        },
        {
            "text": "Brand name or CTA",
            "time_start": "4s",
            "time_end": "6s",
            "position": "bottom"
        }
    ],
    "voiceover_script": "Max 2 short sentences that fit in 6 seconds."
}

CRITICAL RULES for video_prompt:
- MUST be under 500 characters
- Describe ONE simple, elegant scene with slow camera movement
- Focus on ATMOSPHERE and MOOD, not actions or people doing things
- GOOD examples:
  "Soft morning light slowly fills a cozy bedroom. A candle glows on a wooden nightstand beside fresh flowers. Camera gently drifts forward, warm golden tones throughout."
  "Close-up of a candle flame flickering in a dark room. Camera slowly pulls back revealing a peaceful living space with warm ambient lighting."
  "Gentle camera pan across a minimalist table setting. A lit candle casts warm shadows on natural wood. Soft bokeh lights in the background."
- BAD examples (NEVER do these):
  "A person lights a candle" — AI generates weird hand movements
  "Someone reaches for the product" — AI generates unnatural body parts
  "A woman picks up the candle and smiles" — AI cannot do realistic human actions
- NEVER include people lighting, touching, picking up, or interacting with the product
- NEVER describe hands, fingers, or body movements
- Keep it simple: product + environment + lighting + slow camera movement
- Match the brand_vibe from the Brand Brief

CRITICAL RULES for text_overlays:
- Maximum 2 overlays
- Keep text SHORT — max 4 words per overlay
- First overlay: brand tagline
- Second overlay: product name only
- Position: "center" or "bottom" only

CRITICAL RULES for voiceover_script:
- Max 2 short sentences
- Must fit naturally in 6 seconds when spoken
- Match brand_voice
- End with product name

Respond with ONLY the JSON object. Nothing else."""


def run_video_agent(brand_brief, tiktok_copy):
    raw_text = call_nova_text(
        prompt=(
            f"Here is the Brand Brief:\n{json.dumps(brand_brief, indent=2)}"
            f"\n\nHere is the TikTok script:\n{json.dumps(tiktok_copy, indent=2)}"
            "\n\nWrite a cinematic video prompt (UNDER 500 CHARACTERS, NO PEOPLE, NO HANDS, just atmosphere and product)."
        ),
        system_prompt=VIDEO_SYSTEM_PROMPT,
        max_tokens=1024,
        temperature=0.7,
    )
    result = parse_json_response(raw_text)

    # Safety: truncate if over 512
    if len(result.get("video_prompt", "")) > 512:
        result["video_prompt"] = result["video_prompt"][:510]

    # Safety: limit text overlays to 2
    if len(result.get("text_overlays", [])) > 2:
        result["text_overlays"] = result["text_overlays"][:2]

    return result


if __name__ == "__main__":
    from mock_data import MOCK_BRAND_BRIEF, MOCK_COPY

    print("Running Video Agent with mock data...")
    result = run_video_agent(MOCK_BRAND_BRIEF, MOCK_COPY["tiktok"])
    print(f"Prompt length: {len(result['video_prompt'])} chars")
    print(json.dumps(result, indent=2))