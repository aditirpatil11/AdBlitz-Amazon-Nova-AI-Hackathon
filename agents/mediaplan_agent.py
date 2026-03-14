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

MEDIAPLAN_SYSTEM_PROMPT = """You are an expert digital media planner and advertising strategist.
You will be given a Brand Brief, ad copy for 5 platforms, and 3 customer personas.
Use all of this to create a complete 7-day launch strategy.

You MUST respond with ONLY valid JSON — no markdown, no explanation, no extra text.

Return this exact JSON structure:
{
    "budget_split": {
        "instagram": 40,
        "tiktok": 25,
        "google": 20,
        "email": 15
    },
    "daily_budget_recommendation": "$XX-$XX/day for first week",
    "platform_strategy": [
        {
            "platform": "Instagram",
            "creatives": ["carousel", "story", "video"],
            "targeting": "Which persona(s) this targets",
            "why": "One sentence explaining why this platform for this audience"
        }
    ],
    "ab_tests": [
        {
            "test": "What is being tested (e.g., Instagram hook)",
            "variant_a": "Version A text",
            "variant_b": "Version B text",
            "metric": "What metric to track (CTR, Conversions, etc.)",
            "duration": "How long to run the test",
            "winner_rule": "How to determine the winner"
        }
    ],
    "seven_day_calendar": [
        {
            "day": 1,
            "action": "What to do on this day",
            "platform": "Which platform",
            "budget": "$XX"
        }
    ]
}

Rules:
- budget_split: Percentages must add up to 100. Allocate based on where the target personas spend time.
- platform_strategy: One entry per platform (Instagram, TikTok, Google, Email). Include which creatives and which personas.
- ab_tests: Create 2 meaningful A/B tests. Use actual copy from the ad copy provided.
- seven_day_calendar: Exactly 7 days. Day 1 is soft launch, Day 7 is review/optimize. Ramp up spending mid-week.
- daily_budget_recommendation: Suggest a realistic daily budget for a small business.
- All recommendations should be practical and actionable for a small business owner.

Respond with ONLY the JSON object. Nothing else."""


def run_mediaplan_agent(brand_brief, copy_output, personas):
    """
    Takes Brand Brief, copy output, and personas.
    Returns a complete media plan dictionary.
    """
    context = {
        "brand_brief": brand_brief,
        "copy": copy_output,
        "personas": personas
    }

    request_body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": f"Here is everything you need:\n{json.dumps(context, indent=2)}\n\nCreate a complete 7-day media launch strategy."
                    }
                ]
            }
        ],
        "system": [
            {
                "text": MEDIAPLAN_SYSTEM_PROMPT
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

    media_plan = json.loads(raw_text)

    return media_plan


# --- Test independently ---
if __name__ == "__main__":
    from mock_data import MOCK_BRAND_BRIEF, MOCK_COPY, MOCK_PERSONAS

    print("Running Media Plan Agent with mock data...")
    result = run_mediaplan_agent(MOCK_BRAND_BRIEF, MOCK_COPY, MOCK_PERSONAS)
    print(json.dumps(result, indent=2))