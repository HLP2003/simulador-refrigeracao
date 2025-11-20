# simulador_refrigeracao_unico_ptbr.py
# Simulador único — PT-BR
# Uso: pip install streamlit matplotlib numpy pandas
# streamlit run simulador_refrigeracao_unico_ptbr.py

import streamlit as st, numpy as np, pandas as pd, matplotlib.pyplot as plt
from math import sqrt

st.set_page_config(page_title="Simulador de Refrigeração — PT-BR", layout="wide")
st.title("Simulador de Refrigeração de CPU (PT-BR)")
st.markdown("Selecione **arquitetura → CPU**, cooler e condição do gabinete. Explicações em português abaixo.")

# ---------------------------
# DADOS (CPUS e COOLERS: sua lista completa)
# ---------------------------
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
    # Novo: Intel Xeon E5-1630 (adicionado conforme pedido)
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

    # -----------------------------
    # NOVOS AIR COOLERS (adicionados conforme pedido) — não alterei os existentes
    # Valores tdp_manufacturer estimados para posicionamento relativo
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

    # NOVOS WATER COOLERS (AIO) — adicionados conforme pedido
    {"modelo":"Water Cooler Gamer Rise Mode Black ARGB 120mm (AIO)","tipo":"AIO","tdp_manufacturer":180,"ruido_db":32,"durabilidade_anos":4},
    {"modelo":"Water Cooler Tgt Spartel V3 Rainbow 120mm (AIO)","tipo":"AIO","tdp_manufacturer":170,"ruido_db":33,"durabilidade_anos":4},
    {"modelo":"Water Cooler Pichau Aqua 240S (AIO)","tipo":"AIO","tdp_manufacturer":260,"ruido_db":34,"durabilidade_anos":5},
    {"modelo":"Water Cooler Gamer Ninja Yuki ARGB 120mm (AIO)","tipo":"AIO","tdp_manufacturer":175,"ruido_db":31,"durabilidade_anos":4},
    {"modelo":"Water Cooler Husky Icy Comet (AIO)","tipo":"AIO","tdp_manufacturer":200,"ruido_db":33,"durabilidade_anos":5},
    {"modelo":"Water Cooler Husky Glacier (AIO)","tipo":"AIO","tdp_manufacturer":230,"ruido_db":33,"durabilidade_anos":5},
    {"modelo":"Water Cooler PCYES Nix 2 120mm (AIO)","tipo":"AIO","tdp_manufacturer":165,"ruido_db":32,"durabilidade_anos":4},
]
# ajuste prático do nominal do cooler (eficiência prática)
for c in COOLERS: c["tdp_nominal"] = round(0.85 * c.get("tdp_manufacturer", 0.0),1)

# ---------------------------
# PERFIS e PARÂMETROS
# ---------------------------
BASE_SAFETY_PCT = 0.10
WORKLOAD_PROFILES = {"Idle / Leve":0.15,"Navegação / Escritório":0.30,"Jogos (típico)":0.55,"Bench sustentado (Cinebench)":1.00,"AVX/Prime (pesado)":1.30}

# ---------------------------
# FUNÇÕES (explicadas)
# ---------------------------
def avg_freq(cpu): return (cpu.get("frequencia_base",3.5)+cpu.get("frequencia_turbo",3.5))/2.0

def cpu_power_model(tdp, carga_pct, profile, freq_scale=1.0):
    # retorna W estimados (heurístico): idle + parte dinâmica + leakage
    idle = 0.10*tdp
    dyn = tdp*(carga_pct/100.0)*(0.80*profile)*freq_scale
    leak = 0.02*tdp*(1+0.05*(freq_scale-1.0))
    return max(0.0, idle+dyn+leak)

def compute_PLs(cpu):
    t=cpu.get("tdp",65); y=cpu.get("ano",2018)
    if y>=2022: return round(t*1.2,1), round(t*1.8,1), 28.0
    if y>=2017: return round(t*1.05,1), round(t*1.4,1), 20.0
    return round(t*1.0,1), round(t*1.2,1), 10.0

def derive_rth_heatsink(c):
    nome=c.get("modelo","").lower(); tipo=c.get("tipo","air").lower()
    if tipo=="aio":
        if "360" in nome: return 0.07
        if "280" in nome: return 0.09
        if "240" in nome or "h100" in nome: return 0.11
        return 0.10
    premium=["noctua","dark rock","true spirit","ak620"]
    if "hyper 212" in nome: return 0.16
    if any(k in nome for k in premium): return 0.12
    if any(k in nome for k in ["gammaxx","superframe","gamedias","glacier","tyr"]): return 0.18
    return 0.18

def cpu_r_cs(cpu):
    # R_cs = resistência térmica DIE/IHS→contato (°C/W) — aplicada internamente
    fab=cpu.get("fabricante","Intel").lower(); ano=cpu.get("ano",2018)
    if fab=="amd": return 0.25
    if ano>=2022: return 0.20
    if ano>=2015: return 0.22
    return 0.30

def fan_rpm(util): 
    idle, maxr = 600, 2200
    u=max(0.0,min(100.0,util))
    return idle if u<=15 else int(idle + (maxr-idle)*((u-15)/85.0))

def r_total(cpu,cooler,rpm):
    Rcs=cpu_r_cs(cpu); Rhs=derive_rth_heatsink(cooler)
    rpm_ref=1500.0
    if rpm<=0: rpm=rpm_ref
    Rhs_adj = Rhs * (rpm_ref/rpm)**0.8
    return Rcs + Rhs_adj

def estimate_noise(cooler,util):
    base=cooler.get("ruido_db",30)
    return round(base*(0.6+0.4*sqrt(min(1.0,util/100.0))),1)

def estimate_durability(cooler,util):
    b=cooler.get("durabilidade_anos",5)
    if util<=80: return b
    exc=(util-80)/20.0
    return max(1,int(b*(1.0-0.5*exc)))

# ---------------------------
# UI: seleção por ARQUITETURA então CPU
# ---------------------------
arqus = sorted({c["arquitetura"] for c in CPUS})
st.sidebar.markdown("### Seleção rápida")
arch = st.sidebar.selectbox("Arquitetura", ["(todas)"]+arqus, index=0)
filtered = CPUS if arch=="(todas)" else [c for c in CPUS if c["arquitetura"]==arch]
cpu_modelos = [f'{c["modelo"]} — {c["ano"]}' for c in filtered]
cpu_choice = st.sidebar.selectbox("CPU (filtrada por arquitetura)", cpu_modelos)
# map back
cpu = next((filtered[i] for i,v in enumerate(cpu_modelos) if v==cpu_choice), filtered[0] if filtered else None)

# filtro de tipo de cooler - permite mostrar listas separadas/ordenadas
cooler_type = st.sidebar.selectbox("Tipo de cooler", ("Todos","Air","AIO"))

# ordenar coolers por capacidade prática (tdp_nominal) — crescente: do pior ao melhor
# primeiro garantimos que tdp_nominal exista (foi calculado acima)
coolers_sorted = sorted(COOLERS, key=lambda x: x.get("tdp_nominal", 0.0))
# filtrar por tipo se necessário
if cooler_type == "Air":
    coolers_display = [c for c in coolers_sorted if c.get("tipo","Air").upper()=="AIR"]
elif cooler_type == "AIO":
    coolers_display = [c for c in coolers_sorted if c.get("tipo","AIO").upper()=="AIO"]
else:
    coolers_display = coolers_sorted

cooler_choice_label = [f'{c["modelo"]} — {c.get("tipo","Air")}' for c in coolers_display]
if not cooler_choice_label:
    cooler_choice_label = [f'{c["modelo"]} — {c.get("tipo","Air")}' for c in coolers_sorted]
cooler_choice = st.sidebar.selectbox("Cooler (ordenado do pior ao melhor)", cooler_choice_label)
# map back
cooler = next((c for c in coolers_display if f'{c["modelo"]} — {c.get("tipo","Air")}'==cooler_choice), coolers_sorted[0])

# antes de simular: condição do gabinete (disponível)
vent = st.sidebar.selectbox("Condição do gabinete", ("Bem ventilado","Moderado","Pouco ventilado"))
vent_factor = 1.0 if vent=="Bem ventilado" else (0.92 if vent=="Moderado" else 0.85)

# parâmetros principais
amb = st.sidebar.number_input("Temperatura ambiente (°C)", 10.0,45.0,25.0,0.5)
carga = st.sidebar.slider("Carga (percentual do TDP)", 10,150,100,1)
perfil = st.sidebar.selectbox("Perfil de carga", list(WORKLOAD_PROFILES.keys()), index=3)
freq_scale = st.sidebar.slider("Escala de frequência (%)", 80,140,100,1)/100.0

# ----------------------------------------
# EXIBIÇÃO SIMPLIFICADA DAS FREQUÊNCIAS (abaixo do slider)
# ----------------------------------------
st.sidebar.markdown("### Frequências do Processador")
st.sidebar.markdown(
    "Essas são as frequências principais do seu processador. "
    "A frequência aplicada é o valor que você escolheu no controle acima."
)

# seguro caso cpu seja None
base_freq_sidebar = cpu.get("frequencia_base", 0.0) if cpu else 0.0
turbo_freq_sidebar = cpu.get("frequencia_turbo", base_freq_sidebar) if cpu else 0.0

freq_aplicada_sidebar = base_freq_sidebar * freq_scale
if turbo_freq_sidebar and freq_aplicada_sidebar > turbo_freq_sidebar:
    freq_aplicada_sidebar = turbo_freq_sidebar

st.sidebar.write(f"**Frequência base:** {base_freq_sidebar:.2f} GHz")
st.sidebar.write(f"**Frequência turbo máxima:** {turbo_freq_sidebar:.2f} GHz")
st.sidebar.write(f"**Frequência aplicada:** {freq_aplicada_sidebar:.2f} GHz")

permitir_pl2 = st.sidebar.checkbox("Permitir burst PL2 (se aplicável)", value=True)
mostrar_graf = st.sidebar.checkbox("Mostrar gráfico detalhado", value=True)

# legendas / explicações (sempre visíveis)
with st.expander("Legenda e como funciona (resumo)"):
    st.markdown("""
    - **R_cs (°C/W)** — resistência interna DIE/IHS → contato (aplicada internamente). Ex.: *R_cs (case→heatsink °C/W)*.
    - **R_hs (°C/W)** — resistência do radiador/torre do cooler (atribuída automaticamente por tipo/tamanho).
    - **R_total = R_cs + R_hs'** → resistência total usada no cálculo (°C/W).
    - **ΔT = P × R_total** → aumento de temperatura acima do ambiente.
    - **Hotspot AMD**: para CPUs AMD aplicamos um offset interno simulando Tj > IHS.
    - **PL1 / PL2**: limites heurísticos para burst/sustentação (aplicados internamente).
    - **Observação:** usuário NÃO precisa informar resistências — elas são estimadas automaticamente por arquitetura e cooler.
    """)

# botão simular
if st.button("Simular"):
    if cpu is None or cooler is None:
        st.error("Selecione CPU e cooler válidos.")
    else:
        tdp_ref = cpu["tdp"]
        perfil_f = WORKLOAD_PROFILES.get(perfil,1.0)

        # -----------------------
        # FREQUÊNCIAS: base, turbo e frequência USADA no cálculo (considerando slider)
        # - freq_used_nominal = base * freq_scale
        # - se freq_used_nominal > turbo -> cap em turbo e ajusta freq_scale_for_calc
        # -----------------------
        base_freq = cpu.get("frequencia_base", 0.0)
        turbo_freq = cpu.get("frequencia_turbo", base_freq)
        freq_used_nominal = base_freq * freq_scale
        if turbo_freq and freq_used_nominal > turbo_freq:
            freq_used = turbo_freq
            freq_scale_for_calc = turbo_freq / base_freq if base_freq>0 else freq_scale
            freq_capped = True
        else:
            freq_used = freq_used_nominal
            freq_scale_for_calc = freq_scale
            freq_capped = False

        # potência/modelo usa o fator de frequência efetivo
        potencia_modelo = cpu_power_model(tdp_ref, carga, perfil_f, freq_scale_for_calc)
        PL1, PL2, TAU = compute_PLs(cpu)
        potencia_aplicada = min(potencia_modelo, PL2 if permitir_pl2 else PL1)
        nominal = cooler.get("tdp_nominal", round(0.85*cooler.get("tdp_manufacturer",0.0),1))
        nominal_v = nominal * vent_factor * (1.0 - BASE_SAFETY_PCT)
        dyn_pct = min(0.20, 0.15 * (potencia_aplicada / max(1.0, nominal_v)))
        cap_eff = nominal_v * (1.0 - dyn_pct)
        util_pct = round((potencia_aplicada / max(1.0, cap_eff)) * 100.0,1) if cap_eff>0 else 999.9
        rpm = fan_rpm(util_pct)
        Rtot = r_total(cpu, cooler, rpm)
        temp_steady = amb + potencia_aplicada * Rtot
        hotspot = cpu.get("fabricante","Intel").lower()=="amd"
        if hotspot: temp_steady += 8.0  # offset Tj vs IHS para AMD
        aviso_throttle = temp_steady >= 95.0
        ruido = estimate_noise(cooler, util_pct)
        dur = estimate_durability(cooler, util_pct)

        # saída
        st.markdown("## Resultado")
        st.write(f"**CPU:** {cpu['modelo']} — TDP referência: {tdp_ref} W — arquitetura: {cpu.get('arquitetura')}")
        # exibir frequências: base, turbo e usada no cálculo
        st.write(f"**Frequência base:** {base_freq:.2f} GHz • **Frequência turbo:** {turbo_freq:.2f} GHz")
        cap_note = " (capada ao turbo)" if freq_capped else ""
        st.write(f"**Frequência usada no cálculo:** {freq_used:.2f} GHz{cap_note} — escala efetiva utilizada: {freq_scale_for_calc:.2f}×")
        st.write(f"**Perfil:** {perfil} (fator {perfil_f:.2f}) • Escala freq (slider): {freq_scale:.2f}×")
        st.write(f"**Potência estimada (modelo):** {potencia_modelo:.1f} W")
        st.write(f"**Potência aplicada (após PL):** {potencia_aplicada:.1f} W  (PL1={PL1} W, PL2={PL2} W)")
        st.write(f"**Cooler:** {cooler['modelo']} — tipo: {cooler.get('tipo','Air')} — nominal ajustado: {nominal:.1f} W • ventilação: {vent}")
        st.write(f"**Capacidade efetiva do cooler:** {cap_eff:.1f} W (redução dinâmica {dyn_pct*100:.1f}%)")
        st.write(f"**Utilização da capacidade efetiva:** {util_pct}%")
        st.write(f"**RPM estimado:** {rpm} RPM")
        st.write(f"**Resistência térmica interna aplicada (R_total):** {Rtot:.3f} °C/W (estimada internamente)")
        st.write(f"**Temperatura estimada (steady, IHS aprox.):** {temp_steady:.1f} °C (ambiente {amb} °C)")
        if hotspot: st.write("⚠️ Hotspot AMD aplicado internamente (simula Tj > IHS).")
        if aviso_throttle: st.error("Risco: Temperatura estimada >= 95°C — possível throttling.")
        else: st.success("Temperatura estimada dentro de limites operacionais.")
        st.write(f"**Ruído estimado:** {ruido} dB • **Durabilidade estimada:** ~{dur} anos")

        # gráficos
        if mostrar_graf:
            cols = st.columns(2)
            with cols[0]:
                st.markdown("### Temperatura vs Potência aplicada")
                pvals = np.linspace(0.2*tdp_ref, max(tdp_ref*1.6,potencia_aplicada*1.2),40)
                temps = amb + pvals * Rtot + (8.0 if hotspot else 0.0)
                fig,ax=plt.subplots(figsize=(6,3)); ax.plot(pvals,temps,linewidth=2)
                ax.scatter([potencia_aplicada],[temp_steady],color='red',zorder=6)
                ax.set_xlabel("Potência (W)"); ax.set_ylabel("Temperatura estimada (°C)"); ax.grid(alpha=0.4,ls='--')
                st.pyplot(fig)
            with cols[1]:
                st.markdown("### Potência aplicada × Capacidade efetiva")
                fig2,ax2=plt.subplots(figsize=(5,3))
                ax2.bar(["Power(W)","Cap.Efetiva(W)"],[potencia_aplicada,cap_eff])
                for i,v in enumerate([potencia_aplicada,cap_eff]): ax2.text(i,v+max(1,0.02*v),f"{v:.1f}",ha='center')
                ax2.set_ylim(0,max(cap_eff,potencia_aplicada)*1.3 if max(cap_eff,potencia_aplicada)>0 else 1)
                st.pyplot(fig2)

        # tabela resumida
        df=pd.DataFrame([{
            "cpu":cpu['modelo'],"arquitetura":cpu.get("arquitetura"),"tdp_ref_W":tdp_ref,
            "freq_base_GHz":base_freq,"freq_turbo_GHz":turbo_freq,"freq_usada_GHz":round(freq_used,2),
            "pot_modelo_W":round(potencia_modelo,1),"pot_aplicada_W":round(potencia_aplicada,1),
            "cap_eff_W":round(cap_eff,1),"temp_steady_C":round(temp_steady,1),"util_pct":util_pct
        }])
        st.markdown("### Dados resumidos")
        st.dataframe(df)

st.markdown("---")
st.caption("Observação: O simulador usa heurísticas (R_cs, R_hs estimadas automaticamente). Para medições reais, use sensores e benchs controlados (HWiNFO, etc.).")
