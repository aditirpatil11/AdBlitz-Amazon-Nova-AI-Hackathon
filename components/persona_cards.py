import streamlit as st

ACCENT_COLORS = ["#7c3aed", "#2dd4bf", "#f59e0b"]


def render_persona_cards(personas):
    cols = st.columns(len(personas))
    for i, persona in enumerate(personas):
        color = ACCENT_COLORS[i % len(ACCENT_COLORS)]
        with cols[i]:
            # Header section
            vals = " · ".join(persona.get("values", []))
            income = persona.get("income", "N/A")
            st.markdown(f"""<div style="background:linear-gradient(135deg,{color}22,{color}08);border:1px solid #1a1a3e;border-radius:16px 16px 0 0;padding:20px;">
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
                    <div style="width:44px;height:44px;border-radius:12px;background:{color}33;border:2px solid {color};display:flex;align-items:center;justify-content:center;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/></svg>
                    </div>
                    <div>
                        <div style="font-size:1.15rem;font-weight:700;color:#e8e8ff;">{persona['name']}</div>
                        <div style="font-size:0.82rem;color:{color};">{persona['age']} · {persona['job']}</div>
                    </div>
                </div>
                <span style="background:{color}22;color:{color};padding:3px 10px;border-radius:6px;font-size:0.75rem;font-weight:600;">{income}</span>
                <span style="color:#9999bb;font-size:0.8rem;margin-left:8px;">{vals}</span>
            </div>""", unsafe_allow_html=True)

            # Pain points
            pp = persona.get("pain_points", [])
            pp_html = "".join([f'<div style="display:flex;align-items:flex-start;gap:8px;padding:3px 0;"><span style="color:{color};font-size:0.7rem;margin-top:3px;">●</span><span style="color:#8888aa;font-size:0.85rem;">{p}</span></div>' for p in pp])
            st.markdown(f"""<div style="background:#111128;border-left:1px solid #1a1a3e;border-right:1px solid #1a1a3e;padding:14px 20px;">
                <div style="font-size:0.7rem;color:{color};text-transform:uppercase;letter-spacing:1px;font-weight:600;margin-bottom:8px;">Pain Points</div>
                {pp_html}
            </div>""", unsafe_allow_html=True)

            # Buying triggers
            bt = persona.get("buying_triggers", [])
            bt_html = "".join([f'<span style="display:inline-block;padding:4px 12px;border-radius:20px;font-size:0.75rem;color:{color};border:1px solid {color}44;background:{color}11;margin:3px 4px 3px 0;">{t}</span>' for t in bt])
            st.markdown(f"""<div style="background:#111128;border-left:1px solid #1a1a3e;border-right:1px solid #1a1a3e;padding:10px 20px;">
                <div style="font-size:0.7rem;color:#5555aa;text-transform:uppercase;letter-spacing:1px;font-weight:600;margin-bottom:8px;">Buying Triggers</div>
                {bt_html}
            </div>""", unsafe_allow_html=True)

            # Footer
            top_plat = persona.get("platforms", ["N/A"])[0]
            discovery = persona.get("how_they_discover", "N/A")
            st.markdown(f"""<div style="background:#111128;border:1px solid #1a1a3e;border-radius:0 0 16px 16px;padding:14px 20px;border-top:1px solid #1a1a3e;">
                <div style="display:flex;gap:12px;">
                    <div style="flex:1;">
                        <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:1px;color:#5555aa;margin-bottom:4px;">Top Platform</div>
                        <div style="font-size:0.9rem;font-weight:700;color:#e8e8ff;">{top_plat}</div>
                    </div>
                    <div style="flex:1;">
                        <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:1px;color:#5555aa;margin-bottom:4px;">Discovery</div>
                        <div style="font-size:0.8rem;color:#9999bb;">{discovery}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)