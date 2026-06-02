import streamlit as st
import google.generativeai as genai
from PIL import Image

# Настройка страницы приложения
st.set_page_config(page_title="Умный ИИ-Помощник", layout="centered")
st.title("📸 Моментальный ИИ-Помощник")
st.write("Сделай фото через камеру, и ИИ сразу решит твою задачу!")

# Твой личный ключ, который ты только что скопировал!
API_KEY = 'AIzaSyD3b5G3TEufAfto5GRIzBPNhninFZz7RI4' 
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

# Включаем камеру
img_file = st.camera_input("Наведи камеру на задачу и сделай снимок")
user_prompt = st.text_input("Что нужно сделать?", "Реши и объясни, что на фото.")

# Обработка фото
if img_file is not None:
    image = Image.open(img_file)
    st.image(image, caption="Фото загружено!", use_column_width=True)
    
    with st.spinner("🧠 ИИ думает..."):
        try:
            response = model.generate_content([user_prompt, image])
            st.success("Ответ ИИ:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Ошибка соединения с ИИ: {e}")
