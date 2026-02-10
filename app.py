import streamlit as st
import pandas as pd
import numpy as np

# Configurare stil "Premium"
st.set_page_config(page_title="Wealth Builder Pro", page_icon="💰", layout="wide")

# --- DESIGN HEADER ---
st.title("💰 Wealth Builder Pro")
st.markdown("### *\"Profits are better than wages.\" - J. Earl Shoaff*")

# --- SIDEBAR PENTRU INPUTURI ---
with st.sidebar:
    st.header("⚙️ Parametri Financiari")
    investitie_initiala = st.number_input("Suma Inițială (€):", value=1000, step=100)
    depunere_lunara = st.number_input("Depunere Lunară (€):", value=200, step=50)
    dobanda_anuala = st.slider("Dobândă Anuală Estimată (%):", 1, 20, 8)
    ani = st.slider("Orizont de Timp (Ani):", 1, 40, 10)

# --- LOGICA DE CALCUL (Matematică Financiară) ---
luni = ani * 12
rata_lunara = (dobanda_anuala / 100) / 12
balanta = investitie_initiala
date_grafic = []

for luna in range(1, luni + 1):
    balanta = (balanta + depunere_lunara) * (1 + rata_lunara)
    if luna % 12 == 0: # Salvăm datele anual pentru grafic
        date_grafic.append({"An": luna // 12, "Total": round(balanta, 2)})

df = pd.DataFrame(date_grafic)

# --- AFIȘARE REZULTATE PE PĂTRATE (Stilul tău) ---
st.divider()
c1, c2, c3 = st.columns(3)

total_final = date_grafic[-1]["Total"]
total_investit = investitie_initiala + (depunere_lunara * luni)
profit_pur = total_final - total_investit

c1.metric("💰 Sumă Finală", f"{total_final:,} €")
c2.metric("📥 Total Investit", f"{total_investit:,} €")
c3.metric("📈 Profit Pur", f"{profit_pur:,} €", delta=f"{((total_final/total_investit)-1)*100:.1f}%")

# --- GRAFIC EVOLUȚIE ---
st.divider()
st.subheader("📊 Evoluția Averei în Timp")
st.area_chart(df.set_index("An"), color="#22d3ee")

# --- TABEL DE PROIECTIE ---
with st.expander("📂 Vezi Proiecția Anuală Detaliată"):
    st.table(df)

# --- MESAJ DE BUSINESS ---
st.info("💡 Această proiecție demonstrează puterea dobânzii compuse. Vrei un plan personalizat? Contactează-mă!")

st.divider()
st.caption("Creat de Cristian | Powered by i5 Gen 13 | OO Architecture")