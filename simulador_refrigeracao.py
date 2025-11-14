# simulador_refrigeracao_final_ptbr.py
# Simulador otimizado em Português (PT-BR)
# - Modelo térmico simplificado e realista (R_cs interno, R_hs por tipo de cooler)
# - PL1/PL2 heurísticos (burst) para CPUs
# - Perfis de carga (Gaming, Cinebench, AVX, etc.)
# - Saída em PT-BR com explicações resumidas (sem expor R_cs/R_hs ao usuário)
#
# Uso:
# pip install streamlit matplotlib numpy pandas
# streamlit run simulador_refrigeracao_final_ptbr.py

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt

st.set_page_config(page_title="Simulador de Refrigeração (PT-BR)", layout="wide")

# -------------------------
# DADOS: CPUs e COOLERS (mantidos conforme você enviou)
# -------------------------
CPUS = [
    {"modelo": "AMD Ryzen 5 1600X", "tdp": 95, "ano": 2017, "socket": "AM4",
     "frequencia_base": 3.6, "frequencia_turbo": 4.0, "arquitetura": "Zen", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 5 3600", "tdp": 65, "ano": 2019, "socket": "AM4",
     "frequencia_base": 3.6, "frequencia_turbo": 4.2, "arquitetura": "Zen 2", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 5 5600", "tdp": 65, "ano": 2021, "socket": "AM4",
     "frequencia_base": 3.5, "frequencia_turbo": 4.4, "arquitetura": "Zen 3", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 5 5600X", "tdp": 65, "ano": 2020, "socket": "AM4",
     "frequencia_base": 3.7, "frequencia_turbo": 4.6, "arquitetura": "Zen 3", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 5 5600X3D", "tdp": 105, "ano": 2022, "socket": "AM4",
     "frequencia_base": 3.3, "frequencia_turbo": 4.4, "arquitetura": "Zen 3 (3D)", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 5 5500X3D", "tdp": 105, "ano": 2024, "socket": "AM4",
     "frequencia_base": 3.0, "frequencia_turbo": 4.0, "arquitetura": "Zen 3 (3D)", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 5 7400F", "tdp": 65, "ano": 2024, "socket": "AM5",
     "frequencia_base": 3.7, "frequencia_turbo": 4.7, "arquitetura": "Zen 4", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 5 7500F", "tdp": 65, "ano": 2024, "socket": "AM5",
     "frequencia_base": 3.7, "frequencia_turbo": 5.0, "arquitetura": "Zen 4", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 5 7600", "tdp": 65, "ano": 2022, "socket": "AM5",
     "frequencia_base": 3.8, "frequencia_turbo": 5.1, "arquitetura": "Zen 4", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 5 7600X", "tdp": 105, "ano": 2022, "socket": "AM5",
     "frequencia_base": 4.7, "frequencia_turbo": 5.3, "arquitetura": "Zen 4", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 5 7600X3D", "tdp": 65, "ano": 2024, "socket": "AM5",
     "frequencia_base": 4.1, "frequencia_turbo": 4.7, "arquitetura": "Zen 4 (3D)", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 5 8400F", "tdp": 65, "ano": 2024, "socket": "AM5",
     "frequencia_base": 4.2, "frequencia_turbo": 4.7, "arquitetura": "Zen 5", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 5 8500G", "tdp": 65, "ano": 2024, "socket": "AM5",
     "frequencia_base": 3.5, "frequencia_turbo": 5.0, "arquitetura": "Zen 5 (G)", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 5 8600G", "tdp": 65, "ano": 2024, "socket": "AM5",
     "frequencia_base": 4.3, "frequencia_turbo": 5.0, "arquitetura": "Zen 5 (G)", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 5 9600X", "tdp": 65, "ano": 2024, "socket": "AM5",
     "frequencia_base": 3.9, "frequencia_turbo": 5.4, "arquitetura": "Zen 5", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 7 7700", "tdp": 65, "ano": 2023, "socket": "AM5",
     "frequencia_base": 3.8, "frequencia_turbo": 5.3, "arquitetura": "Zen 4", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 7 7700X", "tdp": 105, "ano": 2023, "socket": "AM5",
     "frequencia_base": 4.5, "frequencia_turbo": 5.4, "arquitetura": "Zen 4", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 7 5800X", "tdp": 105, "ano": 2020, "socket": "AM4",
     "frequencia_base": 3.8, "frequencia_turbo": 4.7, "arquitetura": "Zen 3", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 7 5800X3D", "tdp": 105, "ano": 2022, "socket": "AM4",
     "frequencia_base": 3.4, "frequencia_turbo": 4.5, "arquitetura": "Zen 3 (3D)", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 9 5900X", "tdp": 105, "ano": 2020, "socket": "AM4",
     "frequencia_base": 3.7, "frequencia_turbo": 4.8, "arquitetura": "Zen 3", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 9 5950X", "tdp": 105, "ano": 2020, "socket": "AM4",
     "frequencia_base": 3.4, "frequencia_turbo": 4.9, "arquitetura": "Zen 3", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 9 7950X", "tdp": 170, "ano": 2022, "socket": "AM5",
     "frequencia_base": 4.5, "frequencia_turbo": 5.7, "arquitetura": "Zen 4", "fabricante":"AMD"},
    {"modelo": "AMD Ryzen 9 7950X3D", "tdp": 120, "ano": 2023, "socket": "AM5",
     "frequencia_base": 4.2, "frequencia_turbo": 5.7, "arquitetura": "Zen 4 (3D)", "fabricante":"AMD"},
    {"modelo": "Intel Core 2 Duo E8400", "tdp": 65, "ano": 2008, "socket": "LGA775",
     "frequencia_base": 3.0, "frequencia_turbo": 3.0, "arquitetura": "Core (65nm)", "fabricante":"Intel"},
    {"modelo": "Intel Core i3-530", "tdp": 73, "ano": 2010, "socket": "LGA1156",
     "frequencia_base": 2.93, "frequencia_turbo": 3.06, "arquitetura": "Clarksfield", "fabricante":"Intel"},
    {"modelo": "Intel Core i3-3240", "tdp": 55, "ano": 2012, "socket": "LGA1155",
     "frequencia_base": 3.4, "frequencia_turbo": 3.4, "arquitetura": "Ivy Bridge", "fabricante":"Intel"},
    {"modelo": "Intel Core i7-920", "tdp": 130, "ano": 2008, "socket": "LGA1366",
     "frequencia_base": 2.66, "frequencia_turbo": 2.93, "arquitetura": "Nehalem", "fabricante":"Intel"},
    {"modelo": "Intel Core i3-6100", "tdp": 51, "ano": 2015, "socket": "LGA1151",
     "frequencia_base": 3.7, "frequencia_turbo": 3.7, "arquitetura": "Skylake", "fabricante":"Intel"},
    {"modelo": "Intel Core i5-6600K", "tdp": 91, "ano": 2015, "socket": "LGA1151",
     "frequencia_base": 3.5, "frequencia_turbo": 3.9, "arquitetura": "Skylake", "fabricante":"Intel"},
    {"modelo": "Intel Core i5-8400", "tdp": 65, "ano": 2018, "socket": "LGA1151",
     "frequencia_base": 2.8, "frequencia_turbo": 4.0, "arquitetura": "Coffee Lake", "fabricante":"Intel"},
    {"modelo": "Intel Core i5-10400F", "tdp": 65, "ano": 2020, "socket": "LGA1200",
     "frequencia_base": 2.9, "frequencia_turbo": 4.3, "arquitetura": "Comet Lake", "fabricante":"Intel"},
    {"modelo": "Intel Core i5-10600K", "tdp": 125, "ano": 2020, "socket": "LGA1200",
     "frequencia_base": 4.1, "frequencia_turbo": 4.8, "arquitetura": "Comet Lake", "fabricante":"Intel"},
    {"modelo": "Intel Core i5-12400F", "tdp": 65, "ano": 2022, "socket": "LGA1700",
     "frequencia_base": 2.5, "frequencia_turbo": 4.4, "arquitetura": "Alder Lake", "fabricante":"Intel"},
    {"modelo": "Intel Core i5-13400F", "tdp": 65, "ano": 2023, "socket": "LGA1700",
     "frequencia_base": 2.5, "frequencia_turbo": 4.6, "arquitetura": "Raptor Lake", "fabricante":"Intel"},
    {"modelo": "Intel Core i5-14600K", "tdp": 180, "ano": 2024, "socket": "LGA1700",
     "frequencia_base": 3.1, "frequencia_turbo": 5.1, "arquitetura": "Raptor Lake Refresh", "fabricante":"Intel"},
    {"modelo": "Intel Core i7-11700K", "tdp": 125, "ano": 2021, "socket": "LGA1200",
     "frequencia_base": 3.6, "frequencia_turbo": 5.0, "arquitetura": "Rocket Lake", "fabricante":"Intel"},
    {"modelo": "Intel Core i7-12700K", "tdp": 190, "ano": 2022, "socket": "LGA1700",
     "frequencia_base": 3.6, "frequencia_turbo": 5.0, "arquitetura": "Alder Lake", "fabricante":"Intel"},
    {"modelo": "Intel Core i7-13700K", "tdp": 250, "ano": 2023, "socket": "LGA1700",
     "frequencia_base": 3.4, "frequencia_turbo": 5.4, "arquitetura": "Raptor Lake", "fabricante":"Intel"},
    {"modelo": "Intel Core i9-10900K", "tdp": 125, "ano": 2020, "socket": "LGA1200",
     "frequencia_base": 3.7, "frequencia_turbo": 5.3, "arquitetura": "Comet Lake", "fabricante":"Intel"},
    {"modelo": "Intel Core i9-12900K", "tdp": 240, "ano": 2022, "socket": "LGA1700",
     "frequencia_base": 3.2, "frequencia_turbo": 5.2, "arquitetura": "Alder Lake", "fabricante":"Intel"},
    {"modelo": "Intel Core i9-13900K", "tdp": 250, "ano": 2023, "socket": "LGA1700",
     "frequencia_base": 3.0, "frequencia_turbo": 5.8, "arquitetura": "Raptor Lake", "fabricante":"Intel"},
    {"modelo": "Intel Core i9-14900K", "tdp": 250, "ano": 2024, "socket": "LGA1700",
     "frequencia_base": 3.2, "frequencia_turbo": 6.0, "arquitetura": "Raptor Lake Refresh", "fabricante":"Intel"},
    {"modelo": "Intel Xeon E5-2666 v3", "tdp": 115, "ano": 2014, "socket": "LGA2011-v3",
     "frequencia_base": 2.9, "frequencia_turbo": 3.5, "arquitetura": "Haswell-EP", "fabricante":"Intel"},
    {"modelo": "Intel Xeon E5-2667 v3", "tdp": 135, "ano": 2014, "socket": "LGA2011-v3",
     "frequencia_base": 3.2, "frequencia_turbo": 3.6, "arquitetura": "Haswell-EP", "fabricante":"Intel"},
    {"modelo": "Intel Xeon E5-2667 v4", "tdp": 160, "ano": 2016, "socket": "LGA2011-v3",
     "frequencia_base": 3.2, "frequencia_turbo": 3.7, "arquitetura": "Broadwell-EP", "fabricante":"Intel"},
    {"modelo": "Intel Xeon E5-2680 v4", "tdp": 120, "ano": 2016, "socket": "LGA2011-v3",
     "frequencia_base": 2.4, "frequencia_turbo": 3.3, "arquitetura": "Broadwell-EP", "fabricante":"Intel"},
    {"modelo": "Intel Xeon E5-1660 v3", "tdp": 140, "ano": 2014, "socket": "LGA2011-v3",
     "frequencia_base": 3.0, "frequencia_turbo": 3.7, "arquitetura": "Haswell-EP", "fabricante":"Intel"},
    {"modelo": "Intel Xeon E5-2680 v3", "tdp": 135, "ano": 2014, "socket": "LGA2011-v3",
     "frequencia_base": 2.5, "frequencia_turbo": 3.3, "arquitetura": "Haswell-EP", "fabricante":"Intel"},
    {"modelo": "Intel Xeon E5-2690 v3", "tdp": 135, "ano": 2014, "socket": "LGA2011-v3",
     "frequencia_base": 2.6, "frequencia_turbo": 3.5, "arquitetura": "Haswell-EP", "fabricante":"Intel"},
    {"modelo": "Intel Xeon E5-2670 v3", "tdp": 120, "ano": 2014, "socket": "LGA2011-v3",
     "frequencia_base": 2.3, "frequencia_turbo": 3.1, "arquitetura": "Haswell-EP", "fabricante":"Intel"},
    {"modelo": "Intel Xeon E5-2699 v4", "tdp": 145, "ano": 2016, "socket": "LGA2011-v3",
     "frequencia_base": 2.2, "frequencia_turbo": 3.6, "arquitetura": "Broadwell-EP", "fabricante":"Intel"},
    {"modelo": "AMD FX-8350", "tdp": 125, "ano": 2012, "socket": "AM3+",
     "frequencia_base": 4.0, "frequencia_turbo": 4.2, "arquitetura": "Piledriver", "fabricante":"AMD"},
]

COOLERS = [
    {"modelo": "SuperFrame SuperFlow 450 (Air)", "tipo": "Air", "tdp_manufacturer": 95, "ruido_db": 25, "durabilidade_anos": 4},
    {"modelo": "Gamdias Boreas E1-410 (Air)", "tipo": "Air", "tdp_manufacturer": 95, "ruido_db": 28, "durabilidade_anos": 4},
    {"modelo": "TGT Glacier 120 (Air)", "tipo": "Air", "tdp_manufacturer": 100, "ruido_db": 36, "durabilidade_anos": 3},
    {"modelo": "DeepCool Gammaxx 400 (Air)", "tipo": "Air", "tdp_manufacturer": 120, "ruido_db": 38, "durabilidade_anos": 4},
    {"modelo": "Redragon TYR (Air)", "tipo": "Air", "tdp_manufacturer": 130, "ruido_db": 22, "durabilidade_anos": 4},
    {"modelo": "Cooler Master Hyper 212 (Air)", "tipo": "Air", "tdp_manufacturer": 150, "ruido_db": 35, "durabilidade_anos": 5},
    {"modelo": "DeepCool AK500S (Air)", "tipo": "Air", "tdp_manufacturer": 150, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Thermalright TRUE Spirit 140 (Air)", "tipo": "Air", "tdp_manufacturer": 200, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Arctic Freezer 34 (Air)", "tipo": "Air", "tdp_manufacturer": 180, "ruido_db": 28, "durabilidade_anos": 5},
    {"modelo": "DeepCool AK400 (Air)", "tipo": "Air", "tdp_manufacturer": 220, "ruido_db": 29, "durabilidade_anos": 6},
    {"modelo": "DeepCool Gammaxx AG400 (Air)", "tipo": "Air", "tdp_manufacturer": 220, "ruido_db": 28, "durabilidade_anos": 4},
    {"modelo": "GameMax Sigma 520 (Air)", "tipo": "Air", "tdp_manufacturer": 220, "ruido_db": 30, "durabilidade_anos": 5},
    {"modelo": "Rise Mode Storm 8 (Air)", "tipo": "Air", "tdp_manufacturer": 280, "ruido_db": 30, "durabilidade_anos": 5},
    {"modelo": "Be Quiet! Dark Rock Pro 4 (Air)", "tipo": "Air", "tdp_manufacturer": 250, "ruido_db": 24, "durabilidade_anos": 7},
    {"modelo": "Noctua NH-D15 (Air)", "tipo": "Air", "tdp_manufacturer": 250, "ruido_db": 24, "durabilidade_anos": 8},
    {"modelo": "DeepCool AK620 (Air)", "tipo": "Air", "tdp_manufacturer": 260, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Rise Mode Black 240 (Water)", "tipo": "AIO", "tdp_manufacturer": 250, "ruido_db": 30, "durabilidade_anos": 5},
    {"modelo": "GameMax IceBurg 240 (Water)", "tipo": "AIO", "tdp_manufacturer": 245, "ruido_db": 31, "durabilidade_anos": 6},
    {"modelo": "Corsair H100i (AIO 240) (Water)", "tipo": "AIO", "tdp_manufacturer": 300, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Arctic Liquid Freezer II 240 (Water)", "tipo": "AIO", "tdp_manufacturer": 320, "ruido_db": 27, "durabilidade_anos": 7},
    {"modelo": "TGT Storm 240 (Water)", "tipo": "AIO", "tdp_manufacturer": 280, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "DeepCool LS720 (AIO 360) (Water)", "tipo": "AIO", "tdp_manufacturer": 300, "ruido_db": 32, "durabilidade_anos": 7},
    {"modelo": "Corsair H150i (AIO 360)", "tipo": "AIO", "tdp_manufacturer": 350, "ruido_db": 30, "durabilidade_anos": 7},
    {"modelo": "NZXT Kraken X63 (AIO 280)", "tipo": "AIO", "tdp_manufacturer": 350, "ruido_db": 29, "durabilidade_anos": 7},
    {"modelo": "DeepCool Castle 360EX (AIO 360)", "tipo": "AIO", "tdp_manufacturer": 350, "ruido_db": 31, "durabilidade_anos": 7},
    {"modelo": "Rise Mode Gamer Black 240 (AIO)", "tipo": "AIO", "tdp_manufacturer": 220, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Pichau AIO 240 (Water)", "tipo": "AIO", "tdp_manufacturer": 270, "ruido_db": 34, "durabilidade_anos": 5},
    {"modelo": "Husky Hunter 240 (AIO)", "tipo": "AIO", "tdp_manufacturer": 260, "ruido_db": 33, "durabilidade_anos": 5},
]

# aplica tdp_nominal simplificado (por compatibilidade)
for c in COOLERS:
    c["tdp_nominal"] = round(0.85 * c.get("tdp_manufacturer", 0.0), 1)

# -------------------------
# PARÂMETROS GLOBAIS E PERFIS
# -------------------------
BASE_SAFETY_PCT = 0.10  # redução conservadora aplicada à capacidade do cooler

WORKLOAD_PROFILES = {
    "Idle / Leve": 0.15,
    "Navegação / Escritório": 0.30,
    "Jogos (típico)": 0.55,
    "Bench sustentado (Cinebench)": 1.00,
    "AVX/Prime (pesado)": 1.30
}

# -------------------------
# FUNÇÕES AUXILIARES (internas)
# -------------------------
def avg_frequency(cpu):
    b = cpu.get("frequencia_base", 3.5)
    t = cpu.get("frequencia_turbo", b)
    return (b + t) / 2.0

def cpu_power_model(tdp_ref, carga_pct, profile_factor=1.0, freq_scale=1.0):
    """
    Modelo heurístico de potência (W).
    - tdp_ref: TDP do fabricante (W)
    - carga_pct: 0..100 (slider)
    - profile_factor: perfil (WORKLOAD_PROFILES)
    - freq_scale: fator de frequência (1.0 padrão)
    Retorna potência estimada em W.
    """
    idle = 0.10 * tdp_ref
    dynamic = tdp_ref * (carga_pct / 100.0) * (0.80 * profile_factor) * freq_scale
    leakage = 0.02 * tdp_ref * (1.0 + 0.05 * (freq_scale - 1.0))
    return max(0.0, idle + dynamic + leakage)

def compute_PLs(cpu):
    """
    Heurística para PL1/PL2/Tau (em segundos).
    Valores são aproximados para modelar burst/limites.
    """
    tdp = cpu.get("tdp", 65)
    ano = cpu.get("ano", 2018)
    if ano >= 2022:
        pl1 = tdp * 1.2
        pl2 = tdp * 1.8
        tau = 28.0
    elif ano >= 2017:
        pl1 = tdp * 1.05
        pl2 = tdp * 1.4
        tau = 20.0
    else:
        pl1 = tdp * 1.0
        pl2 = tdp * 1.2
        tau = 10.0
    return round(pl1,1), round(pl2,1), tau

def derive_rth_heatsink_por_cooler(cooler):
    """
    Atribui uma resistência térmica (°C/W) aproximada ao cooler
    com base em tipo / tamanho. Interno — não exibido ao usuário.
    """
    tipo = cooler.get("tipo","Air").lower()
    nome = cooler.get("modelo","").lower()
    # heurísticas simples por palavra-chave e tipo
    if tipo == "aio":
        # diferenciar por '360', '280', '240'
        if "360" in nome:
            return 0.07
        if "280" in nome:
            return 0.09
        if "240" in nome or "h100" in nome:
            return 0.11
        return 0.10
    # air coolers
    # premium tower
    premium_keywords = ["noctua","dark rock","true spirit","ak620","hyper 212" ]
    if any(k in nome for k in premium_keywords):
        # hyper 212 é mid-range; tratamos separado
        if "hyper 212" in nome:
            return 0.16
        if "noctua" in nome or "dark rock" in nome or "ak620" in nome:
            return 0.12
        return 0.15
    # pequenas torres / single fan
    if any(k in nome for k in ["gammaxx","superframe","gamedias","glacier","tyr"]):
        return 0.18
    # default air
    return 0.18

def cpu_r_cs_interno(cpu):
    """
    Determina internamente R_cs (°C/W) por fabricante/era.
    Não exposto ao usuário.
    """
    fab = cpu.get("fabricante","Intel")
    ano = cpu.get("ano",2018)
    if fab.lower() == "amd":
        # Ryzen frequentemente tem hotspot mayor; aproximamos com R_cs maior
        return 0.25
    # Intel e Xeon
    if ano >= 2022:
        return 0.20
    if ano >= 2015:
        return 0.22
    return 0.30

def rth_total_interno(cpu, cooler, rpm):
    """
    Combina R_cs (interno), R_cs->heatsink (user-independent) e R_sh (heatsink),
    retornando R_total (°C/W).
    """
    R_cs = cpu_r_cs_interno(cpu)            # DIE/IHS -> contato
    R_hs_nominal = derive_rth_heatsink_por_cooler(cooler)
    # efeito RPM (quanto maior RPM, menor R_hs)
    rpm_ref = 1500.0
    if rpm <= 0: rpm = rpm_ref
    R_hs = R_hs_nominal * (rpm_ref / rpm) ** 0.8
    return R_cs + R_hs  # R_total (°C/W)

def fan_rpm_por_util(util_pct):
    """
    Curva simples de rpm baseada em utilização percentual.
    """
    idle = 600
    maxrpm = 2200
    u = max(0.0, min(100.0, util_pct))
    if u <= 15:
        return idle
    return int(idle + (maxrpm - idle) * ((u - 15) / 85.0))

def estimate_durability(cooler, util_pct):
    """
    Estimativa simples de durabilidade em anos baseada em uso.
    """
    base = cooler.get("durabilidade_anos",5)
    if util_pct <= 80:
        return base
    excess = (util_pct - 80)/20.0
    return max(1, int(base * (1.0 - 0.5 * excess)))

# -------------------------
# INTERFACE (PT-BR)
# -------------------------
st.title("Simulador de Refrigeração — Versão Final (PT-BR)")
st.markdown("Selecione CPU, cooler e perfil de carga. Resultados e explicações resumidas aparecem abaixo.")

with st.expander("Como este simulador calcula (resumo)"):
    st.markdown("""
    - **R_cs** (interno): resistência térmica entre DIE/IHS e o ponto de contato com o cooler — *aplicada internamente* (não solicite ao usuário).
    - **R_hs** (interno): resistência térmica do radiador / torre do cooler — atribuída automaticamente com base no modelo.
    - **ΔT = P × R_total**: elevação térmica (°C) obtida multiplicando a potência dissipada pela resistência térmica total.
    - **Hotspot AMD**: para CPUs AMD adicionamos um offset de hotspot automaticamente (simula a diferença Tj vs IHS).
    - **PL1 / PL2 / Tau**: limites de potência sustentada e burst são aplicados heurísticamente (Intel e CPUs modernas).
    - **Perfil de carga** influencia a potência (ex.: AVX > Cinebench > jogos).
    """)

col_esq, col_dir = st.columns((2,1))

with col_dir:
    st.subheader("Painel de calibração (opcional)")
    # knobs simples — exibir explicação em PT-BR
    safety_pct = st.slider("Redução base da capacidade do cooler (%)", 0.0, 30.0, 10.0, 1.0)/100.0
    cth = st.slider("Inércia térmica (C_th, J/°C) — afeta transientes", 100.0, 2000.0, 350.0, 10.0)
    st.caption("Ajuste se souber medições reais (padrões já calibrados para uso geral).")

with col_esq:
    cpu_sel = st.selectbox("Processador", [c["modelo"] for c in CPUS])
    cooler_sel = st.selectbox("Cooler", [c["modelo"] for c in COOLERS])
    ambiente = st.number_input("Temperatura ambiente (°C)", 10.0, 45.0, 25.0, 0.5)
    carga_slider = st.slider("Carga (percentual do TDP)", 10, 150, 100, 1)
    perfil = st.selectbox("Tipo de carga (perfil)", list(WORKLOAD_PROFILES.keys()), index=3)
    freq_scale = st.slider("Escala de frequência (%)", 80, 140, 100, 1)/100.0
    permitir_pl2 = st.checkbox("Permitir burst PL2 (se aplicável)", value=True)
    mostrar_transiente = st.checkbox("Mostrar gráfico transiente (tempo x temperatura)", value=True)

    if st.button("Simular"):
        cpu = next(c for c in CPUS if c["modelo"] == cpu_sel)
        cooler = next(c for c in COOLERS if c["modelo"] == cooler_sel)
        tdp_ref = cpu["tdp"]
        perfil_fator = WORKLOAD_PROFILES.get(perfil, 1.0)

        # potência gerada pelo perfil (modelo)
        potencia_modelo = cpu_power_model(tdp_ref, carga_slider, perfil_fator, freq_scale)

        # PLs heurísticos
        PL1, PL2, TAU = compute_PLs(cpu)

        # aplicar limites PL
        if permitir_pl2:
            potencia_aplicada = min(potencia_modelo, PL2)
        else:
            potencia_aplicada = min(potencia_modelo, PL1)

        # capacidade do cooler (nominal ajustado)
        nominal = cooler.get("tdp_nominal", 0.0)
        # ventilação do gabinete (pequeno efeito)
        vent_choice = st.radio("Condição do gabinete", ("Bem ventilado", "Moderado", "Pouco ventilado"), index=0)
        vent_factor = 1.0 if vent_choice == "Bem ventilado" else (0.92 if vent_choice == "Moderado" else 0.85)
        nominal_v = nominal * vent_factor * (1.0 - safety_pct)
        dyn_pct = min(0.20, 0.15 * (potencia_aplicada / max(1.0, nominal_v)))
        capacidade_efetiva = nominal_v * (1.0 - dyn_pct)

        util_pct = round((potencia_aplicada / max(1.0, capacidade_efetiva)) * 100.0, 1) if capacidade_efetiva>0 else 999.9
        rpm = fan_rpm_por_util(util_pct)
        rth_total = rth_total_interno(cpu, cooler, rpm)  # R_total interno (°C/W)
        temp_steady = ambiente + potencia_aplicada * rth_total

        # aplicar hotspot AMD (não mostrado como R separado)
        if cpu.get("fabricante","Intel").lower() == "amd":
            # acrescenta um offset para simular hotspot/Tj
            temp_steady += 8.0  # valor conservador (pode calibrar)
            hotspot_aplicado = True
        else:
            hotspot_aplicado = False

        # throttling heurístico
        aviso_throttle = temp_steady >= 95.0

        # ruído estimado
        ruido = round(cooler.get("ruido_db",30) * (0.6 + 0.4 * sqrt(min(1.0, util_pct/100.0))),1)
        durabilidade = estimate_durability(cooler, util_pct)

        # Saída (PT-BR)
        st.markdown("## Resultado — Resumo")
        st.write(f"**CPU:** {cpu['modelo']} — TDP referência: {tdp_ref} W")
        st.write(f"**Perfil de carga:** {perfil} (fator ≈ {perfil_fator:.2f}) • Escala de frequência: {freq_scale:.2f}×")
        st.write(f"**Potência estimada (modelo):** {potencia_modelo:.1f} W")
        st.write(f"**Potência aplicada (após PL/limites):** {potencia_aplicada:.1f} W  (PL1={PL1} W, PL2={PL2} W, Tau={TAU}s)")
        st.write(f"**Cooler:** {cooler['modelo']} — nominal aplicado: {nominal:.1f} W (ajustado por ventilação e safety)")
        st.write(f"**Capacidade efetiva do cooler:** {capacidade_efetiva:.1f} W (redução dinâmica {dyn_pct*100:.1f}%)")
        st.write(f"**Utilização da capacidade efetiva:** {util_pct}%")
        st.write(f"**RPM estimado (fan curve):** {rpm} RPM")
        st.write(f"**Temperatura estimada (steady):** {temp_steady:.1f} °C (ambiente {ambiente} °C)")
        if hotspot_aplicado:
            st.write("⚠️ Hotspot AMD aplicado internamente (simula Tj > IHS).")
        if aviso_throttle:
            st.error("Risco: Temperatura estimada >= 95°C — possível throttling/proteção térmica.")
        else:
            st.success("Temperatura estimada dentro de limites operacionais.")

        st.write(f"**Ruído estimado:** {ruido} dB")
        st.write(f"**Durabilidade estimada:** ~{durabilidade} anos")

        # Gráficos
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Gráfico: Temperatura steady vs Potência")
            p_vals = np.linspace(0.2*tdp_ref, max(tdp_ref*1.6, potencia_aplicada*1.2), 40)
            temps = ambiente + p_vals * rth_total + (8.0 if hotspot_aplicado else 0.0)
            fig, ax = plt.subplots(figsize=(6,3))
            ax.plot(p_vals, temps, linewidth=2)
            ax.scatter([potencia_aplicada],[temp_steady], color='red', zorder=5)
            ax.set_xlabel("Potência (W)")
            ax.set_ylabel("Temperatura estimada (°C)")
            ax.grid(alpha=0.4, linestyle='--')
            st.pyplot(fig)

        with col2:
            st.markdown("### Comparativo: Potência x Capacidade")
            fig2, ax2 = plt.subplots(figsize=(5,3))
            labels = ["Power aplicada (W)", "Capacidade efetiva (W)"]
            values = [potencia_aplicada, capacidade_efetiva]
            bars = ax2.bar(labels, values)
            for i,v in enumerate(values):
                ax2.text(i, v + max(1, 0.02*v), f"{v:.1f}", ha='center')
            ax2.set_ylim(0, max(values) * 1.3 if max(values)>0 else 1)
            st.pyplot(fig2)

        # Tabela resumida (copiável)
        tabela = pd.DataFrame([{
            "cpu": cpu['modelo'],
            "tdp_ref_W": tdp_ref,
            "potencia_modelo_W": round(potencia_modelo,1),
            "potencia_aplicada_W": round(potencia_aplicada,1),
            "capacidade_efetiva_W": round(capacidade_efetiva,1),
            "temp_steady_C": round(temp_steady,1),
            "rpm": rpm,
            "util_pct": util_pct
        }])
        st.markdown("### Dados resumidos (tabela)")
        st.dataframe(tabela)

        # Transiente (opcional)
        if mostrar_transiente:
            st.markdown("### Simulação transiente (curva tempo x temperatura) — simplificada")
            # perfil de potência: começa leve e sobe para potência_aplicada em t=5s, se PL2 for usado, faz burst por TAU
            def perfil_potencia(t):
                if t < 5: return cpu_power_model(tdp_ref, 10.0, 0.5, freq_scale)
                if permitir_pl2 and potencia_modelo > PL1:
                    if t < 5 + TAU:
                        return min(potencia_modelo, PL2)
                    else:
                        return min(potencia_modelo, PL1)
                return potencia_aplicada

            dt = 1.0
            t_total = 180.0
            times = np.arange(0.0, t_total + dt, dt)
            T = np.zeros_like(times)
            T[0] = ambiente
            C_th = cth
            for i in range(1, len(times)):
                P = perfil_potencia(times[i-1])
                dTdt = (P - (T[i-1] - ambiente) / rth_total) / C_th
                T[i] = T[i-1] + dTdt * dt
            fig3, ax3 = plt.subplots(figsize=(8,3))
            ax3.plot(times, T, linewidth=2)
            ax3.set_xlabel("Tempo (s)"); ax3.set_ylabel("Temp (°C)")
            ax3.grid(alpha=0.4, linestyle='--')
            st.pyplot(fig3)

st.markdown("---")
st.caption("Este simulador usa heurísticas e aproximações para se aproximar de medições reais. Para alta fidelidade, calibre usando medições locais (HWInfo, sensores e benchs controlados).")
