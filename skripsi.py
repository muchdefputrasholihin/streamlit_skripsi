import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ===============================
# Baca Data CSV
# ===============================
try:
    df = pd.read_csv("hasil_model.csv", sep=";", names=["stemming", "label"], header=None)
    df.columns = df.columns.str.lower()

    # Jika masih nyatu, pisahkan komentar dan label
    if df['stemming'].str.contains(',').any():
        df[['stemming', 'label']] = df['stemming'].str.split(',', n=1, expand=True)

except Exception as e:
    st.error(f"Gagal membaca data: {e}")
    st.stop()
# ===============================
# Sidebar Navigasi
# ===============================
st.sidebar.title("🧭 Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["Deskripsi", "Statistik Sentimen", "Keyword Sentimen", "Penutup"])

# ===============================
# Halaman 1: Deskripsi
# ===============================
if page == "Deskripsi":
    st.title("📚 Kepercayaan Masyarakat terhadap Pondok Pesantren")
    st.image("FOTO.png", caption="Suasana Pondok Pesantren")

    st.subheader("🕌 Apa Itu Pondok Pesantren?")
    st.write("""
        Pondok pesantren adalah lembaga pendidikan agama Islam yang mengajarkan ilmu-ilmu agama dan moral kepada para santri.
        Pesantren berperan penting dalam membina akhlak, karakter, dan keilmuan masyarakat.Pondok Pesantren lembaga pendidikan
        di mana kyai menjadi figur sentral dan masjid menjadi titik pusat yang menjiwainya
    """)

# ===============================
# Halaman 2: Statistik Sentimen
# ===============================
elif page == "Statistik Sentimen":
    st.title("📊 Statistik Sentimen Masyarakat")

    total_data = 1971
    total_data_yt = 971
    total_data_x = 1000
    positif = 851
    negatif = 743
    netral = 743
    
    st.subheader("🔢 Ringkasan Data Sentimen")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total", total_data)
    col2.metric("YOUTUBE", total_data_yt)
    col3.metric("X", total_data_x)
    col4.metric("Positif", positif)
    col5.metric("Negatif", negatif)
    col6.metric("Netral", netral)

    st.subheader("📈 Diagram Pie Sentimen")
    col1, col2 = st.columns(2)
    with col1:
        st.image("persentasee pie.png", caption="Distribusi Sentimen Masyarakat", width=350)
    with col2:
        st.image("perbandingan akurasi dan f1 Score.png", caption="Distribusi Sentimen Masyarakat",  use_container_width=True)

    # Buat 5 kolom sejajar
    import streamlit as st

    st.subheader("📈 Perbandingan Model-Model")

# Buat dua kolom per baris
   # Buat dua kolom per baris
    col1, col2 = st.columns(2)

    with col1:
        st.image("SVM.png", caption="SVM Model", use_container_width=True)
        st.image("RANDOM FOREST.png", caption="Random Forest Model", use_container_width=True)
        st.image("Neural Network.png", caption="Neural Network Model", use_container_width=True)

    with col2:
        st.image("NAIVE BAYES.png", caption="Naive Bayes Model", use_container_width=True)
        st.image("DISECION TREE.png", caption="Decision Tree Model", use_container_width=True)

# ===============================
# Halaman 3: Keyword Sentimen
# ===============================
elif page == "Keyword Sentimen":
    st.title("🗝️ Keyword Berdasarkan Sentimen")

    st.markdown("""
    Berikut adalah contoh keyword yang sering muncul berdasarkan kategori sentimen:
    
    - ✅ **Positif**: Mengandung pujian, rasa syukur, atau dukungan.  
    - ❌ **Negatif**: Mengandung kritik, keluhan, atau kata bermakna buruk.  
    - ⚪ **Netral**: Informasi umum atau tidak memiliki kecenderungan sentimen yang kuat.
    """)

    # ====== Kategori: POSITIF ======
    st.subheader("✅ Positif")
    col1, col2 = st.columns(2)
    with col1:
        st.write("""
        ** Contoh Keyword Positif : **
        - sehat     - Semoga
        - masuk     - Bangga
        - gontor    - alhamdulillah  
        """)
    with col2:
        st.image("positiff.png", caption="Visualisasi Keyword Positif")

    # ====== Kategori: NEGATIF ======
    st.subheader("❌ Negatif")
    col3, col4 = st.columns(2)
    with col3:
        st.image("negatif.png", caption="Visualisasi Keyword Negatif")
    with col4:
        st.write("""
                Berikut ini adalah beberapa contoh kata kunci yang dikategorikan sebagai sentimen negatif. 
                Perlu dicatat bahwa kata-kata ini muncul dalam konteks perbincangan publik yang menyoroti isu-isu sensitif di lingkungan pesantren.

        **Contoh Keyword Bernuansa Negatif:**
        - cabul        - pencabulan  
        - mesum        - pelecehan  
        - kasus        - perkosa  
        """
    )

    # ====== Kategori: NETRAL ======
    st.subheader("⚪ Netral")
    col5, col6 = st.columns(2)
    with col5:
        st.write("""
        **Contoh Keyword Netral:**
        - Nadhatul Ulama    - Masyaallah
        - Lulus 
        - Santri      
        """)
    with col6:
        st.image("netral.png", caption = "Visualisasi Keyword Netral")

    # =======================
    # 🔍 Cek Kata dalam Komentar dan Sentimennya
    # =======================
    st.subheader("🔍 Cek Kata dalam Komentar dan Sentimennya")
    keyword = st.text_input(" Masukkan kata yang ingin dicek (misal: cabul)")

    if keyword:
        if 'stemming' in df.columns :
            matching_comments = df[df['stemming'].str.contains(keyword, case=False, na=False)]

            if not matching_comments.empty:
                count_by_sentiment = matching_comments['label'].value_counts().to_dict()
                total_found = len(matching_comments)

                st.info(f"🔎 Ditemukan {total_found} komentar yang mengandung kata **'{keyword}'**.")

                st.subheader("📌 Komentar yang Mengandung Kata Ini:")
                for _, row in matching_comments.iterrows():
                    stemming = str(row["stemming"]).strip()
                    
                    st.markdown(f"- {stemming}")
            else:
                st.success("✅ Tidak ada komentar yang mengandung kata tersebut.")
        else:
            st.error("❌ Kolom 'komentar' atau 'label' tidak ditemukan dalam data.")

# ===============================
# Halaman 4: Penutup
# ===============================
elif page == "Penutup":
    st.title("📜 Penutup")
    st.markdown("""
    ---
    > ✨ * Di balik kesederhanaan pondok, tersimpan cahaya yang membimbing dunia.*

   Ucapan Terima Kasih

✨ Dengan penuh rasa syukur, penulis menyampaikan terima kasih yang sebesar-besarnya kepada:

✨ Bapak Dihin Muriyatmoko, S.ST., M.T. selaku Ketua Program Studi Teknik Informatika UNIDA Gontor, atas bimbingan, dukungan, dan motivasi yang diberikan selama proses penyusunan skripsi ini.

✨ Bapak Eko Prasetio Widhi, S.Kom., M.Kom. selaku dosen pembimbing skripsi I yang telah memberikan arahan, masukan, dan bimbingan dengan sabar sejak awal hingga selesainya penelitian ini.

✨ Bapak Aziz Musthafa, S.Kom., M.T. selaku dosen pembimbing skripsi II yang juga telah banyak membantu penulis melalui saran yang konstruktif dan semangat yang menguatkan.

✨ Ibu Nurhana Marantika, S.Sos.I., M.A. yang telah berkenan membantu dalam proses verifikasi komentar sebagai bagian penting dari data penelitian ini.

✨ Semoga segala kebaikan dan ilmu yang telah diberikan menjadi amal jariyah dan mendapatkan balasan terbaik dari Allah SWT.

Terima kasih atas segala bantuan, bimbingan, dan dukungan yang telah diberikan. Semoga karya ini dapat bermanfaat bagi masyarakat luas.
               
    """)
