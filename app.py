import streamlit as st
from openai import OpenAI

def analyze(uploaded_image, disease):
    disease = 2
    return disease
    #query for diseases
    #if healthy, disease = 1
    #if viral, disease = 2
    #if bacterial, disease = 3
    #if not a [thing], disease = 4

st.set_page_config(layout="wide", page_title="Disease Detection")
st.title("Disease Detection")

imageUploaded = False
disease = 0

col1, col2, col3 = st.columns([0.25, 0.4, 0.35], gap="small", vertical_alignment="top", border=True, width="stretch")

with col1:
    st.write("# Upload images 📷")
    upload = st.file_uploader("Select an image that resembles the sample", type=["png", "jpg", "jpeg"], accept_multiple_files=False)
    if (upload != None):
        if st.button("Analyze image"):
            imageUploaded = True
            col2.write("# Uploaded image")
            col2.image(upload)
            disease = analyze(upload, disease)
    
with col2:
    if (imageUploaded == False):
        st.write("# Sample image")
        st.image("assets/kirby.jpg")
    
with col3:
    match disease: 
        case 1:
            '''
                # HEALTHY
                #### This [thing] does not appear to have a skin infection
            '''
        case 2:
            '''
                # ILLNESS 1
                ### Learn more: [USDA article](https://www.usda.gov/)
                ### Symptoms
                * A
                * B
                * C
                ### Treatment
                * A
                * B
                * C
                ### Prevention
                * A
                * B
                * C
            '''
        case 3:
            '''
                # ILLNESS 2
                ### Learn more: [USDA article](https://www.usda.gov/)
                ### Symptoms
                * A
                * B
                * C
                ### Treatment
                * A
                * B
                * C
                ### Prevention
                * A
                * B
                * C
            '''
        case 4:
            st.write("## Error: The model does not recognize a [thing] in the uploaded image")
        case _:
            st.write("# Diagnosis")

    match disease: 
        case 1 | 2 | 3:
            with st.expander("Additional Information", expanded=False, icon=None, width="stretch"):
                #Chatbot
                st.write("# Diagnosis")
