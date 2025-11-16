import streamlit as st
from openai import OpenAI

def analyze(image, disease):
    disease = 2
    return disease
    #query for diseases
    #if healthy, disease = 1
    #if viral, disease = 2
    #if bacterial, disease = 3
    #if not a [thing], disease = 4

st.set_page_config(layout="wide", page_title="Disease Detection")
st.title("Disease Detection")

if "imageUploaded" not in st.session_state:
    st.session_state.imageUploaded = False
if "disease" not in st.session_state:
    st.session_state.disease = 0
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file" not in st.session_state:
    st.session_state.file = None

col1, col2, col3 = st.columns([0.25, 0.4, 0.35], gap="small", vertical_alignment="top", border=True, width="stretch")

with col1:
    st.write("# Upload Images 📷")
    upload = st.file_uploader("Select an image that resembles the sample", type=["png", "jpg", "jpeg"], accept_multiple_files=False)
    if (upload != None):
        st.session_state.file = upload
        if st.button("Analyze Image"):
            if st.session_state.file:
                st.session_state.imageUploaded = True
                st.session_state.disease = analyze(st.session_state.file, st.session_state.disease)
    
with col2:
    if (st.session_state.imageUploaded == False):
        st.write("# Sample Image")
        st.image("assets/kirby.jpg")
    else:
        st.write("# Uploaded Image")
        st.image(st.session_state.file)
    
with col3:
    match st.session_state.disease: 
        case 1:
            '''
                # HEALTHY
                #### This [thing] does not appear to have [thing]
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

    match st.session_state.disease: 
        case 1 | 2 | 3:
            '''
                ### Consider prompting the chat bot for additional resources!
            '''

            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("What can I help you with?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    stream = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    )
                    response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})