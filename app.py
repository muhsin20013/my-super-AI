import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Настройка страницы
st.set_page_config(page_title="ИИ Помощник", page_icon="🧠", layout="centered")

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

# 2. Подключение ИИ напрямую из Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Системная инструкция: робот знает твоё имя!
    system_instruction = "Ты — продвинутый ИИ-помощник, созданный разработчиком по имени Мухсин. Ты должен помогать пользователям решать любые задачи и называть себя помощником Мухсина."
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=system_instruction
    )
except Exception as e:
    st.error("Ошибка подключения. Проверь вкладку Secrets в настройках Streamlit!")

# 3. Чистый интерфейс (без полей для ввода ключей на экране)
st.write("### 🧠 Личный ИИ-помощник")
st.write("Напиши свой вопрос или покажи задачу через камеру — я всё решу!")

# Поля ввода
img_file = st.camera_input("📸 Сделать снимок задачи")
user_text = st.text_input("✍️ Твой вопрос или задание:", placeholder="Напиши сюда то, что нужно решить...")

# Кнопка запуска
if st.button("🧠 Запустить анализ"):
    if img_file is not None or user_text.strip() != "":
        with st.spinner("🔮 Нейроны ИИ обрабатывают запрос..."):
            try:
                if img_file is not None and user_text.strip() != "":
                    img = Image.open(img_file)
                    response = model.generate_content([user_text, img])
                elif img_file is not None:
                    img = Image.open(img_file)
                    response = model.generate_content(["Внимательно посмотри на фото и подробно реши/объясни то, что там изображено.", img])
                else:
                    response = model.generate_content(user_text)
                
                st.success("✨ Ответ готов!")
                st.markdown("---")
                st.write(response.text)
                st.markdown("---")
                
            except Exception as e:
                st.error(f"Произошла ошибка при обращении к ИИ: {e}")
    else:
        st.warning("⚠️ Пожалуйста, напиши текст или сделай снимок задачи!")
