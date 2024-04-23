import base64
import google.generativeai as genai
import streamlit as st
import os
import time
import PIL.Image

GOOGLE_API_KEY=st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)


def app():

    model = genai.GenerativeModel(
        "gemini-pro-vision",
    )


    # Create two columns
    col1, col2 = st.columns([1, 4])

    # Display the image in the left column
    with col1:
        st.image("wvsu-logo.jpg")

    # Display the title in the right column
    with col2:
        st.title("Automated Essay Scoring System using Gemini on Google AI Studio")

    text = """Prof. Louie F. Cervantes, M. Eng. (Information Engineering) \n
    CCS 229 - Intelligent Systems
    Department of Computer Science
    College of Information and Communications Technology
    West Visayas State University
    """
    with st.expander("Click to display developer information."):
        st.text(text)
        link_text = "Click here to visit [Gemini 1.5 Pro](https://developers.googleblog.com/2024/04/gemini-15-pro-in-public-preview-with-new-features.html)"
        st.write(link_text)
        link_text = "Click here to visit [Gemini Vertex AI](https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform)"
        st.write(link_text)
    
    st.subheader("Score Handwritten Essays Quickly and Easily")
    text = """This app streamlines the process of scoring your students' handwritten essays. Here's how to get started:
    \n1. Capture a Clear Photo: Ensure good lighting and hold your camera
    steady to take a sharp photo of the handwritten essay.
    \n2. Upload the Image: Select the photo you just captured from your 
    device's gallery.
    \n3. Provide Context: Enter the essay prompt or question that the 
    students were responding to.
    \n4. Upload or paste the scoring rubric you'll be using to evaluate 
    the essays.
    \nGet Instant Scores: Click "Score Essay" to receive an automated 
    assessment based on your chosen rubric."""
    st.write(text)

    # Create a file uploader widget
    uploaded_file = st.sidebar.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        image = PIL.Image.open(uploaded_file)
        question = st.text_area("Enter the essay question:")
        scoring_rubric = st.text_area("Enter the scoring rubric:")
    
        prompt = """You are a language teacher. The essay question is
        {question} Use the scoring rubric: {scoring_rubric} Score the essay 
        response found in this image out of a perfect score of 100. 
        Point out significant errors. Provide feedback and suggestions for improvement."""

    # Button to generate response
    if st.button("Score Essay"):
        progress_bar = st.progress(0, text="The AI teacher co-pilot is processing the request, please wait...")
       

        # Generate response from emini
        bot_response = model.generate_content([prompt, image])

        # Access the content of the response text
        bot_response = bot_response.text
        st.write(f"Gemini: {bot_response}")

        # update the progress bar
        for i in range(100):
            # Update progress bar value
            progress_bar.progress(i + 1)
            # Simulate some time-consuming task (e.g., sleep)
            time.sleep(0.01)
        # Progress bar reaches 100% after the loop completes
        st.success("AI teacher co-pilot task completed!") 

#run the app
if __name__ == "__main__":
  app()
