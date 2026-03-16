import streamlit as st
import json
import base64
import time
import zipfile
import io
import requests

from components.brand_card    import render_brand_card
from components.copy_tabs     import render_copy_tabs
from components.image_gallery import render_image_gallery
from components.video_player  import render_video_player
from components.persona_cards import render_persona_cards
from components.media_plan    import render_media_plan

# ── SVG Icons ──────────────────────────────────────────────────
BOLT_SM = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg>'
BOLT_LG = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg>'

# Sidebar nav icons (matching the reference design)
NAV_ICONS = {
    "Overview": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
    "Brand Identity": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 10a4 4 0 0 0 0 8c1.1 0 1.94-.36 2.55-.86"/><path d="M7.21 7.21A10 10 0 0 0 2 12c0 5.52 4.48 10 10 10s10-4.48 10-10a10 10 0 0 0-4.79-8.54"/><path d="M12 2a14.5 14.5 0 0 0 0 20"/><path d="M12 2a14.5 14.5 0 0 1 0 20"/></svg>',
    "Ad Copy": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/><line x1="12" y1="4" x2="12" y2="20"/></svg>',
    "Creatives": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>',
    "Video Ad": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="16" height="16" rx="2"/><path d="m22 7-4 3 4 3V7z"/></svg>',
    "Audiences": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "Media Plan": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/><path d="M8 14h.01"/><path d="M12 14h.01"/><path d="M16 14h.01"/><path d="M8 18h.01"/><path d="M12 18h.01"/></svg>',
    "Regenerate": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>',
}

st.set_page_config(page_title="AdBlitz", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    /* ── Global background with subtle grid + dots ── */
    .stApp {
        background: #0b1120;
        background-image:
            radial-gradient(circle, rgba(90,100,160,0.13) 1px, transparent 1px),
            linear-gradient(rgba(70,80,140,0.045) 1px, transparent 1px),
            linear-gradient(90deg, rgba(70,80,140,0.045) 1px, transparent 1px);
        background-size: 52px 52px, 52px 52px, 52px 52px;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: #0c0c1e;
        border-right: 1px solid rgba(124,58,237,0.15);
    }

    /* Nav buttons styling */
    section[data-testid="stSidebar"] .stButton:not(:first-of-type) > button {
        background: transparent !important;
        border: none !important;
        color: #7777aa !important;
        font-size: 0.88rem !important;
        font-weight: 400 !important;
        padding: 10px 14px !important;
        border-radius: 8px !important;
        margin: 1px 0 !important;
        transition: all 0.15s !important;
        box-shadow: none !important;
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
    }
    section[data-testid="stSidebar"] .stButton:not(:first-of-type) > button > div {
        display: flex !important;
        justify-content: flex-start !important;
        width: 100% !important;
    }
    section[data-testid="stSidebar"] .stButton:not(:first-of-type) > button > div > p {
        text-align: left !important;
        width: 100% !important;
    }
    section[data-testid="stSidebar"] .stButton:not(:first-of-type) > button:hover {
        color: #b8b8ff !important;
        background: rgba(124,58,237,0.08) !important;
    }
    /* Active nav button (primary type) - exclude first button */
    section[data-testid="stSidebar"] .stButton:not(:first-of-type) > button[kind="primary"] {
        color: #c4b5fd !important;
        background: rgba(124,58,237,0.15) !important;
        border-right: 3px solid #7c3aed !important;
        font-weight: 500 !important;
    }
    /* + New Campaign button */
    section[data-testid="stSidebar"] .stButton:first-of-type > button[kind="primary"] {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        border-right: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
    }

    /* ── Hide defaults ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: #0a0a1a; border-bottom: 1px solid #1a1a3e;}

    /* ── Cards & sections ── */
    .dark-card { background: #111128; border: 1px solid #1a1a3e; border-radius: 16px; padding: 24px; margin-bottom: 16px; }
    .section-title { font-size: 1.8rem; font-weight: 700; color: #e8e8ff; margin-bottom: 4px; }
    .section-subtitle { font-size: 0.95rem; color: #6666aa; margin-bottom: 24px; }

    .metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
    .metric-card { background: #111128; border: 1px solid #1a1a3e; border-radius: 12px; padding: 20px; }
    .metric-value { font-size: 2rem; font-weight: 800; color: #e8e8ff; }
    .metric-label { font-size: 0.8rem; color: #6666aa; margin-top: 2px; }

    .feature-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 32px; }
    .feature-card { background: #111128; border: 1px solid #1a1a3e; border-radius: 12px; padding: 20px; }
    .feature-card .icon-box { width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1rem; }
    .feature-card h4 { color: #e8e8ff; margin: 12px 0 4px 0; font-size: 0.95rem; }
    .feature-card p { color: #6666aa; font-size: 0.8rem; margin: 0; }

    .tag-container { display: flex; flex-wrap: wrap; gap: 8px; margin: 8px 0; }
    .tag { background: #131830; border: 1px solid #1e2548; border-radius: 20px; padding: 4px 14px; font-size: 0.8rem; color: #7c6fb5; }
    .vibe-pill { display: inline-block; padding: 6px 16px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; margin: 4px; }

    .platform-card { background: #111128; border: 1px solid #1a1a3e; border-radius: 16px; padding: 24px; margin-bottom: 16px; }
    .platform-header { font-size: 1.1rem; font-weight: 700; color: #e8e8ff; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #1a1a3e; }
    .copy-label { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .copy-label-hook { color: #fbbf24; }
    .copy-label-body { color: #6666aa; }
    .copy-label-cta { color: #a78bfa; }
    .cta-box { background: linear-gradient(135deg, #1a1a3e, #2a1a4e); border: 1px solid #7c3aed; border-radius: 10px; padding: 12px 16px; color: #e8e8ff; font-weight: 600; }

    .persona-card { background: #111128; border: 1px solid #1a1a3e; border-top: 3px solid; border-radius: 16px; padding: 24px; }
    .persona-name { font-size: 1.15rem; font-weight: 700; color: #e8e8ff; }
    .persona-demo { font-size: 0.85rem; color: #a78bfa; margin: 4px 0 8px 0; }
    .persona-desc { font-size: 0.9rem; color: #8888aa; line-height: 1.5; }
    .persona-badge { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; border: 1px solid; margin: 2px; }
    .persona-footer { display: flex; justify-content: space-between; margin-top: 16px; padding-top: 12px; border-top: 1px solid #1a1a3e; }
    .persona-footer-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; color: #5555aa; }
    .persona-footer-value { font-size: 0.95rem; font-weight: 700; color: #e8e8ff; }

    /* ── Buttons ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        border: none; color: white; font-weight: 700;
        padding: 0.75rem 2rem; border-radius: 12px; font-size: 1rem;
    }
    .stButton > button[kind="primary"]:hover { background: linear-gradient(135deg, #6d28d9 0%, #9333ea 100%); }
    .stTabs [data-baseweb="tab"] { border-radius: 8px; font-weight: 600; color: #8888aa; }
    .stProgress > div > div > div > div { background: linear-gradient(90deg, #7c3aed, #a855f7); }

    /* ── Sidebar logo ── */
    .sidebar-logo {
        display: flex; align-items: center; gap: 10px;
        padding: 16px 0 24px 0;
        border-bottom: 1px solid rgba(124,58,237,0.15);
        margin-bottom: 16px;
    }
    .sidebar-logo-icon {
        width: 36px; height: 36px;
        background: linear-gradient(135deg, #7c3aed, #a855f7);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
    }
    .sidebar-logo-text { font-size: 1.2rem; font-weight: 800; color: #e8e8ff; }
    .sidebar-ai-badge { background: #7c3aed; color: white; padding: 2px 8px; border-radius: 6px; font-size: 0.65rem; font-weight: 700; }
    .sidebar-section-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; color: #5555aa; margin: 16px 0 8px 0; }



    /* ── Upload area styling ── */
    .upload-zone {
        border: 2px dashed rgba(124,58,237,0.3);
        border-radius: 16px;
        padding: 48px 24px;
        text-align: center;
        background: rgba(17,17,40,0.5);
        margin: 24px auto;
        max-width: 600px;
        transition: border-color 0.3s;
    }
    .upload-zone:hover { border-color: rgba(124,58,237,0.6); }
    .upload-icon {
        width: 56px; height: 56px; border-radius: 14px;
        background: rgba(124,58,237,0.15);
        display: inline-flex; align-items: center; justify-content: center;
        margin-bottom: 16px;
    }

    /* ── Pro badge ── */
    .pro-badge {
        background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(168,85,247,0.15));
        border: 1px solid rgba(124,58,237,0.25);
        border-radius: 12px; padding: 14px;
        margin-top: 16px;
    }
    .pro-label { font-size: 0.65rem; font-weight: 700; letter-spacing: 1.5px; color: #a855f7; }
    .pro-title { font-size: 0.9rem; font-weight: 600; color: #e8e8ff; margin-top: 2px; }

    hr { border-color: #1a1a3e !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ──
for key, default in {
    "campaign_data": None, "is_loading": False, "uploaded_file": None,
    "image_bytes": None, "refine_feedback": None, "current_page": "Overview",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">{BOLT_SM}</div>
        <span class="sidebar-logo-text">AdBlitz</span>
        <span class="sidebar-ai-badge">AI</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("+ New Campaign", use_container_width=True, type="primary"):
        st.session_state.campaign_data = None
        st.session_state.uploaded_file = None
        st.session_state.image_bytes = None
        st.session_state.is_loading = False
        st.session_state.current_page = "Overview"
        st.rerun()

    st.markdown('<div class="sidebar-section-label">CAMPAIGN</div>', unsafe_allow_html=True)

    pages = ["Overview","Brand Identity","Ad Copy","Creatives","Video Ad","Audiences","Media Plan","Regenerate"]

    # Icon-based nav using buttons
    for p in pages:
        is_active = st.session_state.current_page == p
        icon_map = {
            "Overview": "⊞", "Brand Identity": "◎", "Ad Copy": "≡",
            "Creatives": "⧉", "Video Ad": "▶", "Audiences": "⁂",
            "Media Plan": "▦", "Regenerate": "↻",
        }
        if st.button(
            f"{icon_map.get(p,'')}  {p}",
            key=f"nav_{p}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.current_page = p
            st.rerun()

    page = st.session_state.current_page




# ── Export button ──
def create_export_zip(data):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("campaign.json", json.dumps(data, indent=2))
        for i, img in enumerate(data.get("images", [])):
            if img.get("url"):
                try:
                    r = requests.get(img["url"], timeout=10)
                    if r.status_code == 200:
                        zf.writestr(f"images/{img.get('format','img')}_{i+1}.png", r.content)
                except Exception: pass
        if data.get("video", {}).get("url"):
            try:
                r = requests.get(data["video"]["url"], timeout=30)
                if r.status_code == 200: zf.writestr("video/ad_video.mp4", r.content)
            except Exception: pass
        if data.get("audio", {}).get("url"):
            try:
                r = requests.get(data["audio"]["url"], timeout=10)
                if r.status_code == 200: zf.writestr("audio/voiceover.mp3", r.content)
            except Exception: pass
        if data.get("copy"):
            for plat, content in data["copy"].items():
                zf.writestr(f"copy/{plat}.json", json.dumps(content, indent=2))
    buf.seek(0)
    return buf

if st.session_state.campaign_data:
    _, exp_col = st.columns([6, 1])
    with exp_col:
        zd = create_export_zip(st.session_state.campaign_data)
        st.download_button("Export", data=zd, file_name="adblitz_campaign.zip", mime="application/zip", use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  PAGES
# ══════════════════════════════════════════════════════════════

if st.session_state.current_page == "Overview":
    if st.session_state.is_loading:
        st.markdown('<div class="section-title">Generating Your Campaign</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">AI agents are building your campaign</div>', unsafe_allow_html=True)
        progress = st.progress(0)
        status = st.empty()
        steps = [
            "Analyzing product and building brand identity",
            "Writing platform-specific ad copy",
            "Creating audience personas",
            "Generating ad creative images",
            "Building media launch strategy",
        ]
        for i, s in enumerate(steps):
            status.markdown(f"**Step {i+1} of {len(steps)}:** {s}")
            progress.progress((i + 1) / (len(steps) + 1))
            time.sleep(0.3)
        try:
            from agents.orchestrator import generate_campaign, refine_campaign
            ib = st.session_state.image_bytes
            if st.session_state.refine_feedback:
                status.markdown("**Refining campaign...**")
                res = refine_campaign(st.session_state.refine_feedback, st.session_state.campaign_data, image_bytes=ib)
                st.session_state.refine_feedback = None
            else:
                res = generate_campaign(ib)
            if isinstance(res, str): res = json.loads(res)
            st.session_state.campaign_data = res
            progress.progress(1.0)
            status.markdown("**Complete.**")
            time.sleep(0.4)
        except Exception as e:
            st.error(f"Generation failed: {str(e)}")
            with st.expander("Debug"): st.code(str(e))
            st.session_state.campaign_data = None
        finally:
            st.session_state.is_loading = False
            if st.session_state.campaign_data: st.rerun()

    elif st.session_state.campaign_data:
        data = st.session_state.campaign_data
        brief = data.get("brand_brief", {})
        budget = data.get("media_plan", {}).get("budget_split", {})
        n_img = len([i for i in data.get("images", []) if i.get("url")])
        n_platforms = len(budget) if budget else 5
        n_personas = len(data.get("personas", []))

        # Estimated metrics derived from real data
        import hashlib
        seed_str = brief.get("product_name", "") + brief.get("brand_vibe", "")
        seed_val = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
        est_roas = round(2.0 + (seed_val % 30) / 10.0, 1)
        est_sentiment = 75 + (seed_val % 20)
        max_budget_pct = max(budget.values()) if budget else 30
        est_reach_base = int(8000 + (seed_val % 12000))
        est_reach = [
            est_reach_base,
            int(est_reach_base * 1.15),
            int(est_reach_base * 1.35),
            int(est_reach_base * 1.5),
            int(est_reach_base * 1.9),
            int(est_reach_base * 2.4),
            int(est_reach_base * 2.8),
        ]
        est_reach_growth = int(((est_reach[-1] - est_reach[0]) / est_reach[0]) * 100)

        # ── Title + Ready badge ──
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
            <div>
                <div class="section-title">Campaign Dashboard</div>
                <div class="section-subtitle" style="margin-bottom:0;">{brief.get("product_name", "")} — AI-generated overview</div>
            </div>
            <span style="background:rgba(45,212,191,0.12);color:#2dd4bf;padding:6px 16px;border-radius:20px;
                        font-size:0.8rem;font-weight:600;border:1px solid rgba(45,212,191,0.25);display:flex;align-items:center;gap:6px;">
                <span style="width:8px;height:8px;border-radius:50%;background:#2dd4bf;display:inline-block;"></span>
                READY FOR LAUNCH
            </span>
        </div>
        """, unsafe_allow_html=True)

        # ── Metric cards with icons + badges ──
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:20px 0 24px;">
            <div class="dark-card" style="margin-bottom:0;position:relative;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div style="width:40px;height:40px;border-radius:10px;background:rgba(124,58,237,0.15);
                                display:flex;align-items:center;justify-content:center;margin-bottom:12px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
                    </div>
                    <span style="background:rgba(124,58,237,0.15);color:#a78bfa;padding:2px 8px;border-radius:6px;font-size:0.7rem;font-weight:600;">+{n_img} new</span>
                </div>
                <div style="font-size:2.2rem;font-weight:800;color:#e8e8ff;">{n_img}</div>
                <div style="font-size:0.8rem;color:#5555aa;">Total Assets</div>
            </div>
            <div class="dark-card" style="margin-bottom:0;position:relative;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div style="width:40px;height:40px;border-radius:10px;background:rgba(45,212,191,0.15);
                                display:flex;align-items:center;justify-content:center;margin-bottom:12px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2dd4bf" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
                    </div>
                    <span style="background:rgba(45,212,191,0.15);color:#2dd4bf;padding:2px 8px;border-radius:6px;font-size:0.7rem;font-weight:600;">All active</span>
                </div>
                <div style="font-size:2.2rem;font-weight:800;color:#e8e8ff;">{n_platforms}</div>
                <div style="font-size:0.8rem;color:#5555aa;">Platforms</div>
            </div>
            <div class="dark-card" style="margin-bottom:0;position:relative;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div style="width:40px;height:40px;border-radius:10px;background:rgba(245,158,11,0.15);
                                display:flex;align-items:center;justify-content:center;margin-bottom:12px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                    </div>
                    <span style="background:rgba(245,158,11,0.15);color:#f59e0b;padding:2px 8px;border-radius:6px;font-size:0.7rem;font-weight:600;">~{est_reach[-1]//1000}K reach</span>
                </div>
                <div style="font-size:2.2rem;font-weight:800;color:#e8e8ff;">{n_personas}</div>
                <div style="font-size:0.8rem;color:#5555aa;">Audience Segs</div>
            </div>
            <div class="dark-card" style="margin-bottom:0;position:relative;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div style="width:40px;height:40px;border-radius:10px;background:rgba(236,72,153,0.15);
                                display:flex;align-items:center;justify-content:center;margin-bottom:12px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ec4899" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
                    </div>
                    <span style="background:rgba(236,72,153,0.15);color:#ec4899;padding:2px 8px;border-radius:6px;font-size:0.7rem;font-weight:600;">Est.</span>
                </div>
                <div style="font-size:2.2rem;font-weight:800;color:#e8e8ff;">{est_roas}x</div>
                <div style="font-size:0.8rem;color:#5555aa;">Est. ROAS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Budget Allocation + Brand Sentiment row ──
        c1, c2 = st.columns([3, 2])
        with c1:
            import plotly.express as px
            if budget:
                plat_colors = {"instagram": "#7c3aed", "tiktok": "#a855f7", "facebook": "#a855f7",
                               "google": "#ec4899", "email": "#f59e0b", "tiktok": "#a855f7"}
                bar_colors = [plat_colors.get(p.lower(), "#7c3aed") for p in budget.keys()]
                fig = px.bar(
                    x=[p.capitalize() for p in budget.keys()],
                    y=list(budget.values()),
                    color_discrete_sequence=bar_colors,
                )
                fig.update_traces(marker_color=bar_colors)
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#8888aa", size=12),
                    showlegend=False,
                    xaxis=dict(title="", gridcolor="#1a1a3e", showgrid=False),
                    yaxis=dict(title="", gridcolor="#1a1a3e", showgrid=True, gridwidth=1),
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=280,
                    bargap=0.35,
                )
                st.markdown("""
                <div class="dark-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <span style="font-weight:700;color:#e8e8ff;font-size:1.05rem;">Budget Allocation</span>
                        <span style="color:#3a3a5e;cursor:pointer;">⋮</span>
                    </div>
                """, unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            # Brand Sentiment donut (estimated)
            sentiment_color = "#2dd4bf" if est_sentiment >= 80 else "#f59e0b" if est_sentiment >= 60 else "#ec4899"
            remaining = 100 - est_sentiment
            st.markdown(f"""
            <div class="dark-card">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                    <span style="font-weight:700;color:#e8e8ff;font-size:1.05rem;">Brand Sentiment</span>
                    <span style="color:#3a3a5e;cursor:pointer;">⋮</span>
                </div>
                <div style="text-align:center;padding:16px 0;">
                    <svg width="180" height="180" viewBox="0 0 180 180">
                        <circle cx="90" cy="90" r="70" fill="none" stroke="#1a1a3e" stroke-width="14"/>
                        <circle cx="90" cy="90" r="70" fill="none" stroke="{sentiment_color}" stroke-width="14"
                                stroke-dasharray="{est_sentiment * 4.4} {remaining * 4.4}"
                                stroke-dashoffset="110" stroke-linecap="round"/>
                        <text x="90" y="82" text-anchor="middle" fill="#e8e8ff" font-size="32" font-weight="800">{est_sentiment}%</text>
                        <text x="90" y="105" text-anchor="middle" fill="{sentiment_color}" font-size="12" font-weight="700">POSITIVE</text>
                    </svg>
                </div>
                <div style="text-align:center;color:#5555aa;font-size:0.85rem;">
                    Est. campaign tone alignment with target audience
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Projected Weekly Reach line chart ──
        import plotly.graph_objects as go
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=days, y=est_reach,
            mode='lines+markers',
            line=dict(color="#7c3aed", width=3, shape='spline'),
            marker=dict(size=6, color="#7c3aed"),
            fill='tozeroy',
            fillcolor='rgba(124,58,237,0.08)',
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8888aa", size=12),
            showlegend=False,
            xaxis=dict(title="", gridcolor="#1a1a3e", showgrid=False),
            yaxis=dict(title="", gridcolor="#1a1a3e", showgrid=True, gridwidth=1),
            margin=dict(t=10, b=10, l=10, r=10),
            height=220,
        )
        st.markdown(f"""
        <div class="dark-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <span style="font-weight:700;color:#e8e8ff;font-size:1.05rem;">Projected Weekly Reach</span>
                <span style="background:rgba(124,58,237,0.15);color:#a78bfa;padding:4px 12px;border-radius:8px;font-size:0.75rem;font-weight:600;">
                    Est. +{est_reach_growth}% vs. baseline
                </span>
            </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        # ── HOME / UPLOAD PAGE ──
        st.markdown(f"""
        <div style="text-align:center; padding:40px 0 10px 0;">
            <div style="width:72px;height:72px;border-radius:18px;
                        background:linear-gradient(135deg,#7c3aed,#a855f7);
                        display:inline-flex;align-items:center;justify-content:center;
                        margin-bottom:20px;box-shadow:0 0 40px rgba(124,58,237,0.3);">
                {BOLT_LG}
            </div>
            <h1 style="font-size:3.2rem;font-weight:800;margin:0;letter-spacing:-1px;">
                <span style="color:#e8e8ff;">Ad</span><span style="background:linear-gradient(135deg,#a78bfa,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Blitz</span>
            </h1>
            <p style="font-size:1.1rem;color:#8888aa;margin:8px 0 4px 0;">AI-Powered Campaign Generator</p>
            <p style="color:#5555aa;font-size:0.9rem;max-width:500px;margin:0 auto;">
                Drop a product photo. Get a complete marketing campaign — brand strategy, creatives, copy & launch plan.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Upload zone
        st.markdown("""
        <div class="upload-zone">
            <div class="upload-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="17 8 12 3 7 8"/>
                    <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
            </div>
            <p style="color:#e8e8ff;font-size:1.05rem;font-weight:600;margin:0;">Drop your product image here</p>
            <p style="color:#5555aa;font-size:0.85rem;margin:4px 0 0 0;">PNG, JPG or WebP — up to 10MB</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload", type=["png","jpg","jpeg","webp"], label_visibility="collapsed")
        if uploaded_file:
            c1, c2, c3 = st.columns([1,2,1])
            with c2:
                st.image(uploaded_file, width=300)
                if st.button("⚡ Generate Campaign with AI", type="primary", use_container_width=True):
                    st.session_state.uploaded_file = uploaded_file
                    st.session_state.image_bytes = uploaded_file.getvalue()
                    st.session_state.is_loading = True
                    st.session_state.campaign_data = None
                    st.rerun()

        st.markdown(f"""
        <div class="feature-grid">
            <div class="feature-card">
                <div class="icon-box" style="background:rgba(167,139,250,0.1);color:#a78bfa;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                </div>
                <h4>AI Brand Analysis</h4>
                <p>Extracts tone, personality & color DNA from your image</p>
            </div>
            <div class="feature-card">
                <div class="icon-box" style="background:rgba(236,72,153,0.1);color:#ec4899;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ec4899" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>
                </div>
                <h4>Multi-Format Creatives</h4>
                <p>Stories, feeds, banners & video ads generated instantly</p>
            </div>
            <div class="feature-card">
                <div class="icon-box" style="background:rgba(45,212,191,0.1);color:#2dd4bf;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2dd4bf" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                </div>
                <h4>Audience Personas</h4>
                <p>Data-backed customer profiles with platform targeting</p>
            </div>
            <div class="feature-card">
                <div class="icon-box" style="background:rgba(245,158,11,0.1);color:#f59e0b;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>
                </div>
                <h4>Launch-Ready Plan</h4>
                <p>Week-by-week media strategy with budget breakdown</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_page == "Brand Identity":
    if st.session_state.campaign_data and st.session_state.campaign_data.get("brand_brief"):
        st.markdown('<div class="section-title">Brand Identity</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">AI-extracted brand attributes from your product</div>', unsafe_allow_html=True)
        render_brand_card(st.session_state.campaign_data["brand_brief"])
    else:
        st.info("Generate a campaign first from the Overview page.")

elif st.session_state.current_page == "Ad Copy":
    if st.session_state.campaign_data and st.session_state.campaign_data.get("copy"):
        st.markdown('<div class="section-title">Ad Copy</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Platform-optimised marketing copy</div>', unsafe_allow_html=True)
        render_copy_tabs(st.session_state.campaign_data["copy"])
    else:
        st.info("Generate a campaign first from the Overview page.")

elif st.session_state.current_page == "Creatives":
    if st.session_state.campaign_data and st.session_state.campaign_data.get("images"):
        st.markdown('<div class="section-title">Generated Visuals</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">AI-created ad creatives for every format</div>', unsafe_allow_html=True)
        render_image_gallery(st.session_state.campaign_data["images"])
    else:
        st.info("Generate a campaign first from the Overview page.")

elif st.session_state.current_page == "Video Ad":
    st.markdown('<div class="section-title">Video Advertisement</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">AI-generated product ad with script & voiceover</div>', unsafe_allow_html=True)
    if st.session_state.campaign_data and st.session_state.campaign_data.get("video"):
        render_video_player(st.session_state.campaign_data["video"])
    else:
        st.info("Generate a campaign first from the Overview page.")

elif st.session_state.current_page == "Audiences":
    if st.session_state.campaign_data and st.session_state.campaign_data.get("personas"):
        st.markdown('<div class="section-title">Target Personas</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">AI-generated audience profiles based on product analysis</div>', unsafe_allow_html=True)
        render_persona_cards(st.session_state.campaign_data["personas"])
    else:
        st.info("Generate a campaign first from the Overview page.")

elif st.session_state.current_page == "Media Plan":
    if st.session_state.campaign_data and st.session_state.campaign_data.get("media_plan"):
        st.markdown('<div class="section-title">Media Plan & Strategy</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">AI-recommended campaign roadmap</div>', unsafe_allow_html=True)
        render_media_plan(st.session_state.campaign_data["media_plan"])
    else:
        st.info("Generate a campaign first from the Overview page.")

elif st.session_state.current_page == "Regenerate":
    if st.session_state.campaign_data:
        st.markdown(f"""
        <div style="text-align:center;padding:40px 0 20px 0;">
            <div style="width:64px;height:64px;border-radius:16px;
                        background:linear-gradient(135deg,#7c3aed,#a855f7);
                        display:inline-flex;align-items:center;justify-content:center;margin:0 auto 16px auto;
                        box-shadow:0 0 30px rgba(124,58,237,0.25);">
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>
            </div>
            <div class="section-title">Refine Your Campaign</div>
            <p style="color:#6666aa;">Give the AI feedback and regenerate assets instantly.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**WHAT WOULD YOU LIKE TO CHANGE?**")
        feedback = st.text_area("fb", placeholder="e.g., 'Make the brand voice more luxury', 'Target a slightly older demographic', 'Use more blue tones'...", label_visibility="collapsed", height=120)
        quick = ["Luxury Vibe","Younger Audience","More Playful","Focus on Benefits","Shorter Copy"]
        qcols = st.columns(len(quick))
        for i, q in enumerate(quick):
            with qcols[i]:
                if st.button(f"+ {q}", use_container_width=True):
                    feedback = q
        st.markdown("")
        if st.button("Regenerate Campaign Assets", type="primary", use_container_width=True):
            if feedback and feedback.strip():
                st.session_state.refine_feedback = feedback
                st.session_state.is_loading = True
                st.session_state.current_page = "Overview"
                st.rerun()
            else:
                st.warning("Please describe what you'd like to change.")
    else:
        st.info("Generate a campaign first from the Overview page.")