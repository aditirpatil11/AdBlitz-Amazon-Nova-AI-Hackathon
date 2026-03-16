import streamlit as st


def render_image_gallery(images):
    valid = [img for img in images if img.get("url")]

    if not valid:
        st.warning("No images were generated successfully.")
        return

    cols = st.columns(3)
    for i, img in enumerate(valid):
        with cols[i % 3]:
            label = img["format"].replace("_", " ").upper()
            platform = img.get("platform", "").upper()
            badge_color = {
                "LIFESTYLE": "#7c3aed",
                "HERO": "#ec4899",
                "CAROUSEL": "#2dd4bf",
                "STORY": "#f59e0b",
            }.get(label, "#7c3aed")

            st.markdown(f"""
            <div style="background:#111128;border:1px solid #1a1a3e;border-radius:16px;
                        overflow:hidden;margin-bottom:16px;">
                <div style="position:relative;">
                    <img src="{img['url']}" style="width:100%;display:block;border-radius:16px 16px 0 0;" />
                    <div style="position:absolute;top:12px;left:12px;">
                        <span style="background:{badge_color};color:white;padding:4px 12px;
                                     border-radius:6px;font-size:0.7rem;font-weight:700;
                                     text-transform:uppercase;letter-spacing:1px;">
                            {label}
                        </span>
                    </div>
                </div>
                <div style="padding:12px 16px;">
                    <p style="color:#8888aa;font-size:0.8rem;margin:0;">{img.get('description', '')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)