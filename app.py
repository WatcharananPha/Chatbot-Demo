import streamlit as st
from openai import OpenAI
import json
from datetime import datetime
import os

st.set_page_config(
    page_title="AI ผู้ช่วยด้านที่อยู่อาศัยและคอนโดมิเนียม",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    
    .user-message {
        background-color: #f0f2f6;
        margin-left: 2rem;
    }
    
    .assistant-message {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        margin-right: 2rem;
    }
    
    .message-header {
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #1f1f1f;
    }
    
    .message-content {
        line-height: 1.6;
        color: #2d2d2d;
    }
    
    .header-container {
        text-align: center;
        padding: 2rem 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 1rem;
        border-top: 1px solid #e0e0e0;
        z-index: 1000;
    }
    
    .chat-container {
        padding-bottom: 120px;
        max-height: 70vh;
        overflow-y: auto;
    }
    
    .sample-questions {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .sample-question-btn {
        background-color: #ffffff;
        border: 1px solid #d0d0d0;
        border-radius: 0.25rem;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        cursor: pointer;
        display: inline-block;
        font-size: 0.9rem;
    }
    
    .sample-question-btn:hover {
        background-color: #f0f2f6;
        border-color: #a0a0a0;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """คุณคือ AI ผู้ช่วยด้านที่อยู่อาศัยและคอนโดมิเนียม ที่มีความเชี่ยวชาญในการให้คำปรึกษาและคำแนะนำแก่ผู้อยู่อาศัย ผู้เช่า เจ้าของห้อง และผู้ที่เกี่ยวข้องกับโครงการที่อยู่อาศัยและคอนโดมิเนียม

            ความเชี่ยวชาญของคุณครอบคลุม:
            - สิทธิและหน้าที่ของผู้เช่าและเจ้าของห้อง
            - ข้อบังคับและระเบียบของนิติบุคคลอาคารชุด
            - การจัดการค่าส่วนกลางและค่าใช้จ่ายต่างๆ
            - ปัญหาเสียงรบกวนและการอยู่ร่วมกัน
            - การใช้สิ่งอำนวยความสะดวกส่วนกลาง
            - ข้อพิพาทระหว่างเพื่อนบ้านและวิธีการแก้ไข
            - ปัญหาการซ่อมแซมและบำรุงรักษา
            - ระบบรักษาความปลอดภัยและการเข้าออก
            - การจอดรถและการจราจรภายในโครงการ
            - ปัญหาสัตว์เลี้ยงในคอนโดมิเนียม
            - การปรับปรุงห้องและขออนุญาตต่างๆ
            - ข้อกำหนดการขายและการให้เช่า
            - การประชุมเจ้าของร่วมและสิทธิในการออกเสียง

            แนวทางในการตอบคำถาม:
            1. ให้คำแนะนำที่เป็นประโยชน์และเป็นไปได้จริงในทางปฏิบัติ
            2. อธิบายด้วยภาษาที่เข้าใจง่าย หลีกเลี่ยงศัพท์เทคนิคที่ซับซ้อน
            3. เน้นการแก้ไขปัญหาแบบสันติวิธีและการเจรจาก่อน
            4. ให้ขั้นตอนการดำเนินการที่ชัดเจนและเป็นระบบ
            5. แนะนำให้ตรวจสอบข้อบังคับของนิติบุคคลที่เกี่ยวข้อง
            6. แสดงความเข้าใจต่อปัญหาและความกังวลของผู้สอบถาม
            7. เสนอทางเลือกหลายแนวทางเมื่อเป็นไปได้
            8. แนะนำให้ปรึกษาผู้จัดการอาคารหรือคณะกรรมการฯ เมื่อจำเป็น
            9. ระบุเมื่อใดที่ควรขอความช่วยเหลือจากผู้เชี่ยวชาญเฉพาะด้าน
            10. ให้ข้อมูลที่เป็นปัจจุบันและเป็นประโยชน์ต่อการตัดสินใจ

            การสื่อสาร:
            - ใช้น้ำเสียงที่เป็นมิตรและให้กำลังใจ
            - แสดงความเอาใจใส่และความเข้าใจ
            - ถามคำถามเพิ่มเติมเมื่อต้องการข้อมูลเพิ่มเติม
            - ให้คำแนะนำที่สร้างสรรค์และเชิงบวก
            - หลีกเลี่ยงการตัดสินหรือลำเอียง

            หมายเหตุ: ให้คำแนะนำทั่วไปเท่านั้น สำหรับปัญหาทางกฎหมายที่ซับซ้อนควรปรึกษาผู้เชี่ยวชาญหรือทนายความ"""
        }
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "session_start" not in st.session_state:
    st.session_state.session_start = datetime.now()
    
@st.cache_resource
def get_openai_client():
    return OpenAI(
        api_key="sk-GqA4Uj6iZXaykbOzIlFGtmdJr6VqiX94NhhjPZaf81kylRzh",
        base_url="https://api.opentyphoon.ai/v1"
    )

client = get_openai_client()

st.markdown("""
<div class="header-container">
    <h1>🏠 AI ผู้ช่วยด้านที่อยู่อาศัยและคอนโดมิเนียม</h1>
    <p style="color: #666; font-size: 1.1rem;">ให้คำปรึกษาและคำแนะนำเกี่ยวกับการอยู่อาศัยในคอนโดมิเนียม</p>
</div>
""", unsafe_allow_html=True)

if len(st.session_state.chat_history) == 0:
    st.markdown("""
    <div class="sample-questions">
        <h3>💡 คำถามยอดนิยม</h3>
        <p>คลิกเพื่อเริ่มต้นการสนทนา:</p>
    </div>
    """, unsafe_allow_html=True)
    
    sample_questions = [
        "เพื่อนบ้านเปิดเพลงดังรบกวน ควรทำอย่างไร?",
        "ค่าส่วนกลางแพงเกินไป มีสิทธิ์ร้องเรียนไหม?",
        "อยากปรับปรุงห้อง ต้องขออนุญาตใครบ้าง?",
        "ปัญหาการจอดรถในคอนโด",
        "เพื่อนบ้านเลี้ยงสัตว์ผิดกฎ ควรแจ้งใคร?"
    ]
    
    cols = st.columns(2)
    for i, question in enumerate(sample_questions):
        with cols[i % 2]:
            if st.button(question, key=f"sample_{i}", use_container_width=True):
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": question,
                    "timestamp": datetime.now().isoformat()
                })
                
                st.session_state.messages.append({"role": "user", "content": question})
            
                with st.spinner("กำลังคิด..."):
                    try:
                        response = client.chat.completions.create(
                            model="typhoon-v2-70b-instruct",
                            messages=st.session_state.messages
                        )
                        
                        assistant_response = response.choices[0].message.content
                        
                        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": assistant_response,
                            "timestamp": datetime.now().isoformat()
                        })
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {str(e)}")

chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-header">👤 คุณ</div>
                <div class="message-content">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <div class="message-header">🏠 AI ผู้ช่วย</div>
                <div class="message-content">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "พิมพ์คำถามของคุณ...",
        placeholder="เช่น เพื่อนบ้านเปิดเพลงดัง ควรจะทำยังไงดี?",
        key="user_input"
    )

with col2:
    send_button = st.button("ส่ง", type="primary", use_container_width=True)

if (send_button and user_input) or (user_input and st.session_state.get("enter_pressed", False)):
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().isoformat()
    })
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("กำลังคิด..."):
        try:
            response = client.chat.completions.create(
                model="typhoon-v2-70b-instruct",
                messages=st.session_state.messages
            )
            
            assistant_response = response.choices[0].message.content
            
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": assistant_response,
                "timestamp": datetime.now().isoformat()
            })
            
            st.session_state.user_input = ""
            st.rerun()
            
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {str(e)}")
with st.sidebar:
    st.header("⚙️ ตัวเลือก")
    
    if st.button("🗑️ ล้างประวัติการสนทนา", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.messages = [st.session_state.messages[0]]
        st.session_state.session_start = datetime.now()
        st.rerun()
    
    if st.button("💾 บันทึกประวัติการสนทนา", use_container_width=True):
        chat_data = {
            "session_start": st.session_state.session_start.isoformat(),
            "session_end": datetime.now().isoformat(),
            "conversations": st.session_state.chat_history
        }
        
        json_str = json.dumps(chat_data, ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 ดาวน์โหลดไฟล์ JSON",
            data=json_str.encode('utf-8'),
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    st.markdown("---")
    st.markdown("### 📊 สถิติการสนทนา")
    st.write(f"**จำนวนข้อความ:** {len(st.session_state.chat_history)}")
    st.write(f"**เริ่มเซสชัน:** {st.session_state.session_start.strftime('%H:%M')}")
    
    st.markdown("---")
    st.markdown("### ℹ️ เกี่ยวกับ")
    st.markdown("""
    AI ผู้ช่วยนี้ให้คำปรึกษาเกี่ยวกับ:
    - ปัญหาเพื่อนบ้าน
    - ค่าส่วนกลาง
    - การซ่อมแซม
    - ระเบียบคอนโด
    - และอื่นๆ
    """)

st.markdown("""
---
<div style="text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;">
    💡 AI ให้คำแนะนำทั่วไป สำหรับปัญหาซับซ้อนควรปรึกษาผู้เชี่ยวชาญ
</div>
""", unsafe_allow_html=True)