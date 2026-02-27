import streamlit as st
import google.generativeai as genai

# API Ayarları
genai.configure(api_key="AIzaSyACo_b2KfNo7WyAitVNaXHLdn7r-UewhF8")
model = genai.GenerativeModel('gemini-3.1-pro-preview') # Hızlı olması için flash seçtik

# Senin aldığın File ID'leri buraya tanımlıyoruz
DOSYA_KUTUPHANESI = {
    "Tanzimat - Servetifünun": "files/zjqlna9sb89s",
    "Milli Edebiyat": "files/fv556sw4n1ie",
    "Divan Edebiyatı": "files/8nbnbn0htcfv",
    "Cumhuriyet Dönemi": "files/uf2ppbawyp2l",
    "Halk Edebiyatı": "files/4g98e60cfsqi"
}

st.set_page_config(page_title="Edebiyat Soru Botu", page_icon="📚")

st.title("🎓 Edebiyat Sınav Asistanı")
st.write("Çalışmak istediğin dönemi seç ve 'Soru Sor' butonuna bas!")

# Kategori Seçimi
secilen_kategori = st.selectbox("Dönem Seçin:", list(DOSYA_KUTUPHANESI.keys()))

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Soru Sorma Butonu
if st.button("Soru Sor 🚀"):
    file_id = DOSYA_KUTUPHANESI[secilen_kategori]
    
    # Dosyayı buluyoruz
    # Doğrudan ID üzerinden erişim sağlayan güvenli yöntem
    response = model.generate_content([{'file_data': {'file_uri': file_id, 'mime_type': 'application/pdf'}}, prompt])
    
    with st.spinner("Dosya taranıyor ve soru hazırlanıyor..."):
        # Gemini'ye dosyayı ve komutu gönderiyoruz
        prompt = f"Sana verdiğim dosyaya bakarak {secilen_kategori} hakkında 4 şıklı, kaliteli bir soru sor. Cevabı en altta belirt."
        response = model.generate_content([ilgili_dosya, prompt])
        
        # Cevabı ekrana yazdır ve geçmişe ekle
        st.session_state.chat_history.append({"role": "assistant", "content": response.text})

# Sohbet Geçmişini Göster
for message in reversed(st.session_state.chat_history):
    with st.chat_message(message["role"]):

        st.write(message["content"])
