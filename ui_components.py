import streamlit as st
from audio_recorder_streamlit import audio_recorder

def get_user_input():
    """
    Handle user input selection (Upload Audio, Record Audio, Upload Video).
    Initially shows only the radio selection (styled as cards) in one row;
    after a choice is made, it hides the selection and shows the corresponding uploader/recorder.
    
    Returns:
        tuple: (audio_data, video_data, selected_method)
            - audio_data (bytes or None): Audio file bytes if provided.
            - video_data (bytes or None): Video file bytes if provided.
            - selected_method (str or None): The input method selected by the user.
    """
    # Inject custom CSS for the radio buttons (styled as cards)
    # st.markdown("""
    # <style>
    # /* Container: display radio buttons in a row */
    # div[role="radiogroup"] {
    #     display: flex !important;
    #     justify-content: space-evenly;
    #     flex-direction: row; !important
    #     gap: 20px;
    # }
    # /* Style each radio button label as a card */
    # div[role="radiogroup"] > label {
    #     width: 190px;
    #     height: 254px;
    #     border-radius: 1rem;
    #     background-color: #4158D0;
    #     background-image: linear-gradient(43deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);
    #     box-shadow: rgba(0, 0, 0, 0.17) 0px -23px 25px 0px inset, 
    #                 rgba(0, 0, 0, 0.15) 0px -36px 30px 0px inset, 
    #                 rgba(0, 0, 0, 0.1) 0px -79px 40px 0px inset, 
    #                 rgba(0, 0, 0, 0.06) 0px 2px 1px, 
    #                 rgba(0, 0, 0, 0.09) 0px 4px 2px, 
    #                 rgba(0, 0, 0, 0.09) 0px 8px 4px, 
    #                 rgba(0, 0, 0, 0.09) 0px 16px 8px, 
    #                 rgba(0, 0, 0, 0.09) 0px 32px 16px;
    #     display: flex;
    #     align-items: center;
    #     justify-content: center;
    #     position: relative;
    #     overflow: hidden;
    #     cursor: pointer;
    #     margin:0;
    #     padding: 0;
    # }
    # /* Hide the default radio input */
    # div[role="radiogroup"] > label > input {
    #     display: none; !important
    # }
    # /* Style the text inside each card using the default text from the label */
    # div[role="radiogroup"] > label::after {
    #     content: attr(data-label);
    #     position: relative;
    #     z-index: 1;
    #     color: white;
    #     font-size: 2em;
    #     font-weight: bold;
    #     text-align: center;
    #     width: 100%;
    # }
    # </style>
    # """, unsafe_allow_html=True)
    
    # Use session state to track if a selection has already been made.
    if "selected_method" not in st.session_state:
        st.session_state.selected_method = None

    # If no selection is made, show the radio buttons.
    if st.session_state.selected_method is None:
        # Use st.radio to get the selection.
        # Note: We cannot directly add a data-label attribute with st.radio,
        # so we assume the radio button labels will be styled by our CSS.
        selected_method = st.radio(
            "Select Input Method",
            ("Upload Audio File", "Record Audio", "Upload Video File"),
            index=None  # No default selection
        )
        if selected_method:
            st.session_state.selected_method = selected_method
            st.rerun()  # Rerun to hide the radio selection.
    else:
        # If a selection is already made, show the corresponding uploader/recorder.
        audio_data = None
        video_data = None
        st.write(f"### You selected: **{st.session_state.selected_method}**")
        try:
            if st.session_state.selected_method == "Upload Audio File":
                uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "flac", "m4a"])
                if uploaded_file is not None:
                    audio_data = uploaded_file.read()
                    st.audio(audio_data, format="audio/wav")
            elif st.session_state.selected_method == "Record Audio":
                st.write("Record your audio:")
                audio_bytes = audio_recorder()
                if audio_bytes:
                    audio_data = audio_bytes
                    st.audio(audio_bytes, format="audio/wav")
            elif st.session_state.selected_method == "Upload Video File":
                uploaded_video = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])
                if uploaded_video:
                    video_data = uploaded_video.read()
            # Provide a reset button to allow re-selection
            if st.button("Change Selection"):
                st.session_state.selected_method = None
                st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {e}")
        return audio_data, video_data, st.session_state.selected_method
    return None, None, None
