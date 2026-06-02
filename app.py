import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Настройка страницы (Задаем название и иконку мозга 🧠 на вкладке)
st.set_page_config(page_title="Умный ИИ-Помощник", page_icon="🧠", layout="centered")

# Кастомный CSS для красивого тёмного интерфейса и синей кнопки
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
""", unsafe_allow_html=True)

# 2. Подключение нейросети напрямую через Секреты Streamlit
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Интерфейс самого приложения
st.write("### 🧠 Мой Кибер-Мозг")
st.write("Напиши мне вопрос или покажи задачу через камеру — я всё проанализирую!")

# Поле для камеры
img_file = st.camera_input("📸 Отправить снимок в ИИ")

# Поле для текста
user_text = st.text_input("✍️ Что нужно решить или объяснить?", placeholder="Введи текст или вопрос к фотографии...")

# Кнопка запуска
if st.button("🧠 Запустить анализ"):
    # Проверяем, передал ли пользователь хоть что-то (текст или фото)
    if img_file is not None or user_text.strip() != "":
        with st.spinner("🔮 Нейроны ИИ обрабатывают запрос..."):
            try:
                # Сценарий 1: Пользователь отправил И фото, И текст
                if img_file is not None and user_text.strip() != "":
                    img = Image.open(img_file)
                    response = model.generate_content([user_text, img])
                
                # Сценарий 2: Пользователь отправил ТОЛЬКО фото
                elif img_file is not None:
                    img = Image.open(img_file)
                    response = model.generate_content(["Внимательно посмотри на фото и подробно реши/объясни то, что там изображено.", img])
                
                # Сценарий 3: Пользователь написал ТОЛЬКО текст
                else:
                    response = model.generate_content(user_text)
                
                # Вывод успешного ответа на экран
                st.success("✨ Анализ завершен!")
                st.markdown("---")
                st.write(response.text)
                st.markdown("---")
                
            except Exception as e:
                st.error(f"Произошла ошибка при получении ответа от ИИ: {e}")
    else:
        st.warning("⚠️ Пожалуйста, напиши что-нибудь в поле или сделай снимок камеры!")
