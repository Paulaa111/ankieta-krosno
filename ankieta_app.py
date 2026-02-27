import streamlit as st
import pandas as pd
from datetime import datetime
import time
from streamlit_gsheets import GSheetsConnection

# Konfiguracja strony
st.set_page_config(page_title="Badanie Potrzeb Cyfrowych - Krosno", page_icon="📈", layout="centered")

# Nowoczesna stylizacja
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .stButton>button { 
        width: 100%; 
        border-radius: 12px; 
        height: 3.5em; 
        background-color: #0f172a; 
        color: white; 
        font-weight: 600;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #334155;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    h1 { color: #0f172a; font-family: 'Inter', sans-serif; font-weight: 800; }
    h2 { color: #1e293b; border-left: 5px solid #3b82f6; padding-left: 15px; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# Inicjalizacja połączenia z Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📈 Badanie Potrzeb Cyfrowych Biznesu")
st.write("""
**Cześć! :)** Mam na imię Paula i realizuję projekt badawczy dotyczący wyzwań operacyjnych krośnieńskich firm. 
Twoje odpowiedzi pomogą mi zrozumieć, które codzienne procesy są najbardziej czasochłonne i jak nowoczesne technologie 
mogą wesprzeć lokalny rynek.

Dziękuję za Twój czas i wsparcie mojego projektu!
""")

with st.form("ankieta_final"):
    # I. PROFIL FIRMY
    st.header("🏢 O Firmie")
    nazwa_firmy = st.text_input("Nazwa firmy (opcjonalnie)")
    
    lista_branz = [
        "Beauty (Fryzjer, Barber, Kosmetyczka)", 
        "Weterynaria", "Edukacja i Szkolenia", "Gastronomia / Cukiernie / Piekarnie",
        "Logistyka i Transport", "Budownictwo i Usługi Techniczne", "Kwiaciarnie / Rękodzieło",
        "Biblioteki i Instytucje Kultury", "Motoryzacja / Warsztaty", "Handel Detaliczny",
        "Usługi Specjalistyczne (Prawo, Księgowość)", "Inna"
    ]
    branza = st.selectbox("Branża / Profil działalności", lista_branz)
    staz = st.radio("Staż firmy na rynku:", ["Nowa firma (< 1 rok)", "1-5 lat", "Powyżej 5 lat"])

    # II. CODZIENNE OBOWIĄZKI
    st.header("⏳ Czas i Organizacja")
    st.write("Zaznacz zadania, które zabierają najwięcej czasu:")
    p1 = st.checkbox("Obsługa zapytań (cennik, terminy, dostępność)")
    p2 = st.checkbox("Zarządzanie grafikiem i rezerwacjami")
    p3 = st.checkbox("Dokumentacja, faktury i rozliczenia")
    p4 = st.checkbox("Przygotowywanie ofert i kosztorysów")
    p5 = st.checkbox("Marketing i media społecznościowe")

    godziny_tydzien = st.select_slider(
        "Ile godzin tygodniowo pochłaniają sprawy organizacyjne?",
        options=["0-5h", "5-10h", "10-20h", "20h+"]
    )

    # III. POTENCJAŁ I PREFERENCJE
    st.header("💡 Potencjał Usprawnień")
    proces_auto = st.multiselect(
        "Gdyby można było zautomatyzować jeden proces, co byłoby priorytetem?",
        ["Kontakt z klientem", "Rezerwacje online", "Automatyczne wyceny", "Raporty i faktury", "Zarządzanie zapasami", "Inne"]
    )
    inne_proces = st.text_input("Jeśli wybrano 'Inne', wpisz co to za proces:")
    
    preferencja_narzedzia = st.radio(
        "Wolisz korzystać z narzędzi pomocniczych na:",
        ["Telefonie (aplikacja, powiadomienia)", "Komputerze (przeglądarka, Excel)", "Tablecie"]
    )
    
    wizja = st.radio(
        "Na co zostałby przeznaczony odzyskany czas (np. 10h/miesiąc)?",
        ["Odpoczynek / Czas prywatny", "Większa liczba zleceń", "Szkolenia i rozwój", "Nowe kierunki usług"]
    )
    
    nowoczesnosc = st.select_slider(
        "Nastawienie do nowych technologii wspomagających pracę:",
        options=["Tradycyjne", "Ostrożne", "Otwarte", "Entuzjastyczne"]
    )

    submit = st.form_submit_button("WYŚLIJ ANKIETĘ")

if submit:
    try:
        # 1. Pasek postępu
        progress_text = "Zapisywanie danych w Arkuszu Google..."
        my_bar = st.progress(0, text=progress_text)
        
        # 2. Przygotowanie danych do wysłania
        nowe_dane = pd.DataFrame([{
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nazwa_Firmy": nazwa_firmy,
            "Branża": branza,
            "Staż": staz,
            "Godziny_Tyg": godziny_tydzien,
            "Priorytet_Auto": ", ".join(proces_auto),
            "Inne_proces": inne_proces,
            "Platforma": preferencja_narzedzia,
            "Przeznaczenie_Czasu": wizja,
            "Podejście_Tech": nowoczesnosc
        }])

        # 3. Zapis metodą uproszczoną
        # Używamy bezpośredniego dopisywania (append) zamiast aktualizacji całości
        conn.update(worksheet="Sheet1", data=nowe_dane)
        
        # Wyświetlanie sukcesu
        my_bar.progress(100)
        time.sleep(0.5)
        my_bar.empty()
        
        st.balloons()
        st.success("### Dziękuję! Twoja opinia została zarejestrowana.")
        st.toast('Dane zapisane pomyślnie!', icon='✅')
        
    except Exception as e:
        st.error(f"Nadal występuje problem z połączeniem.")
        st.info(f"Treść błędu: {e}")
        st.warning("""
        **Co możesz teraz zrobić?**
        1. Sprawdź czy w Arkuszu Google zakładka na dole na pewno nazywa się **Sheet1** (bez spacji).
        2. Sprawdź czy w Secrets link jest w cudzysłowie i kończy się na `/edit`.

        """)

