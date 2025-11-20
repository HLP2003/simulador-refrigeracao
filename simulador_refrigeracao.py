# simulador_refrigeracao_unico_ptbr.py
# Simulador único — PT-BR
# Uso: pip install streamlit matplotlib numpy pandas
# streamlit run simulador_refrigeracao_unico_ptbr.py

import streamlit as st, numpy as np, pandas as pd, matplotlib.pyplot as plt
from math import sqrt

st.set_page_config(page_title="Simulador de Refrigeração — PT-BR", layout="wide")
st.title("Simulador de Refrigeração de CPU (PT-BR)")
st.markdown("Selecione **arquitetura → CPU**, cooler e condição do gabinete. Explicações em português abaixo.")

# =====================================================================
# ====================== DADOS (CPUS E COOLERS) =======================
# =====================================================================

CPUS = [
    {"modelo":"AMD Ryzen 5 1600X","tdp":95,"ano":2017,"socket":"AM4","frequencia_base":3.6,"frequencia_turbo":4.0,"arquitetura":"Zen","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 5 3600","tdp":65,"ano":2019,"socket":"AM4","frequencia_base":3.6,"frequencia_turbo":4.2,"arquitetura":"Zen 2","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 5 5600","tdp":65,"ano":2021,"socket":"AM4","frequencia_base":3.5,"frequencia_turbo":4.4,"arquitetura":"Zen 3","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 5 5600X","tdp":65,"ano":2020,"socket":"AM4","frequencia_base":3.7,"frequencia_turbo":4.6,"arquitetura":"Zen 3","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 5 5600X3D","tdp":105,"ano":2022,"socket":"AM4","frequencia_base":3.3,"frequencia_turbo":4.4,"arquitetura":"Zen 3 (3D)","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 5 5500X3D","tdp":105,"ano":2024,"socket":"AM4","frequencia_base":3.0,"frequencia_turbo":4.0,"arquitetura":"Zen 3 (3D)","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 5 7400F","tdp":65,"ano":2024,"socket":"AM5","frequencia_base":3.7,"frequencia_turbo":4.7,"arquitetura":"Zen 4","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 5 7500F","tdp":65,"ano":2024,"socket":"AM5","frequencia_base":3.7,"frequencia_turbo":5.0,"arquitetura":"Zen 4","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 5 7600","tdp":65,"ano":2022,"socket":"AM5","frequencia_base":3.8,"frequencia_turbo":5.1,"arquitetura":"Zen 4","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 5 7600X","tdp":105,"ano":2022,"socket":"AM5","frequencia_base":4.7,"frequencia_turbo":5.3,"arquitetura":"Zen 4","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 5 7600X3D","tdp":65,"ano":2024,"socket":"AM5","frequencia_base":4.1,"frequencia_turbo":4.7,"arquitetura":"Zen 4 (3D)","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 5 8400F","tdp":65,"ano":2024,"socket":"AM5","frequencia_base":4.2,"frequencia_turbo":4.7,"arquitetura":"Zen 5","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 5 8500G","tdp":65,"ano":2024,"socket":"AM5","frequencia_base":3.5,"frequencia_turbo":5.0,"arquitetura":"Zen 5 (G)","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 5 8600G","tdp":65,"ano":2024,"socket":"AM5","frequencia_base":4.3,"frequencia_turbo":5.0,"arquitetura":"Zen 5 (G)","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 5 9600X","tdp":65,"ano":2024,"socket":"AM5","frequencia_base":3.9,"frequencia_turbo":5.4,"arquitetura":"Zen 5","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 7 7700","tdp":65,"ano":2023,"socket":"AM5","frequencia_base":3.8,"frequencia_turbo":5.3,"arquitetura":"Zen 4","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 7 7700X","tdp":105,"ano":2023,"socket":"AM5","frequencia_base":4.5,"frequencia_turbo":5.4,"arquitetura":"Zen 4","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 7 5800X","tdp":105,"ano":2020,"socket":"AM4","frequencia_base":3.8,"frequencia_turbo":4.7,"arquitetura":"Zen 3","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 7 5800X3D","tdp":105,"ano":2022,"socket":"AM4","frequencia_base":3.4,"frequencia_turbo":4.5,"arquitetura":"Zen 3 (3D)","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 9 5900X","tdp":105,"ano":2020,"socket":"AM4","frequencia_base":3.7,"frequencia_turbo":4.8,"arquitetura":"Zen 3","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 9 5950X","tdp":105,"ano":2020,"socket":"AM4","frequencia_base":3.4,"frequencia_turbo":4.9,"arquitetura":"Zen 3","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 9 7950X","tdp":170,"ano":2022,"socket":"AM5","frequencia_base":4.5,"frequencia_turbo":5.7,"arquitetura":"Zen 4","fabricante":"AMD"},
    {"modelo":"AMD Ryzen 9 7950X3D","tdp":120,"ano":2023,"socket":"AM5","frequencia_base":4.2,"frequencia_turbo":5.7,"arquitetura":"Zen 4 (3D)","fabricante":"AMD"},

    {"modelo":"Intel Core 2 Duo E8400","tdp":65,"ano":2008,"socket":"LGA775","frequencia_base":3.0,"frequencia_turbo":3.0,"arquitetura":"Core (65nm)","fabricante":"Intel"},
    {"modelo":"Intel Core i3-530","tdp":73,"ano":2010,"socket":"LGA1156","frequencia_base":2.93,"frequencia_turbo":3.06,"arquitetura":"Clarksfield","fabricante":"Intel"},
    {"modelo":"Intel Core i3-3240","tdp":55,"ano":2012,"socket":"LGA1155","frequencia_base":3.4,"frequencia_turbo":3.4,"arquitetura":"Ivy Bridge","fabricante":"Intel"},
    {"modelo":"Intel Core i7-920","tdp":130,"ano":2008,"socket":"LGA1366","frequencia_base":2.66,"frequencia_turbo":2.93,"arquitetura":"Nehalem","fabricante":"Intel"},
    {"modelo":"Intel Core i3-6100","tdp":51,"ano":2015,"socket":"LGA1151","frequencia_base":3.7,"frequencia_turbo":3.7,"arquitetura":"Skylake","fabricante":"Intel"},
    {"modelo":"Intel Core i5-6600K","tdp":91,"ano":2015,"socket":"LGA1151","frequencia_base":3.5,"frequencia_turbo":3.9,"arquitetura":"Skylake","fabricante":"Intel"},
    {"modelo":"Intel Core i5-8400","tdp":65,"ano":2018,"socket":"LGA1151","frequencia_base":2.8,"frequencia_turbo":4.0,"arquitetura":"Coffee Lake","fabricante":"Intel"},
    {"modelo":"Intel Core i5-10400F","tdp":65,"ano":2020,"socket":"LGA1200","frequencia_base":2.9,"frequencia_turbo":4.3,"arquitetura":"Comet Lake","fabricante":"Intel"},
    {"modelo":"Intel Core i5-10600K","tdp":125,"ano":2020,"socket":"LGA1200","frequencia_base":4.1,"frequencia_turbo":4.8,"arquitetura":"Comet Lake","fabricante":"Intel"},
    {"modelo":"Intel Core i5-12400F","tdp":65,"ano":2022,"socket":"LGA1700","frequencia_base":2.5,"frequencia_turbo":4.4,"arquitetura":"Alder Lake","fabricante":"Intel"},
    {"modelo":"Intel Core i5-13400F","tdp":65,"ano":2023,"socket":"LGA1700","frequencia_base":2.5,"frequencia_turbo":4.6,"arquitetura":"Raptor Lake","fabricante":"Intel"},
    {"modelo":"Intel Core i5-14600K","tdp":180,"ano":2024,"socket":"LGA1700","frequencia_base":3.1,"frequencia_turbo":5.1,"arquitetura":"Raptor Lake Refresh","fabricante":"Intel"},
    {"modelo":"Intel Core i7-11700K","tdp":125,"ano":2021,"socket":"LGA1200","frequencia_base":3.6,"frequencia_turbo":5.0,"arquitetura":"Rocket Lake","fabricante":"Intel"},
    {"modelo":"Intel Core i7-12700K","tdp":190,"ano":2022,"socket":"LGA1700","frequencia_base":3.6,"frequencia_turbo":5.0,"arquitetura":"Alder Lake","fabricante":"Intel"},
    {"modelo":"Intel Core i7-13700K","tdp":250,"ano":2023,"socket":"LGA1700","frequencia_base":3.4,"frequencia_turbo":5.4,"arquitetura":"Raptor Lake","fabricante":"Intel"},
    {"modelo":"Intel Core i9-10900K","tdp":125,"ano":2020,"socket":"LGA1200","frequencia_base":3.7,"frequencia_turbo":5.3,"arquitetura":"Comet Lake","fabricante":"Intel"},
    {"modelo":"Intel Core i9-12900K","tdp":240,"ano":2022,"socket":"LGA1700","frequencia_base":3.2,"frequencia_turbo":5.2,"arquitetura":"Alder Lake","fabricante":"Intel"},
    {"modelo":"Intel Core i9-13900K","tdp":250,"ano":2023,"socket":"LGA1700","frequencia_base":3.0,"frequencia_turbo":5.8,"arquitetura":"Raptor Lake","fabricante":"Intel"},
    {"modelo":"Intel Core i9-14900K","tdp":250,"ano":2024,"socket":"LGA1700","frequencia_base":3.2,"frequencia_turbo":6.0,"arquitetura":"Raptor Lake Refresh","fabricante":"Intel"},
    {"modelo":"Intel Xeon E5-2666 v3","tdp":115,"ano":2014,"socket":"LGA2011-v3","frequencia_base":2.9,"frequencia_turbo":3.5,"arquitetura":"Haswell-EP","fabricante":"Intel"},
    {"modelo":"Intel Xeon E5-2667 v3","tdp":135,"ano":2014,"socket":"LGA2011-v3","frequencia_base":3.2,"frequencia_turbo":3.6,"arquitetura":"Haswell-EP","fabricante":"Intel"},
    {"modelo":"Intel Xeon E5-2667 v4","tdp":160,"ano":2016,"socket":"LGA2011-v3","frequencia_base":3.2,"frequencia_turbo":3.7,"arquitetura":"Broadwell-EP","fabricante":"Intel"},
    {"modelo":"Intel Xeon E5-2680 v4","tdp":120,"ano":2016,"socket":"LGA2011-v3","frequencia_base":2.4,"frequencia_turbo":3.3,"arquitetura":"Broadwell-EP","fabricante":"Intel"},
    {"modelo":"Intel Xeon E5-1660 v3","tdp":140,"ano":2014,"socket":"LGA2011-v3","frequencia_base":3.0,"frequencia_turbo":3.7,"arquitetura":"Haswell-EP","fabricante":"Intel"},
    {"modelo":"Intel Xeon E5-2680 v3","tdp":135,"ano":2014,"socket":"LGA2011-v3","frequencia_base":2.5,"frequencia_turbo":3.3,"arquitetura":"Haswell-EP","fabricante":"Intel"},
    {"modelo":"Intel Xeon E5-2690 v3","tdp":135,"ano":2014,"socket":"LGA2011-v3","frequencia_base":2.6,"frequencia_turbo":3.5,"arquitetura":"Haswell-EP","fabricante":"Intel"},
    {"modelo":"Intel Xeon E5-2670 v3","tdp":120,"ano":2014,"socket":"LGA2011-v3","frequencia_base":2.3,"frequencia_turbo":3.1,"arquitetura":"Haswell-EP","fabricante":"Intel"},
    {"modelo":"Intel Xeon E5-2699 v4","tdp":145,"ano":2016,"socket":"LGA2011-v3","frequencia_base":2.2,"frequencia_turbo":3.6,"arquitetura":"Broadwell-EP","fabricante":"Intel"},

    {"modelo":"Intel Xeon E5-1630 v3","tdp":140,"ano":2014,"socket":"LGA2011-v3","frequencia_base":3.7,"frequencia_turbo":3.7,"arquitetura":"Haswell-EP","fabricante":"Intel"},
    {"modelo":"AMD FX-8350","tdp":125,"ano":2012,"socket":"AM3+","frequencia_base":4.0,"frequencia_turbo":4.2,"arquitetura":"Piledriver","fabricante":"AMD"},
]

COOLERS = [
    {"modelo":"SuperFrame SuperFlow 450 (Air)","tipo":"Air","tdp_manufacturer":95,"ruido_db":25,"durabilidade_anos":4},
    {"modelo":"Gamdias Boreas E1-410 (Air)","tipo":"Air","tdp_manufacturer":95,"ruido_db":28,"durabilidade_anos":4},
    {"modelo":"TGT Glacier 120 (Air)","tipo":"Air","tdp_manufacturer":100,"ruido_db":36,"durabilidade_anos":3},
    {"modelo":"DeepCool Gammaxx 400 (Air)","tipo":"Air","tdp_manufacturer":120,"ruido_db":38,"durabilidade_anos":4},
    {"modelo":"Redragon TYR (Air)","tipo":"Air","tdp_manufacturer":130,"ruido_db":22,"durabilidade_anos":4},
    {"modelo":"Cooler Master Hyper 212 (Air)","tipo":"Air","tdp_manufacturer":150,"ruido_db":35,"durabilidade_anos":5},
    {"modelo":"DeepCool AK500S (Air)","tipo":"Air","tdp_manufacturer":150,"ruido_db":28,"durabilidade_anos":6},
    {"modelo":"Thermalright TRUE Spirit 140 (Air)","tipo":"Air","tdp_manufacturer":200,"ruido_db":28,"durabilidade_anos":6},
    {"modelo":"Arctic Freezer 34 (Air)","tipo":"Air","tdp_manufacturer":180,"ruido_db":28,"durabilidade_anos":5},
    {"modelo":"DeepCool AK400 (Air)","tipo":"Air","tdp_manufacturer":220,"ruido_db":29,"durabilidade_anos":6},
    {"modelo":"DeepCool Gammaxx AG400 (Air)","tipo":"Air","tdp_manufacturer":220,"ruido_db":28,"durabilidade_anos":4},
    {"modelo":"GameMax Sigma 520 (Air)","tipo":"Air","tdp_manufacturer":220,"ruido_db":30,"durabilidade_anos":5},
    {"modelo":"Rise Mode Storm 8 (Air)","tipo":"Air","tdp_manufacturer":280,"ruido_db":30,"durabilidade_anos":5},
    {"modelo":"Be Quiet! Dark Rock Pro 4 (Air)","tipo":"Air","tdp_manufacturer":250,"ruido_db":24,"durabilidade_anos":7},
    {"modelo":"Noctua NH-D15 (Air)","tipo":"Air","tdp_manufacturer":250,"ruido_db":24,"durabilidade_anos":8},
    {"modelo":"DeepCool AK620 (Air)","tipo":"Air","tdp_manufacturer":260,"ruido_db":28,"durabilidade_anos":6},

    {"modelo":"Rise Mode Black 240 (Water)","tipo":"AIO","tdp_manufacturer":250,"ruido_db":30,"durabilidade_anos":5},
    {"modelo":"GameMax IceBurg 240 (Water)","tipo":"AIO","tdp_manufacturer":245,"ruido_db":31,"durabilidade_anos":6},
    {"modelo":"Corsair H100i (AIO 240) (Water)","tipo":"AIO","tdp_manufacturer":300,"ruido_db":28,"durabilidade_anos":6},
    {"modelo":"Arctic Liquid Freezer II 240","tipo":"AIO","tdp_manufacturer":320,"ruido_db":27,"durabilidade_anos":7},
    {"modelo":"TGT Storm 240 (Water)","tipo":"AIO","tdp_manufacturer":280,"ruido_db":33,"durabilidade_anos":5},
    {"modelo":"DeepCool LS720 (AIO 360) (Water)","tipo":"AIO","tdp_manufacturer":300,"ruido_db":32,"durabilidade_anos":7},
    {"modelo":"Corsair H150i (AIO 360)","tipo":"AIO","tdp_manufacturer":350,"ruido_db":30,"durabilidade_anos":7},
    {"modelo":"NZXT Kraken X63 (AIO 280)","tipo":"AIO","tdp_manufacturer":350,"ruido_db":29,"durabilidade_anos":7},
    {"modelo":"DeepCool Castle 360EX (AIO 360)","tipo":"AIO","tdp_manufacturer":350,"ruido_db":31,"durabilidade_anos":7},
    {"modelo":"Rise Mode Gamer Black 240 (AIO)","tipo":"AIO","tdp_manufacturer":220,"ruido_db":28,"durabilidade_anos":6},
    {"modelo":"Pichau AIO 240 (Water)","tipo":"AIO","tdp_manufacturer":270,"ruido_db":34,"durabilidade_anos":5},
    {"modelo":"Husky Hunter 240 (AIO)","tipo":"AIO","tdp_manufacturer":260,"ruido_db":33,"durabilidade_anos":5},

    # novos air coolers
    {"modelo":"NX400 Montech (Air)","tipo":"Air","tdp_manufacturer":90,"ruido_db":30,"durabilidade_anos":3},
    {"modelo":"Gamdias Boreas (Air)","tipo":"Air","tdp_manufacturer":95,"ruido_db":31,"durabilidade_anos":4},
    {"modelo":"Boreas E2 410 (Air)","tipo":"Air","tdp_manufacturer":100,"ruido_db":31,"durabilidade_anos":4},
    {"modelo":"Rise Mode Z2 Pro (Air)","tipo":"Air","tdp_manufacturer":110,"ruido_db":29,"durabilidade_anos":4},
    {"modelo":"Gamemax Sigma 520 Digital N2 (Air)","tipo":"Air","tdp_manufacturer":130,"ruido_db":32,"durabilidade_anos":4},
    {"modelo":"Rise Mode Winter Black (Air)","tipo":"Air","tdp_manufacturer":140,"ruido_db":30,"durabilidade_anos":5},
    {"modelo":"Cooler Master Hyper 212 Spectrum V3 (Air)","tipo":"Air","tdp_manufacturer":150,"ruido_db":34,"durabilidade_anos":5},
    {"modelo":"PCYES Frost Pulse Black (Air)","tipo":"Air","tdp_manufacturer":160,"ruido_db":33,"durabilidade_anos":5},
    {"modelo":"Pichau Falcon (Air)","tipo":"Air","tdp_manufacturer":170,"ruido_db":34,"durabilidade_anos":5},
    {"modelo":"Air Cooler Boreas E2-410 (Air)","tipo":"Air","tdp_manufacturer":100,"ruido_db":31,"durabilidade_anos":4},

    # novos water coolers
    {"modelo":"Water Cooler Gamer Rise Mode Black ARGB 120mm (AIO)","tipo":"AIO","tdp_manufacturer":180,"ruido_db":32,"durabilidade_anos":4},
    {"modelo":"Water Cooler Tgt Spartel V3 Rainbow 120mm (AIO)","tipo":"AIO","tdp_manufacturer":170,"ruido_db":33,"durabilidade_anos":4},
    {"modelo":"Water Cooler Pichau Aqua 240S (AIO)","tipo":"AIO","tdp_manufacturer":260,"ruido_db":34,"durabilidade_anos":5},
    {"modelo":"Water Cooler Gamer Ninja Yuki ARGB 120mm (AIO)","tipo":"AIO","tdp_manufacturer":175,"ruido_db":31,"durabilidade_anos":4},
    {"modelo":"Water Cooler Husky Icy Comet (AIO)","tipo":"AIO","tdp_manufacturer":200,"ruido_db":33,"durabilidade_anos":5},
    {"modelo":"Water Cooler Husky Glacier (AIO)","tipo":"AIO","tdp_manufacturer":230,"ruido_db":33,"durabilidade_anos":5},
    {"modelo":"Water Cooler PCYES Nix 2 120mm (AIO)","tipo":"AIO","tdp_manufacturer":165,"ruido_db":32,"durabilidade_anos":4},
]

# Ajuste do TDP nominal
for c in COOLERS:
    c["tdp_nominal"] = round(0.85 * c.get("tdp_manufacturer", 0.0), 1)

# =====================================================================
# ========================== FUNÇÕES DO MODELO =========================
# =====================================================================

BASE_SAFETY_PCT = 0.10
WORKLOAD_PROFILES = {
    "Idle / Leve": 0.15,
    "Navegação / Escritório": 0.30,
    "Jogos (típico)": 0.55,
    "Bench sustentado (Cinebench)": 1.00,
    "AVX/Prime (pesado)": 1.30
}

def avg_freq(cpu):
    return (cpu.get("frequencia_base", 3.5) + cpu.get("frequencia_turbo", 3.5)) / 2.0

def cpu_power_model(tdp, carga_pct, profile, freq_scale=1.0):
    idle = 0.10 * tdp
    dyn = tdp * (carga_pct/100.0) * (0.80 * profile) * freq_scale
    leak = 0.02 * tdp * (1 + 0.05*(freq_scale - 1.0))
    return max(0.0, idle + dyn + leak)

def compute_PLs(cpu):
    t = cpu["tdp"]
    y = cpu["ano"]
    if y >= 2022:  return round(t*1.2,1), round(t*1.8,1), 28.0
    if y >= 2017:  return round(t*1.05,1), round(t*1.4,1), 20.0
    return round(t*1.0,1), round(t*1.2,1), 10.0

def derive_rth_heatsink(c):
    nome = c["modelo"].lower()
    tipo = c["tipo"].lower()

    if tipo == "aio":
        if "360" in nome: return 0.07
        if "280" in nome: return 0.09
        if "240" in nome or "h100" in nome: return 0.11
        return 0.10

    premium = ["noctua", "dark rock", "true spirit", "ak620"]

    if "hyper 212" in nome: return 0.16
    if any(p in nome for p in premium): return 0.12
    if any(k in nome for k in ["gammaxx","superframe","gamedias","glacier","tyr"]): return 0.18

    return 0.18

def cpu_r_cs(cpu):
    # resistência CPU → IHS → cooler
    if cpu["fabricante"] == "AMD":
        if "3d" in cpu["arquitetura"].lower():
            return 0.25
        return 0.22
    return 0.20

def temp_cpu(power, r_total, amb):
    return amb + power * r_total

# =====================================================================
# ======================== INTERFACE STREAMLIT =========================
# =====================================================================

st.sidebar.header("Seleção")

arquiteturas = sorted(list(set([c["arquitetura"] for c in CPUS])))
arq_sel = st.sidebar.selectbox("Arquitetura", arquiteturas)

cpu_list = [c for c in CPUS if c["arquitetura"] == arq_sel]
cpu_sel_name = st.sidebar.selectbox("CPU", [c["modelo"] for c in cpu_list])
cpu_sel = next(c for c in cpu_list if c["modelo"] == cpu_sel_name)

cooler_sel_name = st.sidebar.selectbox("Cooler", [c["modelo"] for c in COOLERS])
cooler_sel = next(c for c in COOLERS if c["modelo"] == cooler_sel_name)

temp_amb = st.sidebar.slider("Temperatura ambiente (°C)", 10, 40, 25)
profile_sel_name = st.sidebar.selectbox("Uso / Carga", list(WORKLOAD_PROFILES.keys()))
profile_sel = WORKLOAD_PROFILES[profile_sel_name]

PL1, PL2, tau = compute_PLs(cpu_sel)
st.sidebar.markdown(f"**PL1:** {PL1} W — **PL2:** {PL2} W")

freq_scale = st.sidebar.slider("Overclock (multiplicador de frequência)", 1.0, 1.5, 1.0)

# =====================================================================
# =========================== SIMULAÇÃO ================================
# =====================================================================

r_hs = derive_rth_heatsink(cooler_sel)
r_cs_val = cpu_r_cs(cpu_sel)
r_total = r_hs + r_cs_val

power = cpu_power_model(cpu_sel["tdp"], 100, profile_sel, freq_scale)
power = min(power, PL2)

temp_est = temp_cpu(power, r_total, temp_amb)

# =====================================================================
# ============================ RESULTADOS ==============================
# =====================================================================

st.subheader("Resultados da Simulação")

col1, col2, col3 = st.columns(3)
col1.metric("Potência estimada (W)", f"{power:.1f} W")
col2.metric("Resistência Térmica Total (°C/W)", f"{r_total:.3f}")
col3.metric("Temperatura Estimada (°C)", f"{temp_est:.1f} °C")

# gráfico
st.subheader("Comportamento Térmico")

temps = []
powers = []
steps = np.linspace(0.1, profile_sel, 30)

for p in steps:
    pw = cpu_power_model(cpu_sel["tdp"], 100*p, p, freq_scale)
    temps.append(temp_cpu(pw, r_total, temp_amb))
    powers.append(pw)

plt.figure(figsize=(7,4))
plt.plot(steps, temps, linewidth=2)
plt.xlabel("Carga relativa")
plt.ylabel("Temperatura (°C)")
plt.grid(True)

st.pyplot(plt)

# =====================================================================
# ============================== INFO =================================
# =====================================================================

st.markdown("---")
st.subheader("Como interpretar o resultado")

st.markdown("""
- **Temperaturas abaixo de 75°C:** excelentes para jogos e uso geral.  
- **75–85°C:** normal para Ryzen e Intel modernos em carga.  
- **Acima de 90°C:** risco de thermal throttling.  
- **Acima de 95°C:** limite crítico para CPUs modernas (Zen4/5 e Intel 12–14th).  
""")

