import streamlit as st
import google.generativeai as genai

# GÜVENLİ ANAHTAR: Artık anahtarı buradan değil, Streamlit Secrets'tan alıyor
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3-flash-preview')

# DOSYA KİMLİKLERİ: Bunlar aynen kalıyor, tekrar yükleme yapmana gerek yok
DOSYA_KUTUPHANESI = {
    "Tanzimat - Servetifünun": "files/zjqlna9sb89s",
    "Milli Edebiyat": "files/fv556sw4n1ie",
    "Divan Edebiyatı": "files/8nbnbn0htcfv",
    "Cumhuriyet Dönemi": "files/uf2ppbawyp2l",
    "Halk Edebiyatı": "files/4g98e60cfsqi"
}

st.set_page_config(page_title="Edebiyat Soru Botu", page_icon="📚")
st.title("🎓 Edebiyat Sınav Asistanı")
st.info("Jarvis 0.1 altyapısıyla hazırlanmıştır.")

secilen_kategori = st.selectbox("Hangi dönemden soru gelsin?", list(DOSYA_KUTUPHANESI.keys()))

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("Yeni Soru Sor 🚀"):
    file_id = DOSYA_KUTUPHANESI[secilen_kategori]
    tam_adres = f"https://generativelanguage.googleapis.com/v1beta/{file_id}"
    
    with st.spinner("Dosya taranıyor..."):
        try:
            # 1. HİZALAMA: 'response' satırı 'with'in 4 boşluk içinde
            response = model.generate_content([
                {
                    "file_data": {
                        "mime_type": "application/pdf",
                        "file_uri": tam_adres
                    }
                },
                f"Sana verdiğim {secilen_kategori} dosyasını incele ve bana 4 şıklı bir edebiyat sorusu sor. Cevabı en sona sakla."
            ])
            
            # 2. HİZALAMA: Bu satır 'response' ile TAM AYNI hizada olmalı!
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

for message in reversed(st.session_state.chat_history):
    with st.chat_message(message["role"]):
        st.write(message["content"])



