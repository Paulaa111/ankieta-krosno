import streamlit as st
import pandas as pd
from datetime import datetime
import time

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

st.title("📈 Badanie Potrzeb Cyfrowych Biznesu")
st.write("""
**Dzień dobry!** Nazywam się Paula i realizuję projekt badawczy dotyczący wyzwań operacyjnych krośnieńskich firm. 
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
        "Weterynaria", 
        "Edukacja i Szkolenia", 
        "Gastronomia / Cukiernie / Piekarnie",
        "Logistyka i Transport",
        "Budownictwo i Usługi Techniczne",
        "Kwiaciarnie / Rękodzieło",
        "Biblioteki i Instytucje Kultury",
        "Motoryzacja / Warsztaty",
        "Handel Detaliczny",
        "Usługi Specjalistyczne (Prawo, Księgowość)",
        "Inna"
    ]
    branza = st.selectbox("Branża / Profil działalności", lista_branz)
    staz = st.radio("Staż firmy na rynku:", ["Nowa firma (< 1 rok)", "1-5 lat", "Powyżej 5 lat"])

    # II. CODZIENNE OBOWIĄZKI
    st.header("⏳ Czas i Organizacja")
    st.write("Zaznacz zadania, które zabierają najwięcej czasu poza główną działalnością:")
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
        ["Kontakt z klientem", "Rezerwacje online", "Automatyczne wyceny", "Raporty i faktury", "Zarządzanie zapasami", "Inne (napisz poniżej)"]
    )
    
    inne_proces = st.text_input("Jeśli wybrano 'Inne', wpisz co to za proces:")
    
    preferencja_narzedzia = st.radio(
        "Wolisz korzystać z narzędzi pomocniczych na:",
        ["Telefonie (aplikacja, powiadomienia)", "Komputerze (przeglądarka, Excel)", "Tablecie"]
    )
    
    wizja = st.radio(
        "Na co przeznaczyłabyś/przeznaczyłbyś 10 odzyskanych godzin w miesiącu?",
        ["Odpoczynek / Czas prywatny", "Większa liczba zleceń", "Szkolenia i rozwój", "Nowe kierunki usług"]
    )
    
    nowoczesnosc = st.select_slider(
        "Nastawienie do nowych technologii wspomagających pracę:",
        options=["Tradycyjne", "Ostrożne", "Otwarte", "Entuzjastyczne"]
    )

    # IV. PRZYCISK WYŚLIJ
    submit = st.form_submit_button("WYŚLIJ ANKIETĘ")

if submit:
    with st.spinner('Zapisywanie odpowiedzi...'):
        time.sleep(1.2)
        
        nowe_dane = {
            "Data": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Nazwa_Firmy": [nazwa_firmy],
            "Branża": [branza],
            "Staż": [staz],
            "Godziny_Tyg": [godziny_tydzien],
            "Priorytet_Auto": [", ".join(proces_auto)],
            "Inne_proces": [inne_proces],
            "Platforma": [preferencja_narzedzia],
            "Przeznaczenie_Czasu": [wizja],
            "Podejście_Tech": [nowoczesnosc]
        }
        
        df = pd.DataFrame(nowe_dane)
        
        try:
            existing_df = pd.read_csv("badanie_krosno.csv")
            final_df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            final_df = df
            
        final_df.to_csv("badanie_krosno.csv", index=False)
    
    st.success("✨ Dziękuję! Twoja ankieta została pomyślnie wysłana.")
    st.info("""
        Twoje odpowiedzi są niezwykle cenne dla mojego projektu badawczego. 
        Dane zostaną wykorzystane do analizy potrzeb technologicznych lokalnego biznesu w Krośnie.
        Życzę udanego dnia!
    """)