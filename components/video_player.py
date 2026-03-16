import streamlit as st


def render_video_player(video):
    if not video.get("url"):
        st.warning("Video generation failed. Try regenerating from the Regenerate page.")
        return

    col1, col2 = st.columns([3, 2])

    with col1:
        # Video player
        st.video(video["url"])

        # Style pills
        styles = ["Pop", "Corporate", "Lo-Fi", "Upbeat"]
        pills_html = ""
        for i, s in enumerate(styles):
            if i == 0:
                pills_html += f'<span style="display:inline-flex;align-items:center;gap:6px;padding:6px 16px;border-radius:20px;font-size:0.85rem;font-weight:600;background:rgba(124,58,237,0.2);border:1px solid #7c3aed;color:#c4b5fd;margin-right:8px;"><span style="width:8px;height:8px;border-radius:50%;background:#7c3aed;"></span>{s}</span>'
            else:
                pills_html += f'<span style="display:inline-flex;align-items:center;gap:6px;padding:6px 16px;border-radius:20px;font-size:0.85rem;font-weight:500;background:transparent;border:1px solid #2a2a5e;color:#7777aa;margin-right:8px;"><span style="width:8px;height:8px;border-radius:50%;background:#3a3a5e;"></span>{s}</span>'

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:4px;margin-top:16px;flex-wrap:wrap;">
            {pills_html}
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # ── AI Script & Voice card ──
        audio = video.get("voiceover_script", "")
        voice_style = video.get("voice_style", "Sophia")

        st.markdown(f"""
        <div class="dark-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                <span style="font-size:1.05rem;font-weight:700;color:#e8e8ff;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:8px;"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="22"/></svg>
                    AI Script & Voice
                </span>
                <span style="color:#3a3a5e;cursor:pointer;">⋮</span>
            </div>
            <div style="background:rgba(124,58,237,0.08);border:1px solid rgba(124,58,237,0.25);border-radius:10px;padding:14px;margin-bottom:14px;">
                <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#a78bfa;margin-bottom:6px;">
                    VOICE: {voice_style.upper()} (NATURAL)
                </div>
                <div style="color:#c8c8e8;line-height:1.6;font-size:0.9rem;font-style:italic;">
                    "{audio}"
                </div>
            </div>
        """, unsafe_allow_html=True)

        # ── Scene breakdown ──
        overlays = video.get("text_overlays", [])
        scene_labels = ["CINEMATIC PAN", "LIFESTYLE ACTION", "DETAIL SHOT", "CLOSING FRAME", "TRANSITION"]
        if overlays:
            for j, overlay in enumerate(overlays):
                label = scene_labels[j] if j < len(scene_labels) else f"SCENE {j+1}"
                st.markdown(f"""
                <div style="background:#0a0a1a;border:1px solid #1a1a3e;border-radius:8px;padding:12px 14px;margin-bottom:8px;">
                    <div style="font-size:0.7rem;font-weight:600;color:#5555aa;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">
                        SCENE {j+1} · {label}
                    </div>
                    <div style="color:#9999bb;font-size:0.88rem;line-height:1.5;">{overlay.get('text','')}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Performance Estimate card ──
        duration = video.get("duration_seconds", 6)
        has_voice = video.get("has_voiceover", False)

        st.markdown(f"""
        <div class="dark-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                <span style="font-size:1.05rem;font-weight:700;color:#e8e8ff;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:8px;"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
                    Performance Estimate
                </span>
                <span style="color:#3a3a5e;cursor:pointer;">⋮</span>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                <div style="background:#0a0a1a;border:1px solid #1a1a3e;border-radius:10px;padding:16px;">
                    <div style="margin-bottom:8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#60a5fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
                    </div>
                    <div style="font-size:1.6rem;font-weight:800;color:#e8e8ff;">{duration}s</div>
                    <div style="font-size:0.75rem;color:#5555aa;">Avg View Time</div>
                </div>
                <div style="background:#0a0a1a;border:1px solid #1a1a3e;border-radius:10px;padding:16px;">
                    <div style="margin-bottom:8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f472b6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
                    </div>
                    <div style="font-size:1.6rem;font-weight:800;color:#e8e8ff;">3.2%</div>
                    <div style="font-size:0.75rem;color:#5555aa;">CTR Estimate</div>
                </div>
                <div style="background:#0a0a1a;border:1px solid #1a1a3e;border-radius:10px;padding:16px;">
                    <div style="margin-bottom:8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fb923c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg>
                    </div>
                    <div style="font-size:1.6rem;font-weight:800;color:#e8e8ff;">240K</div>
                    <div style="font-size:0.75rem;color:#5555aa;">Impressions</div>
                </div>
                <div style="background:#0a0a1a;border:1px solid #1a1a3e;border-radius:10px;padding:16px;">
                    <div style="margin-bottom:8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                    </div>
                    <div style="font-size:1.6rem;font-weight:800;color:#e8e8ff;">$0.03</div>
                    <div style="font-size:0.75rem;color:#5555aa;">Cost / View</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)