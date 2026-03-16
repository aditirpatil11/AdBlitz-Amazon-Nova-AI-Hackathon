import streamlit as st


def render_upload(on_generate):
    col1, col2 = st.columns([1, 1])

    with col1:
        input_method = st.radio(
            "How do you want to add your product photo?",
            ["Upload a file", "Take a photo"],
            horizontal=True
        )

        uploaded_file = None

        if input_method == "Upload a file":
            uploaded_file = st.file_uploader(
                "Product photo",
                type=["png", "jpg", "jpeg"],
                label_visibility="collapsed"
            )
        else:
            uploaded_file = st.camera_input("Take a photo of your product")

        if uploaded_file:
            st.image(uploaded_file, caption="Your product", use_container_width=True)

    with col2:
        if uploaded_file:
            st.markdown("""
            **Your campaign will include:**
            
            - Brand identity and positioning
            - Ad copy for 5 platforms
            - AI-generated ad images
            - Video ad with voiceover
            - 3 audience personas
            - 7-day media launch plan
            """)

            if st.button("Generate Campaign", type="primary", use_container_width=True):
                on_generate(uploaded_file)
        else:
            st.markdown("""
            **Upload a product photo to get started.**
            
            Supported formats: PNG, JPG, JPEG  
            Best results with clear, well-lit photos.
            """)

    return uploaded_file