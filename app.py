import streamlit as st
import base64
import json

from components.upload        import render_upload
from components.loading       import render_loading
from components.brand_card    import render_brand_card
from components.copy_tabs     import render_copy_tabs
from components.image_gallery import render_image_gallery
from components.video_player  import render_video_player
from components.persona_cards import render_persona_cards
from components.media_plan    import render_media_plan
from components.refine_bar    import render_refine_bar

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="AdBlitz",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Global CSS ────────────────────────────────────────────────
st.markdown("""
    <style>
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none; color: white; font-weight: bold;
        padding: 0.6rem 2rem; border-radius: 8px; font-size: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0; font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.markdown("""
    <div style="text-align:center; padding:32px 0 16px 0;">
        <h1 style="font-size:3rem; margin:0;">⚡ AdBlitz</h1>
        <p style="font-size:1.3rem; color:#888; margin:4px 0 0 0;">
            One Photo. Full Campaign. 90 Seconds.
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ── Session state ─────────────────────────────────────────────
for key, default in {
    "campaign_data":   None,
    "is_loading":      False,
    "uploaded_file":   None,
    "image_bytes":     None,
    "refine_feedback": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ── Callbacks ─────────────────────────────────────────────────
def handle_generate(uploaded_file):
    st.session_state.uploaded_file = uploaded_file
    st.session_state.image_bytes   = uploaded_file.getvalue()
    st.session_state.is_loading    = True
    st.session_state.campaign_data = None
    st.rerun()


def handle_refine(feedback):
    st.session_state.refine_feedback = feedback
    st.session_state.is_loading      = True
    st.rerun()


# ── Upload (always visible) ───────────────────────────────────
render_upload(on_generate=handle_generate)

st.divider()

# ── Loading → campaign data ───────────────────────────────────
if st.session_state.is_loading:
    render_loading()
    try:
        from agents.orchestrator import generate_campaign, refine_campaign

        image_bytes = st.session_state.image_bytes

        if st.session_state.refine_feedback:
            result = refine_campaign(
                st.session_state.refine_feedback,
                st.session_state.campaign_data,
                image_bytes=image_bytes
            )
            st.session_state.refine_feedback = None

        else:
            result = generate_campaign(image_bytes)

        # Safety net — if result is a string parse it
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError as je:
                raise Exception(
                    f"Agent returned invalid JSON: {je}\n\n"
                    f"Raw output (first 500 chars):\n{result[:500]}"
                )

        st.session_state.campaign_data = result

    except Exception as e:
        st.error(f"⚠️ Campaign generation failed: {str(e)}")
        with st.expander("🐛 Debug info — share this with Person 1"):
            st.code(str(e))
        st.info("Please try again.")
        st.session_state.campaign_data = None

    finally:
        st.session_state.is_loading = False
        # Only rerun if campaign generated successfully — this enables scrolling
        if st.session_state.campaign_data is not None:
            st.rerun()

# ── Display campaign ──────────────────────────────────────────
if st.session_state.campaign_data:
    data = st.session_state.campaign_data

    st.success("🎉 Your campaign is ready! Scroll down to explore ⬇️")

    # Metrics bar
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Platforms Covered", "5")
    m2.metric("Ad Creatives",      str(len(data.get("images",   []))))
    m3.metric("Audience Personas", str(len(data.get("personas", []))))
    m4.metric("Generated In",      "< 90s")

    st.divider()

    if data.get("brand_brief"):
        render_brand_card(data["brand_brief"])
        st.divider()

    if data.get("copy"):
        render_copy_tabs(data["copy"])
        st.divider()

    if data.get("images"):
        render_image_gallery(data["images"])
        st.divider()

    if data.get("video"):
        render_video_player(data["video"])
        st.divider()

    if data.get("personas"):
        render_persona_cards(data["personas"])
        st.divider()

    if data.get("media_plan"):
        render_media_plan(data["media_plan"])

    render_refine_bar(on_refine=handle_refine)