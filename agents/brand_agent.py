import json
import boto3
import base64
import streamlit as st

# Initialize Bedrock client
bedrock = boto3.client(
    "bedrock-runtime",
    region_name=st.secrets["AWS_REGION"],
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
)

BRAND_SYSTEM_PROMPT = """You are an expert brand strategist and marketing consultant. 
You will be given a product photo. Analyze it carefully and create a complete brand brief.

You MUST respond with ONLY valid JSON — no markdown, no explanation, no extra text.

Return this exact JSON structure:
{
    "product_name": "Name of the product",
    "category": "Product category (e.g., Home & Wellness, Fashion, Tech, Food & Beverage)",
    "target_audience": "Primary target audience description",
    "brand_vibe": "2-4 word brand vibe (e.g., calm, minimal, premium)",
    "brand_voice": "2-4 word brand voice (e.g., warm, soft-spoken, aspirational)",
    "color_palette": ["#hex1", "#hex2", "#hex3"],
    "taglines": ["tagline 1", "tagline 2", "tagline 3"],
    "selling_points": ["point 1", "point 2", "point 3"],
    "emotional_angle": "The core emotional appeal (e.g., comfort and self-care)"
}

Rules:
- color_palette: Extract 3 colors from the product image + complementary colors. Use hex codes.
- taglines: Write 3 punchy, memorable taglines. Short and catchy.
- selling_points: Infer 3 key selling points from what you see in the image.
- brand_vibe: Think about what aesthetic this product represents.
- brand_voice: How should ads for this product sound?
- emotional_angle: What feeling should the customer associate with this product?
- target_audience: Be specific — include age range, gender if relevant, lifestyle.

Respond with ONLY the JSON object. Nothing else."""


def run_brand_agent(image_bytes):
    """
    Takes raw image bytes, sends to Nova Lite for brand analysis.
    Returns a parsed Brand Brief dictionary.
    """
    # Convert image to base64
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # Detect image type (default to jpeg)
    if image_bytes[:8] == b'\x89PNG\r\n\x1a\n':
        media_type = "image/png"
    else:
        media_type = "image/jpeg"

    # Build the request for Nova Lite
    request_body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "image": {
                            "format": media_type.split("/")[1],
                            "source": {
                                "bytes": image_base64
                            }
                        }
                    },
                    {
                        "text": "Analyze this product photo and create a complete brand brief."
                    }
                ]
            }
        ],
        "system": [
            {
                "text": BRAND_SYSTEM_PROMPT
            }
        ],
        "inferenceConfig": {
            "maxTokens": 1024,
            "temperature": 0.7
        }
    }

    # Call Nova Lite via Bedrock
    response = bedrock.invoke_model(
        modelId=st.secrets["BEDROCK_MODEL_ID"],
        body=json.dumps(request_body),
        contentType="application/json",
        accept="application/json"
    )

    # Parse the response
    response_body = json.loads(response["body"].read())
    raw_text = response_body["output"]["message"]["content"][0]["text"]

    # Clean up response — remove markdown fences if Nova adds them
    raw_text = raw_text.strip()
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    if raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]
    raw_text = raw_text.strip()

    # Parse JSON
    brand_brief = json.loads(raw_text)

    return brand_brief


# --- Test independently ---
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python brand_agent.py <image_path>")
        print("Example: python brand_agent.py test_candle.jpg")
        sys.exit(1)

    image_path = sys.argv[1]
    with open(image_path, "rb") as f:
        img_bytes = f.read()

    print("Running Brand Agent...")
    result = run_brand_agent(img_bytes)
    print(json.dumps(result, indent=2))