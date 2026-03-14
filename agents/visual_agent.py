import json
import boto3
import streamlit as st

# Initialize Bedrock client
bedrock = boto3.client(
    "bedrock-runtime",
    region_name=st.secrets["AWS_REGION"],
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
)

VISUAL_SYSTEM_PROMPT = """You are an expert art director and visual marketing specialist.
You will be given a Brand Brief (JSON). Use it to write detailed image generation prompts
for an AI image generator (Amazon Nova Canvas).

You MUST respond with ONLY valid JSON — no markdown, no explanation, no extra text.

Return this exact JSON structure (an array of image objects):
[
    {
        "prompt": "A detailed, vivid image generation prompt. Include: subject, setting, lighting, mood, camera angle, style. Be very specific.",
        "format": "lifestyle",
        "platform": "instagram",
        "description": "Short human-readable description of what this image shows"
    },
    {
        "prompt": "...",
        "format": "hero",
        "platform": "all",
        "description": "..."
    },
    {
        "prompt": "...",
        "format": "carousel",
        "platform": "instagram",
        "description": "..."
    },
    {
        "prompt": "...",
        "format": "carousel",
        "platform": "instagram",
        "description": "..."
    },
    {
        "prompt": "...",
        "format": "carousel",
        "platform": "instagram",
        "description": "..."
    },
    {
        "prompt": "...",
        "format": "story",
        "platform": "instagram",
        "description": "..."
    }
]

Create exactly 6 images:
1. Lifestyle Image: Product in a real-world setting that matches the brand vibe. Show the product being used or displayed naturally.
2. Product Hero: Clean product shot on a branded background using colors from the color_palette. Include the tagline as text overlay concept.
3. Carousel Slide 1: Problem — show the pain point the product solves. Emotional, relatable.
4. Carousel Slide 2: Solution — show the product as the answer. Aspirational.
5. Carousel Slide 3: Social proof concept — product with visual cues of popularity (reviews, stars, happy customers).
6. Story Format: Vertical 9:16 composition for Instagram/TikTok stories. Product with bold CTA text concept.

Rules for prompts:
- Each prompt must be 2-4 sentences, highly descriptive
- Include lighting direction (soft, warm, natural, studio, golden hour)
- Include camera angle (close-up, overhead, eye-level, slight angle)
- Include mood/atmosphere (cozy, energetic, minimal, luxurious)
- Use colors from the brand's color_palette
- Match the brand_vibe in every prompt
- Do NOT include any text in the prompts — Nova Canvas cannot render text well
- Focus on photorealistic, commercial-quality imagery

Respond with ONLY the JSON array. Nothing else."""


def run_visual_agent(brand_brief):
    """
    Takes a Brand Brief dictionary, sends to Nova Lite.
    Returns a list of image prompt objects.
    These prompts will later be sent to Nova Canvas by Person 2.
    """
    request_body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": f"Here is the Brand Brief:\n{json.dumps(brand_brief, indent=2)}\n\nWrite 6 detailed image generation prompts for this product's ad campaign."
                    }
                ]
            }
        ],
        "system": [
            {
                "text": VISUAL_SYSTEM_PROMPT
            }
        ],
        "inferenceConfig": {
            "maxTokens": 2048,
            "temperature": 0.7
        }
    }

    response = bedrock.invoke_model(
        modelId=st.secrets["BEDROCK_MODEL_ID"],
        body=json.dumps(request_body),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    raw_text = response_body["output"]["message"]["content"][0]["text"]

    # Clean up response
    raw_text = raw_text.strip()
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    if raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]
    raw_text = raw_text.strip()

    image_prompts = json.loads(raw_text)

    return image_prompts


# --- Test independently ---
if __name__ == "__main__":
    from mock_data import MOCK_BRAND_BRIEF

    print("Running Visual Agent with mock brand brief...")
    result = run_visual_agent(MOCK_BRAND_BRIEF)
    print(json.dumps(result, indent=2))