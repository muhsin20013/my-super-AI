import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Настройка страницы (Название и иконка мозга 🧠 на вкладке)
st.set_page_config(page_title="Умный ИИ-Помощник", page_icon="🧠", layout="centered")

# Кастомный CSS для тёмной темы
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

# 2. Безопасное подключение ключа
api_key = None

# Сначала пытаемся взять ключ из скрытых настроек (Secrets)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

# Интерфейс приложения
st.write("### 🧠 Мой Кибер-Мозг")
st.write("Напиши мне вопрос или покажи задачу через камеру — я всё проанализирую!")

# Если ключа нет в настройках, просим ввести его прямо на сайте
if not api_key:
    st.info("🔑 Ключ не найден в настройках Streamlit. Ты можешь временно ввести его ниже:")
    api_key = st.text_input("Вставь свой GEMINI_API_KEY сюда:", type="password")

# Поля для ввода задачи
img_file = st.camera_input("📸 Отправить снимок в ИИ")
user_text = st.text_input("✍️ Что нужно решить или объяснить?", placeholder="Введи текст или вопрос к фотографии...")

# Кнопка запуска
if st.button("🧠 Запустить анализ"):
    if not api_key:
        st.error("❌ Без API-ключа нейросеть не сможет ответить. Пожалуйста, введи ключ!")
    elif img_file is not None or user_text.strip() != "":
        with st.spinner("🔮 Нейроны ИИ обрабатывают запрос..."):
            try:
                # Настраиваем модель прямо перед запуском
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Сценарий 1: И фото, И текст
                if img_file is not None and user_text.strip() != "":
                    img = Image.open(img_file)
                    response = model.generate_content([user_text, img])
                
                # Сценарий 2: ТОЛЬКО фото
                elif img_file is not None:
                    img = Image.open(img_file)
                    response = model.generate_content(["Внимательно посмотри на фото и подробно реши/объясни то, что там изображено.", img])
                
                # Сценарий 3: ТОЛЬКО текст
                else:
                    response = model.generate_content(user_text)
                
                # Вывод ответа
                st.success("✨ Анализ завершен!")
                st.markdown("---")
                st.write(response.text)
                st.markdown("---")
                
            except Exception as e:
                st.error(f"Произошла ошибка при получении ответа от ИИ: {e}")
    else:
        st.warning("⚠️ Пожалуйста, напиши что-нибудь в поле или сделай снимок камеры!")
