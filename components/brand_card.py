import streamlit as st


def render_brand_card(brand):
    # ── Hero Banner with product name + category using brand colors ──
    colors = brand.get("color_palette", ["#7c3aed", "#a855f7", "#ec4899"])
    c1 = colors[0] if len(colors) > 0 else "#7c3aed"
    c2 = colors[1] if len(colors) > 1 else "#a855f7"
    c3 = colors[2] if len(colors) > 2 else "#ec4899"

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, {c1}33, {c2}22, {c3}11);
                border:1px solid {c1}44;border-radius:16px;padding:28px 32px;margin-bottom:24px;
                position:relative;overflow:hidden;">
        <div style="position:absolute;top:-30px;right:-30px;width:120px;height:120px;
                    background:radial-gradient(circle,{c1}22,transparent 70%);border-radius:50%;"></div>
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
            <div style="width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,{c1},{c2});
                        display:flex;align-items:center;justify-content:center;">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg>
            </div>
            <div>
                <div style="font-size:1.6rem;font-weight:800;color:#e8e8ff;letter-spacing:-0.5px;">{brand.get("product_name","Product")}</div>
                <div style="font-size:0.85rem;color:#8888aa;">{brand.get("category","")}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Two column layout: Left (personality/voice/audience) | Right (color palette) ──
    left, right = st.columns([1, 1])

    with left:
        # ── Core Personality card ──
        st.markdown(f"""
        <div class="dark-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                <span style="font-size:1.05rem;font-weight:700;color:#e8e8ff;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:8px;"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 4a2 2 0 1 1-2 2 2 2 0 0 1 2-2zm3 10H9a1 1 0 0 1 0-2h6a1 1 0 0 1 0 2z"/></svg>
                    Core Personality
                </span>
                <span style="color:#3a3a5e;cursor:pointer;">⋮</span>
            </div>
        """, unsafe_allow_html=True)

        vibe_words = [v.strip() for v in brand["brand_vibe"].split(",")]
        pills_html = '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px;">'
        for i, word in enumerate(vibe_words):
            c = colors[i % len(colors)]
            pills_html += f'<span style="display:inline-block;padding:7px 18px;border-radius:20px;font-size:0.85rem;font-weight:600;background:{c}22;color:{c};border:1px solid {c}44;">{word}</span>'
        pills_html += '</div>'
        st.markdown(pills_html, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Brand Voice card ──
        st.markdown(f"""
        <div class="dark-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                <span style="font-size:1.05rem;font-weight:700;color:#e8e8ff;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ec4899" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:8px;"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="22"/></svg>
                    Brand Voice
                </span>
                <span style="color:#3a3a5e;cursor:pointer;">⋮</span>
            </div>
            <div style="color:#9999bb;font-size:0.95rem;line-height:1.6;">{brand["brand_voice"]}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Category + Emotional Angle grid ──
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;">
            <div class="dark-card" style="margin-bottom:0;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>
                    <span style="font-size:0.7rem;color:#5555aa;text-transform:uppercase;letter-spacing:1px;font-weight:600;">Category</span>
                </div>
                <div style="font-size:0.95rem;font-weight:700;color:#e8e8ff;">{brand["category"]}</div>
            </div>
            <div class="dark-card" style="margin-bottom:0;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f472b6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
                    <span style="font-size:0.7rem;color:#5555aa;text-transform:uppercase;letter-spacing:1px;font-weight:600;">Emotional Angle</span>
                </div>
                <div style="font-size:0.95rem;font-weight:700;color:#e8e8ff;">{brand["emotional_angle"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Target Audience card ──
        st.markdown(f"""
        <div class="dark-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span style="font-size:1.05rem;font-weight:700;color:#e8e8ff;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2dd4bf" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:8px;"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                    Target Audience
                </span>
                <span style="color:#3a3a5e;cursor:pointer;">⋮</span>
            </div>
            <div style="color:#9999bb;font-size:0.95rem;line-height:1.6;">{brand["target_audience"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        # ── Color Palette card ──
        st.markdown(f"""
        <div class="dark-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                <span style="font-size:1.05rem;font-weight:700;color:#e8e8ff;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:8px;"><circle cx="13.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="10.5" r="2.5"/><circle cx="8.5" cy="7.5" r="2.5"/><circle cx="6.5" cy="12.5" r="2.5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>
                    Color Palette
                </span>
                <span style="color:#3a3a5e;cursor:pointer;">⋮</span>
            </div>
        """, unsafe_allow_html=True)

        # Large rounded swatches with hex overlay
        swatches_html = '<div style="display:flex;gap:12px;margin-bottom:20px;">'
        for color in brand["color_palette"]:
            # Determine text color based on brightness
            hex_clean = color.lstrip('#')
            r, g, b = int(hex_clean[0:2],16), int(hex_clean[2:4],16), int(hex_clean[4:6],16)
            text_color = "#ffffff" if (r*0.299 + g*0.587 + b*0.114) < 160 else "#000000"
            swatches_html += f'''
            <div style="flex:1;height:90px;border-radius:14px;background:{color};
                        display:flex;align-items:flex-end;justify-content:center;padding-bottom:10px;
                        position:relative;overflow:hidden;">
                <span style="font-size:0.75rem;font-weight:700;color:{text_color};letter-spacing:0.5px;
                            background:{text_color}15;padding:3px 10px;border-radius:8px;backdrop-filter:blur(4px);">
                    {color.upper()}
                </span>
            </div>'''
        swatches_html += '</div>'
        st.markdown(swatches_html, unsafe_allow_html=True)

        # Color list with circles
        for color in brand["color_palette"]:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid #1a1a3e;">
                <div style="width:36px;height:36px;border-radius:50%;background:{color};border:2px solid #2a2a5e;flex-shrink:0;"></div>
                <span style="color:#9999bb;font-size:0.9rem;font-weight:500;">{color.upper()}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Divider ──
    st.markdown('<div style="border-top:1px solid #1a1a3e;margin:8px 0 24px 0;"></div>', unsafe_allow_html=True)

    # ── Generated Taglines ──
    st.markdown(f"""
    <div class="dark-card">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
            <span style="font-size:1.05rem;font-weight:700;color:#e8e8ff;">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:8px;"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                Generated Taglines
            </span>
            <span style="color:#3a3a5e;cursor:pointer;">⋮</span>
        </div>
    """, unsafe_allow_html=True)

    tag_cols = st.columns(len(brand["taglines"]))
    for i, tagline in enumerate(brand["taglines"]):
        with tag_cols[i]:
            st.markdown(f"""
            <div style="background:#0a0a1a;border:1px solid #1a1a3e;border-left:3px solid #7c3aed;
                        border-radius:0 10px 10px 0;padding:16px 18px;">
                <div style="font-size:0.7rem;color:#5555aa;margin-bottom:6px;">✦ TAGLINE {i+1}</div>
                <span style="color:#e8e8ff;font-size:0.95rem;font-style:italic;">"{tagline}"</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Divider ──
    st.markdown('<div style="border-top:1px solid #1a1a3e;margin:8px 0 24px 0;"></div>', unsafe_allow_html=True)

    # ── Key Selling Points ──
    st.markdown(f"""
    <div class="dark-card">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
            <span style="font-size:1.05rem;font-weight:700;color:#e8e8ff;">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2dd4bf" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:8px;"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>
                Key Selling Points
            </span>
            <span style="color:#3a3a5e;cursor:pointer;">⋮</span>
        </div>
    """, unsafe_allow_html=True)

    sp_cols = st.columns(len(brand["selling_points"]))
    accent_colors = ["#7c3aed", "#2dd4bf", "#f59e0b", "#ec4899", "#6366f1"]
    for i, point in enumerate(brand["selling_points"]):
        c = accent_colors[i % len(accent_colors)]
        with sp_cols[i]:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg, {c}11, {c}08);
                        border:1px solid {c}33;border-radius:12px;padding:18px;text-align:center;
                        position:relative;">
                <div style="width:32px;height:32px;border-radius:8px;background:{c}22;
                            display:flex;align-items:center;justify-content:center;margin:0 auto 10px auto;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                </div>
                <span style="color:#d8d8f0;font-size:0.9rem;font-weight:600;line-height:1.4;">{point}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)