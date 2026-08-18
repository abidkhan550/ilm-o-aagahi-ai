import os
import base64
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

# ۱. لوکل تصویر پڑھنے کا فنکشن
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return None

# تصویر کا پاتھ لوڈ کرنا
img_base64 = get_base64_image("my_pic.jpg")

# ۲. CSS اسٹائلنگ
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Great+Vibes&family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #1c1c24 100%);
        background-attachment: fixed;
        font-family: 'Montserrat', 'Noto Nastaliq Urdu', sans-serif;
    }
    
    /* تمام ٹیبز کا متن سفید رکھیں (غیر منتخب) */
    .stTabs [data-baseweb="tab"] p {
        color: #ffffff !important;
        font-weight: normal !important;
        font-size: 15px !important;
        opacity: 0.8 !important;
    }
    
    /* صرف منتخب (Active) ٹیب کا متن گہرا نیلا کریں */
    .stTabs [data-baseweb="tab"][aria-selected="true"] p {
        color: #1e88e5 !important;
        font-weight: bold !important;
        font-size: 16px !important;
        opacity: 1.0 !important;
    }
    
    /* Upload / Camera والی پوری لائن پر سیاہ بارڈر */
    .stExpander > summary {
        border: 2px solid #000000 !important;
        border-radius: 10px !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
    }

    /* ٹاپ کارنر میں لینگویج ڈراپ ڈاؤن */
    div[data-testid="stSelectbox"] {
        width: 150px !important;
        float: right;
        margin-top: -10px;
    }
    div[data-testid="stSelectbox"] label {
        display: none !important;
    }
    div[data-testid="stSelectbox"] > div {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 20px !important;
        font-size: 14px !important;
        color: #000 !important;
        border: 1px solid #1e88e5 !important;
    }

    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        background: rgba(255, 255, 255, 0.95);
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0px 8px 32px rgba(0, 0, 0, 0.3);
        margin-top: 15px;
        margin-bottom: 25px;
    }
    .profile-img {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #1e88e5;
    }
    
    .web-title {
        margin: 0;
        font-weight: 900 !important;
        font-size: 32px !important;
        font-family: 'Montserrat', sans-serif !important;
        background: linear-gradient(135deg, #0d47a1 0%, #00d2ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
    }
    
    .signature-text {
        margin: 0;
        color: #1e88e5 !important;
        font-size: 32px !important;
        font-family: 'Great Vibes', cursive !important;
        font-weight: normal !important;
        margin-top: -5px;
    }

    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #111111 !important;
        border-radius: 14px !important;
        border: 2px solid #1e88e5 !important;
        font-size: 19px !important;
        font-weight: 500 !important;
        font-family: 'Montserrat', 'Noto Nastaliq Urdu', sans-serif !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #777777 !important;
        font-size: 18px !important;
    }
    
    .stExpander {
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        margin-bottom: 10px !important;
    }
    .stExpander summary p {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #1e88e5 0%, #1565c0 100%);
        color: white !important;
        font-weight: bold;
        font-size: 18px;
        border-radius: 12px;
        padding: 12px;
        border: none;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ۳. کارنر میں زبان کا انتخاب
col_head1, col_head2 = st.columns([3, 1])
with col_head2:
    target_language = st.selectbox(
        "Language",
        ["English", "Urdu (اردو)", "Pashto (پښتو)", "Arabic (العربية)", "Hindi (हिंदी)", "Spanish", "French"]
    )

# ۴. ہیڈر
if img_base64:
    img_html = f'<img src="data:image/jpeg;base64,{img_base64}" class="profile-img">'
else:
    img_html = '<div style="font-size: 50px;">🎓</div>'

st.markdown(f"""
    <div class="header-container">
        {img_html}
        <div style="text-align: left;">
            <h1 class="web-title">Ilm-o-Aagahi AI</h1>
            <p class="signature-text">By Abid</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# ۵. API Key اور AI سیشن
API_KEY = st.secrets["API_KEY"]
client = genai.Client(api_key=API_KEY)

# ۶. Attachment Options
uploaded_image = None
camera_image = None

with st.expander("📎 Add Image / Camera Option (تصویر یا کیمرا)", expanded=False):
    tab1, tab2 = st.tabs(["📁 Upload Image", "📷 Take Photo"])
    
    with tab1:
        file_input = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        if file_input:
            uploaded_image = Image.open(file_input)
            st.image(uploaded_image, caption="Selected Image", width=180)
            
    with tab2:
        cam_input = st.camera_input("Take Picture", label_visibility="collapsed")
        if cam_input:
            camera_image = Image.open(cam_input)

# تصویر کا تعین
final_image = camera_image if camera_image else uploaded_image

# Main Search Input Bar
user_text = st.text_area("Ask Ilm-o-Aagahi AI...", height=100, placeholder="Ask anything or attach media...", label_visibility="collapsed")

# 🚀 Ask Button
if st.button("🚀 Ask / جواب حاصل کریں"):
    if user_text or final_image:
        with st.spinner("Processing..."):
            contents_list = []
            if final_image:
                contents_list.append(final_image)
            if user_text:
                contents_list.append(user_text)
            elif final_image and not user_text:
                contents_list.append(f"Please read all educational content in this image and explain/solve it thoroughly in {target_language}.")

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents_list,
                    config=types.GenerateContentConfig(
                        system_instruction=f"You are an expert AI educational tutor named Abid working for 'Ilm-o-Aagahi AI'. Strictly respond in {target_language}. Explain step-by-step.",
                    ),
                )
                st.success("Answer / جواب:")
                
                # انکوڈنگ کے مسئلے سے بچنے کے لیے محفوظ طریقہ
                answer_text = response.text if hasattr(response, 'text') else str(response)
                st.markdown(answer_text)
                
            except Exception as e:
                # اگر پھر بھی کوئی مسئلہ آئے تو اسے UTF-8 میں انکوڈ کر کے دکھائیں
                try:
                    safe_error = str(e).encode('utf-8', errors='ignore').decode('utf-8')
                    st.error(f"An error occurred: {safe_error}")
                except:
                    st.error("An unexpected error occurred.")
    else:
        st.warning("Please enter a question or attach an image first!")
