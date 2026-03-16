import streamlit as st

PLATFORM_COLORS = {
    "instagram": "#ec4899", "tiktok": "#3b82f6", "google": "#f59e0b",
    "facebook": "#3b82f6", "email": "#2dd4bf",
}
DAY_PHASES = {
    1: ("#2dd4bf", "Launch"), 2: ("#2dd4bf", "Launch"),
    3: ("#a78bfa", "Optimize"), 4: ("#a78bfa", "Optimize"),
    5: ("#f59e0b", "Scale"), 6: ("#f59e0b", "Scale"),
    7: ("#ec4899", "Review"),
}


def render_media_plan(media_plan):
    budget = media_plan.get("budget_split", {})
    calendar = media_plan.get("seven_day_calendar", [])
    ab_tests = media_plan.get("ab_tests", [])
    daily_budget = media_plan.get("daily_budget_recommendation", "—")

    # ── Top metrics ──
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px;">
        <div class="dark-card" style="margin-bottom:0;text-align:center;">
            <div style="font-size:1.5rem;font-weight:800;color:#e8e8ff;">{daily_budget}</div>
            <div style="font-size:0.75rem;color:#5555aa;">Daily Budget</div>
        </div>
        <div class="dark-card" style="margin-bottom:0;text-align:center;">
            <div style="font-size:1.5rem;font-weight:800;color:#e8e8ff;">7</div>
            <div style="font-size:0.75rem;color:#5555aa;">Day Campaign</div>
        </div>
        <div class="dark-card" style="margin-bottom:0;text-align:center;">
            <div style="font-size:1.5rem;font-weight:800;color:#e8e8ff;">{len(budget)}</div>
            <div style="font-size:0.75rem;color:#5555aa;">Platforms</div>
        </div>
        <div class="dark-card" style="margin-bottom:0;text-align:center;">
            <div style="font-size:1.5rem;font-weight:800;color:#e8e8ff;">{len(ab_tests)}</div>
            <div style="font-size:0.75rem;color:#5555aa;">A/B Tests</div>
        </div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    # ── LEFT COLUMN: Roadmap + A/B Tests ──
    with col1:
        st.markdown('<div class="dark-card" style="padding-bottom:8px;"><div style="display:flex;justify-content:space-between;align-items:center;"><span style="font-size:1.05rem;font-weight:700;color:#e8e8ff;">7-Day Launch Roadmap</span><span style="background:rgba(124,58,237,0.15);color:#a78bfa;padding:4px 12px;border-radius:8px;font-size:0.75rem;font-weight:600;">4 PHASES</span></div></div>', unsafe_allow_html=True)
        for i, item in enumerate(calendar):
            day = item.get("day", i + 1)
            action = item.get("action", "")
            platform = item.get("platform", "")
            budget_info = item.get("budget", "")
            pc, pl = DAY_PHASES.get(day, ("#7c3aed", "Active"))
            status = "Active" if day == 1 else "Ready" if day <= 2 else "Pending"
            sc = "#2dd4bf" if day == 1 else pc if day <= 2 else "#5555aa"
            st.markdown(f'<div style="display:flex;align-items:flex-start;gap:16px;padding:10px 16px;border-bottom:1px solid #1a1a3e;background:#111128;"><div style="width:32px;height:32px;border-radius:50%;background:{pc}22;border:2px solid {pc};display:flex;align-items:center;justify-content:center;color:{pc};font-weight:700;font-size:0.8rem;flex-shrink:0;">{day}</div><div style="flex:1;"><div style="display:flex;justify-content:space-between;align-items:center;"><span style="color:#e8e8ff;font-weight:600;font-size:0.9rem;">Day {day}: {action}</span><span style="color:{sc};font-size:0.7rem;font-weight:600;background:{sc}15;padding:3px 10px;border-radius:6px;">{status}</span></div><div style="display:flex;align-items:center;gap:8px;margin-top:4px;"><span style="color:#5555aa;font-size:0.8rem;">{platform}</span><span style="color:#5555aa;font-size:0.8rem;">{budget_info}</span><span style="color:{pc};font-size:0.7rem;font-weight:600;">{pl}</span></div></div></div>', unsafe_allow_html=True)

        # A/B Tests in left column
        st.markdown(f'<div class="dark-card" style="padding-bottom:8px;margin-top:16px;"><span style="font-size:1.05rem;font-weight:700;color:#e8e8ff;">A/B Tests</span> <span style="background:rgba(245,158,11,0.15);color:#f59e0b;padding:4px 12px;border-radius:8px;font-size:0.75rem;font-weight:600;margin-left:8px;">{len(ab_tests)} TESTS</span></div>', unsafe_allow_html=True)
        for ab in ab_tests:
            st.markdown(f'<div style="background:#0a0a1a;border:1px solid #1a1a3e;border-radius:10px;padding:12px;margin-bottom:8px;"><div style="font-weight:700;color:#e8e8ff;font-size:0.85rem;margin-bottom:8px;">{ab["test"]}</div><div style="display:flex;align-items:center;gap:6px;"><span style="background:rgba(124,58,237,0.13);color:#a78bfa;padding:3px 10px;border-radius:6px;font-size:0.75rem;">A: {ab["variant_a"]}</span><span style="color:#5555aa;font-size:0.65rem;font-weight:800;">VS</span><span style="background:rgba(236,72,153,0.13);color:#ec4899;padding:3px 10px;border-radius:6px;font-size:0.75rem;">B: {ab["variant_b"]}</span></div><div style="color:#5555aa;font-size:0.75rem;margin-top:6px;">{ab["metric"]} · {ab.get("duration","")}</div></div>', unsafe_allow_html=True)

    # ── RIGHT COLUMN: Budget + Platform Strategy ──
    with col2:
        st.markdown('<div class="dark-card" style="padding-bottom:8px;"><span style="font-size:1.05rem;font-weight:700;color:#e8e8ff;">Budget Breakdown</span></div>', unsafe_allow_html=True)
        if daily_budget and daily_budget != "—":
            st.markdown(f'<div style="text-align:center;margin-bottom:16px;padding:14px;background:#0a0a1a;border:1px solid #1a1a3e;border-radius:12px;"><div style="font-size:1.8rem;font-weight:800;color:#e8e8ff;">{daily_budget}</div><div style="font-size:0.8rem;color:#5555aa;">Recommended daily budget</div></div>', unsafe_allow_html=True)
        for platform, pct in budget.items():
            bc = PLATFORM_COLORS.get(platform.lower(), "#7c3aed")
            st.markdown(f'<div style="margin-bottom:14px;"><div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;"><span style="color:#9999bb;font-size:0.85rem;text-transform:capitalize;">{platform}</span><span style="color:#e8e8ff;font-weight:700;">{pct}%</span></div><div style="background:#0a0a1a;border-radius:6px;height:8px;overflow:hidden;"><div style="width:{pct}%;background:{bc};height:100%;border-radius:6px;"></div></div></div>', unsafe_allow_html=True)

        st.markdown('<div class="dark-card" style="padding-bottom:8px;margin-top:16px;"><span style="font-size:1.05rem;font-weight:700;color:#e8e8ff;">Platform Strategy</span></div>', unsafe_allow_html=True)
        for p in media_plan.get("platform_strategy", []):
            pn = p["platform"].lower()
            pc = PLATFORM_COLORS.get(pn, "#7c3aed")
            cr = " · ".join(p.get("creatives", []))
            st.markdown(f'<div style="background:#0a0a1a;border:1px solid #1a1a3e;border-left:3px solid {pc};border-radius:0 10px 10px 0;padding:12px;margin-bottom:8px;"><div style="font-weight:700;color:#e8e8ff;font-size:0.9rem;">{p["platform"]}</div><div style="color:#7777aa;font-size:0.8rem;margin-top:4px;">{p["targeting"]}</div><div style="color:{pc};font-size:0.75rem;margin-top:4px;">{cr}</div></div>', unsafe_allow_html=True)