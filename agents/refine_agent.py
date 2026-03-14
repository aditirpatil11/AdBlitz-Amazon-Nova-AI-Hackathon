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

REFINE_SYSTEM_PROMPT = """You are an expert campaign manager who reviews ad campaigns and determines what needs to change based on user feedback.

You will be given:
1. The current full campaign output (brand brief, copy, personas, media plan, video details)
2. User feedback in plain English (e.g., "make it more playful", "target younger audience", "different color scheme")

Your job is to determine which agents need to re-run and what changes to make.

You MUST respond with ONLY valid JSON — no markdown, no explanation, no extra text.

Return this exact JSON structure:
{
    "agents_to_rerun": ["brand_agent", "copy_agent"],
    "changes": [
        {
            "agent": "brand_agent",
            "instruction": "Specific instruction for what this agent should change. Be precise."
        },
        {
            "agent": "copy_agent",
            "instruction": "Specific instruction for what this agent should change."
        }
    ],
    "reasoning": "One sentence explaining your decision"
}

Valid agent names: brand_agent, copy_agent, audience_agent, mediaplan_agent, visual_agent, video_agent, audio_agent

Rules for deciding which agents to re-run:
- "make copy more casual/playful/serious" → copy_agent only
- "target younger/older/different audience" → brand_agent + audience_agent + copy_agent
- "different colors/look/aesthetic" → brand_agent + visual_agent
- "change video style/pace" → video_agent + audio_agent
- "different voice/tone" → audio_agent only
- "change budget/strategy" → mediaplan_agent only
- "make it more energetic/calm" → brand_agent + copy_agent + visual_agent + video_agent + audio_agent
- "different tagline" → brand_agent + copy_agent
- If feedback is vague, re-run the minimum necessary agents
- ALWAYS include downstream agents: if brand_agent changes, copy_agent should also re-run since it depends on the brand brief
- Be conservative — only re-run what's actually affected by the feedback

Respond with ONLY the JSON object. Nothing else."""


def run_refine_agent(feedback, current_campaign):
    """
    Takes user feedback and current campaign output.
    Returns which agents need to re-run and what changes to make.
    """
    request_body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": f"Here is the current campaign:\n{json.dumps(current_campaign, indent=2)}\n\nUser feedback: \"{feedback}\"\n\nWhich agents need to re-run and what should change?"
                    }
                ]
            }
        ],
        "system": [
            {
                "text": REFINE_SYSTEM_PROMPT
            }
        ],
        "inferenceConfig": {
            "maxTokens": 1024,
            "temperature": 0.5
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

    refine_output = json.loads(raw_text)

    return refine_output


# --- Test independently ---
if __name__ == "__main__":
    from mock_data import MOCK_BRAND_BRIEF, MOCK_COPY, MOCK_PERSONAS, MOCK_MEDIA_PLAN

    mock_campaign = {
        "brand_brief": MOCK_BRAND_BRIEF,
        "copy": MOCK_COPY,
        "personas": MOCK_PERSONAS,
        "media_plan": MOCK_MEDIA_PLAN
    }

    feedback = "Make the copy more playful and fun"

    print(f"Running Refine Agent with feedback: '{feedback}'...")
    result = run_refine_agent(feedback, mock_campaign)
    print(json.dumps(result, indent=2))