import streamlit as st


def render_refine_bar(on_refine):
    st.markdown("**Not happy with something?** Describe what to change and only the affected parts will regenerate.")

    col1, col2 = st.columns([4, 1])
    with col1:
        feedback = st.text_input(
            "Feedback",
            placeholder="e.g. Make the copy more playful, target younger audience, use warmer colors...",
            label_visibility="collapsed"
        )
    with col2:
        regenerate = st.button("Regenerate", type="primary", use_container_width=True)

    if regenerate:
        if feedback.strip():
            on_refine(feedback)
        else:
            st.warning("Please describe what you'd like to change.")