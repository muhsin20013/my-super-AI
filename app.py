import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Настройка страницы (Название вкладки и иконка мозга)
st.set_page_config(page_title="ИИ Помощник", page_icon="🧠", layout="centered")

# Кастомный CSS для тёмной темы и красивой кнопки
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

# 2. Подключение ИИ напрямую из скрытых настроек (Secrets)
# Здесь мы добавляем системную инструкцию, чтобы робот знал твоё имя!
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # ТУТ НАСТРОЙКА ИМЕНИ: Замени "Мухсин" на своё имя, если нужно!
    system_instruction = "Ты — продвинутый ИИ-помощник. Тебя зовут Мухсин. Твоя задача — помогать решать задачи и отвечать на вопросы."
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=system_instruction
    )
except Exception as e:
    st.error("Ошибка: Ключ не найден в настройках Secrets. Пропиши его в панели Manage app.")

# 3. Интерфейс для обычных пользователей (никаких полей для ключа!)
st.write("### 🧠 Твой умный ИИ-помощник")
st.write("Напиши текст или сделай снимок — я помогу тебе во всём разобраться!")

# Поля ввода
img_file = st.camera_input("📸 Сделать снимок задачи")
user_text = st.text_input("✍️ Твой вопрос или задание:", placeholder="Напиши сюда то, что нужно решить...")

# Кнопка запуска
if st.button("🧠 Запустить анализ"):
    if img_file is not None or user_text.strip() != "":
        with st.spinner("🔮 Нейроны ИИ обрабатывают запрос..."):
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
                st.error(f"Произошла ошибка: {e}")
    else:
        st.warning("⚠️ Пожалуйста, напиши текст или сделай снимок!")
