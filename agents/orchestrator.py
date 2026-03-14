import json
import streamlit as st
from agents.brand_agent import run_brand_agent
from agents.copy_agent import run_copy_agent
from agents.audience_agent import run_audience_agent
from agents.visual_agent import run_visual_agent
from agents.video_agent import run_video_agent
from agents.audio_agent import run_audio_agent
from agents.mediaplan_agent import run_mediaplan_agent
from agents.refine_agent import run_refine_agent


def generate_campaign(image_bytes, status_callback=None):
    """
    Main pipeline: takes a product photo and runs all 7 agents in order.
    Returns the complete campaign output matching Data Contract 7.
    
    status_callback: optional function to update UI with progress
                     e.g., status_callback("Brand Agent analyzing product...")
    """
    campaign = {}

    # --- Step 1: Brand Agent (everything depends on this) ---
    if status_callback:
        status_callback("Brand Agent analyzing product...")
    brand_brief = run_brand_agent(image_bytes)
    campaign["brand_brief"] = brand_brief

    # --- Step 2: Copy Agent (needs brand brief) ---
    if status_callback:
        status_callback("Copy Agent writing ad copy...")
    copy_output = run_copy_agent(brand_brief)
    campaign["copy"] = copy_output

    # --- Step 3: Audience Agent (needs brand brief) ---
    if status_callback:
        status_callback("Audience Agent creating personas...")
    personas = run_audience_agent(brand_brief)
    campaign["personas"] = personas

    # --- Step 4: Visual Agent (needs brand brief) ---
    if status_callback:
        status_callback("Visual Agent creating image prompts...")
    image_prompts = run_visual_agent(brand_brief)
    campaign["images"] = image_prompts

    # --- Step 5: Video Agent (needs brand brief + tiktok copy) ---
    if status_callback:
        status_callback("Video Agent creating video prompt...")
    tiktok_copy = copy_output.get("tiktok", {})
    video_output = run_video_agent(brand_brief, tiktok_copy)
    campaign["video"] = video_output

    # --- Step 6: Audio Agent (needs brand brief + voiceover script) ---
    if status_callback:
        status_callback("Audio Agent selecting voice...")
    voiceover_script = video_output.get("voiceover_script", "")
    audio_output = run_audio_agent(brand_brief, voiceover_script)
    campaign["audio"] = audio_output

    # --- Step 7: Media Plan Agent (needs everything) ---
    if status_callback:
        status_callback("Media Plan Agent creating launch strategy...")
    media_plan = run_mediaplan_agent(brand_brief, copy_output, personas)
    campaign["media_plan"] = media_plan

    if status_callback:
        status_callback("Campaign complete!")

    return campaign


def refine_campaign(feedback, current_campaign, image_bytes=None, status_callback=None):
    """
    Takes user feedback and current campaign.
    Determines which agents to re-run and updates only those parts.
    Returns the updated campaign.
    """
    if status_callback:
        status_callback("Analyzing your feedback...")

    # Step 1: Ask Refine Agent what to change
    refine_result = run_refine_agent(feedback, current_campaign)
    agents_to_rerun = refine_result.get("agents_to_rerun", [])
    changes = {c["agent"]: c["instruction"] for c in refine_result.get("changes", [])}

    brand_brief = current_campaign["brand_brief"]
    copy_output = current_campaign["copy"]
    personas = current_campaign["personas"]

    # Step 2: Re-run only the affected agents
    if "brand_agent" in agents_to_rerun and image_bytes:
        if status_callback:
            status_callback("Re-running Brand Agent...")
        brand_brief = run_brand_agent(image_bytes)
        current_campaign["brand_brief"] = brand_brief

    if "copy_agent" in agents_to_rerun:
        if status_callback:
            status_callback("Re-running Copy Agent...")
        copy_output = run_copy_agent(brand_brief)
        current_campaign["copy"] = copy_output

    if "audience_agent" in agents_to_rerun:
        if status_callback:
            status_callback("Re-running Audience Agent...")
        personas = run_audience_agent(brand_brief)
        current_campaign["personas"] = personas

    if "visual_agent" in agents_to_rerun:
        if status_callback:
            status_callback("Re-running Visual Agent...")
        image_prompts = run_visual_agent(brand_brief)
        current_campaign["images"] = image_prompts

    if "video_agent" in agents_to_rerun:
        if status_callback:
            status_callback("Re-running Video Agent...")
        tiktok_copy = copy_output.get("tiktok", {})
        video_output = run_video_agent(brand_brief, tiktok_copy)
        current_campaign["video"] = video_output

    if "audio_agent" in agents_to_rerun:
        if status_callback:
            status_callback("Re-running Audio Agent...")
        voiceover_script = current_campaign.get("video", {}).get("voiceover_script", "")
        audio_output = run_audio_agent(brand_brief, voiceover_script)
        current_campaign["audio"] = audio_output

    if "mediaplan_agent" in agents_to_rerun:
        if status_callback:
            status_callback("Re-running Media Plan Agent...")
        media_plan = run_mediaplan_agent(brand_brief, copy_output, personas)
        current_campaign["media_plan"] = media_plan

    if status_callback:
        status_callback("Refinement complete!")

    return current_campaign


# --- Test independently ---
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m agents.orchestrator <image_path>")
        print("Example: python -m agents.orchestrator test_candle.jpg")
        sys.exit(1)

    image_path = sys.argv[1]
    with open(image_path, "rb") as f:
        img_bytes = f.read()

    def print_status(msg):
        print(f"  >> {msg}")

    print("Running full campaign pipeline...")
    result = generate_campaign(img_bytes, status_callback=print_status)
    print("\n=== FULL CAMPAIGN OUTPUT ===")
    print(json.dumps(result, indent=2))