import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# OCR reader (bg + en)
reader = easyocr.Reader(['bg', 'en'])

# Вредни съставки (можеш да разшириш)
harmful_ingredients = [
    "e621", "monosodium glutamate", "msg",
    "palm oil", "palm fat", "palmitate",
    "e102", "e110", "e124", "e129",
    "аскорбинова киселина",  # пример
    "палмово масло", "глутамат"
]

# Преводи
translations = {
    "bg": {
        "title": "📷 Разпознаване на съставки",
        "upload": "Качи снимка",
        "result": "Разпознат текст",
        "harmful": "⚠️ Намерени вредни съставки",
        "none": "✅ Не са открити вредни съставки"
    },
    "en": {
        "title": "📷 Ingredient Scanner",
        "upload": "Upload image",
        "result": "Recognized text",
        "harmful": "⚠️ Harmful ingredients found",
        "none": "✅ No harmful ingredients found"
    }
}

# Избор на език
lang = st.selectbox("Language / Език", ["bg", "en"])
t = translations[lang]

st.title(t["title"])

uploaded_file = st.file_uploader(t["upload"], type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # OCR
    with st.spinner("Processing..."):
        img_array = np.array(image)
        results = reader.readtext(img_array, detail=0)

    extracted_text = " ".join(results).lower()

    st.subheader(t["result"])
    st.write(extracted_text)

    # Търсене на вредни съставки
    found = [item for item in harmful_ingredients if item in extracted_text]

    if found:
        st.subheader(t["harmful"])
        for f in found:
            st.write(f"❌ {f}")
    else:
        st.subheader(t["none"])
