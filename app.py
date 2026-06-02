import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Настройка страницы и стилей
st.set_page_config(page_title="ИИ Решатель", page_icon="🤖", layout="centered")

# Кастомный CSS для красивого интерфейса (как у тебя и было)
st.markdown("""
    <style>
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        border-radius: 10px;
        width: 100%;
        font-size: 18px;
        font-weight: bold;
        border: none;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #4338ca;
        border: none;
    }
    </style>
""", unsafe_index=True)

# 2. Подключение нейросети через твои секреты (st.secrets)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Ошибка подключения API-ключа. Проверь Advanced Settings в Streamlit.")

# 3. Интерфейс приложения
st.write("### 🤖 Сделай фото через камеру или просто напиши текст, и ИИ решит твою задачу!")

# Поле для камеры
img_file = st.camera_input("Наведи камеру на задачу и сделай снимок")

# Поле для текста
user_text = st.text_input("Что нужно сделать?", placeholder="Напиши текст задачи или вопрос к фото сюда...")

# Кнопка запуска
if st.button("🚀 Решить задачу"):
    # Проверяем, передал ли пользователь хоть что-то
    if img_file is not None or user_text.strip() != "":
        with st.spinner("🔮 Нейросеть думает и генерирует ответ..."):
            try:
                # Сценарий 1: Отправляем И фото, И текст
                if img_file is not None and user_text.strip() != "":
                    img = Image.open(img_file)
                    response = model.generate_content([user_text, img])
                
                # Сценарий 2: Отправляем ТОЛЬКО фото
                elif img_file is not None:
                    img = Image.open(img_file)
                    response = model.generate_content(["Внимательно посмотри на фото и подробно реши/объясни то, что там изображено.", img])
                
                # Сценарий 3: Отправляем ТОЛЬКО текст
                else:
                    response = model.generate_content(user_text)
                
                # Вывод ответа на экран
                st.success("✨ Ответ готов!")
                st.markdown("---")
                st.write(response.text)
                st.markdown("---")
                
            except Exception as e:
                st.error(f"Произошла ошибка при обращении к ИИ: {e}")
    else:
        st.warning("⚠️ Пожалуйста, напиши текст задачи или сделай снимок экрана!")
