import streamlit as st
from openai import OpenAI
import json
from datetime import datetime
import os
import time

st.set_page_config(
    page_title="Chatbot DEMO",
    page_icon="https://www.freeiconspng.com/uploads/apartment-icon-7.gif",
    layout="centered"
)

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
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-bottom: 20px;
}

.chat-message {
    display: flex;
    flex-direction: column;
    max-width: 80%;
    padding: 10px 15px;
    border-radius: 18px;
    margin: 5px 0;
}

.user-message {
    align-self: flex-end;
    background-color: #f0f2f5;
    color: #000;
}

.assistant-message {
    align-self: flex-start;
    background-color: #f0f2f5;
    color: #000;
}

.message-content {
    font-size: 16px;
    line-height: 1.4;
}

.user-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #673ab7;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-left: auto;
    margin-right: 8px;
}

.assistant-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #e50695;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-right: 8px;
}

.message-row {
    display: flex;
    align-items: flex-start;
    margin-bottom: 12px;
}

.sample-questions button {
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container" style="text-align: center;">
    <img src="https://www.freeiconspng.com/uploads/apartment-icon-7.gif" width="250" height="250" style="margin-bottom: 10px;">
    <h1>Chatbot สำนักงานนิติบุคคล</h1>
    <p style="color: #666; font-size: 1.1rem;">ให้คำปรึกษาและคำแนะนำเกี่ยวกับการอยู่อาศัยของลูกบ้าน</p>
</div>
""", unsafe_allow_html=True)

if len(st.session_state.chat_history) == 0:
    st.markdown("""
    <div class="sample-questions">
        <p>คลิกเพื่อเริ่มต้นการสนทนา:</p>
    </div>
    """, unsafe_allow_html=True)
    
    sample_questions = [
        "เพื่อนบ้านเปิดเพลงดังรบกวน ควรทำอย่างไร?",
        "ค่าส่วนกลางแพงเกินไป มีสิทธิ์ร้องเรียนไหม?",
        "อยากปรับปรุงห้อง ต้องขออนุญาตใครบ้าง?",
        "ปัญหาการจอดรถในคอนโด",
        "เพื่อนบ้านเลี้ยงสัตว์ผิดกฎ ควรแจ้งใคร?",
        "ติดต่อรับพัสดุที่สำนักงานนิติบุคคล",
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
            
                # Removed spinner - process directly
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

chat_container = st.container()
with chat_container:
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="message-row">
                <div style="flex-grow: 1;"></div>
                <div class="chat-message user-message">
                    {message["content"]}
                </div>
                <div class="user-avatar">KA</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-row">
                <div class="assistant-avatar">AI</div>
                <div class="chat-message assistant-message">
                    {message["content"]}
                </div>
                <div style="flex-grow: 1;"></div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<style>
.stButton > button {
    height: 2.5rem;
    width: 100%;
}
.stTextInput > div > div > input {
    height: 2.5rem;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "พิมพ์คำถามของคุณ...",
        placeholder="พิมพ์คำถามของคุณ...",
        key="user_input",
        label_visibility="collapsed"
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
    
    # Removed spinner - process directly
    response = client.chat.completions.create(
        model="typhoon-v2-70b-instruct",
        messages=st.session_state.messages
    )
    
    assistant_response = response.choices[0].message.content
    
    # Create a placeholder for the typewriter effect
    message_placeholder = st.empty()
    
    # Typewriter effect
    for i in range(len(assistant_response)):
        message_placeholder.markdown(f"""
        <div class="message-row">
            <div class="assistant-avatar">AI</div>
            <div class="chat-message assistant-message">
                {assistant_response[:i+1]}
            </div>
            <div style="flex-grow: 1;"></div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.02)
    
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": assistant_response,
        "timestamp": datetime.now().isoformat()
    })
    
    st.session_state.user_input = ""
    st.rerun()

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
    💡 AI ให้คำแนะนำทั่วไป สำหรับปัญหาหรือรายละเอียดที่สำคัญติดต่อที่สำนักงานนิติบุคคล<br>
</div>
""", unsafe_allow_html=True)