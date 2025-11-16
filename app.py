import streamlit as st
from openai import OpenAI
import torch
from torchvision import models, transforms
from PIL import Image

def analyze(file, model, transform, classes, disease):
    img = Image.open(file).convert('RGB')
    img = transform(img).unsqueeze(0)
    with torch.no_grad():
        outputs = model(img)
        _, pred = torch.max(outputs, 1)
        prediction = classes[pred.item()]

    match prediction:
        case 'healthy':
            disease = 1
        case 'lumpy':
            disease = 2
        case 'foot-and-mouth':
            disease = 3

    return disease

st.set_page_config(page_title="Cattle Disease Detection", page_icon="https://cdn.pixabay.com/photo/2012/04/28/20/29/safety-44427_1280.png", layout="wide")
st.title("Cattle Disease Detection")

if "model" not in st.session_state:
    st.session_state.model = models.resnet50(weights=None)
    num_ftrs = st.session_state.model.fc.in_features
    st.session_state.model.fc = torch.nn.Linear(num_ftrs, 3)  # 3 classes
    st.session_state.model.load_state_dict(torch.load("model.pth", map_location='cpu'))
    st.session_state.model.eval()
if "transform" not in st.session_state:
    st.session_state.transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])
if "classes" not in st.session_state:
    st.session_state.classes = ['foot-and-mouth', 'healthy', 'lumpy']
if "imageUploaded" not in st.session_state:
    st.session_state.imageUploaded = False
if "disease" not in st.session_state:
    st.session_state.disease = 0
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-5-nano"
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
        if st.button("Analyze image"):
            if st.session_state.file:
                st.session_state.imageUploaded = True
                st.session_state.disease = analyze(st.session_state.file, st.session_state.model, st.session_state.transform, st.session_state.classes, st.session_state.disease)
    
with col2:
    if (st.session_state.imageUploaded == False):
        st.write("# Sample Image")
        st.image("https://cdn.britannica.com/55/174255-050-526314B6/brown-Guernsey-cow.jpg")
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
                # Lumpy Skin Disease (LSD) 🦠
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
                # Foot and Mouth Disease (FAM) 🦠
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
        case _:
            st.write("# Diagnosis")

    match st.session_state.disease: 
        case 1 | 2 | 3:
            '''
                ### Consider prompting the chat bot for additional resources and feedback!
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