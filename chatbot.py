# Copyright (c) 2025 Shiva Prasad M.R
# All Rights Reserved.
# This code is proprietary and may not be reproduced without permission.

import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO
import time


genai.configure(api_key="AIzaSyCMS-6P84LhtuJI960pvF4kaXhIue6KHp8")
model = genai.GenerativeModel("gemini-2.5-pro")

st.title("Aira Den 🤖")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("type") == "qr":
            st.image(message["content"], caption="Generated QR Code")
        else:
            st.markdown(message["content"])


if prompt := st.chat_input("Ask me anything... (use /qr <link>)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    
    if prompt.lower().startswith("/qr "):
        link = prompt[4:].strip()
        if not link:
            reply = "❌ Please provide a link after /qr"
            with st.chat_message("assistant"):
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        else:
            with st.chat_message("assistant"):
                st.markdown(f"📌 Generating QR Code for: **{link}**")
                qr = qrcode.QRCode(version=1, box_size=10, border=4)
                qr.add_data(link)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buf = BytesIO()
                img.save(buf, format="PNG")
                buf.seek(0)
                st.image(buf, caption="QR Code")
                st.session_state.messages.append({
                    "role": "assistant",
                    "type": "qr",
                    "content": buf
                })

    else:
        
        with st.chat_message("assistant"):
            with st.spinner("🍳 Your response is cooking..."):
                time.sleep(1.5)  # Simulate "thinking"
                try:
                    response = model.generate_content(prompt)
                    reply = response.text
                except Exception as e:
                    reply = f"Error: {e}"
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
