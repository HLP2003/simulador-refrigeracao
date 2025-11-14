# simulador_refrigeracao_final.py
# Simulador otimizado + realista (steady + transiente, PL1/PL2, fan-curve, throttling)
# Requisitos: streamlit, matplotlib, numpy, pandas
# Uso: streamlit run simulador_refrigeracao_final.py

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import sqrt

st.set_page_config(page_title="Simulador de Refrigeração — Final", layout="wide")

# --------------------------
# DATABASE: usei EXATAMENTE as listas que você enviou
# --------------------------
CPUS = [
    {"modelo": "AMD Ryzen 5 1600X", "tdp": 95, "ano": 2017, "socket": "AM4", "frequencia_base": 3.6, "frequencia_turbo": 4.0, "arquitetura": "Zen"},
    {"modelo": "AMD Ryzen 5 3600", "tdp": 65, "ano": 2019, "socket": "AM4", "frequencia_base": 3.6, "frequencia_turbo": 4.2, "arquitetura": "Zen 2"},
    {"modelo": "AMD Ryzen 5 5600", "tdp": 65, "ano": 2021, "socket": "AM4", "frequencia_base": 3.5, "frequencia_turbo": 4.4, "arquitetura": "Zen 3"},
    {"modelo": "AMD Ryzen 5 5600X", "tdp": 65, "ano": 2020, "socket": "AM4", "frequencia_base": 3.7, "frequencia_turbo": 4.6, "arquitetura": "Zen 3"},
    {"modelo": "AMD Ryzen 5 5600X3D", "tdp": 105, "ano": 2022, "socket": "AM4", "frequencia_base": 3.3, "frequencia_turbo": 4.4, "arquitetura": "Zen 3 (3D)"},
    {"modelo": "AMD Ryzen 5 5500X3D", "tdp": 105, "ano": 2024, "socket": "AM4", "frequencia_base": 3.0, "frequencia_turbo": 4.0, "arquitetura": "Zen 3 (3D)"},
    {"modelo": "AMD Ryzen 5 7400F", "tdp": 65, "ano": 2024, "socket": "AM5", "frequencia_base": 3.7, "frequencia_turbo": 4.7, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 5 7500F", "tdp": 65, "ano": 2024, "socket": "AM5", "frequencia_base": 3.7, "frequencia_turbo": 5.0, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 5 7600", "tdp": 65, "ano": 2022, "socket": "AM5", "frequencia_base": 3.8, "frequencia_turbo": 5.1, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 5 7600X", "tdp": 105, "ano": 2022, "socket": "AM5", "frequencia_base": 4.7, "frequencia_turbo": 5.3, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 5 7600X3D", "tdp": 65, "ano": 2024, "socket": "AM5", "frequencia_base": 4.1, "frequencia_turbo": 4.7, "arquitetura": "Zen 4 (3D)"},
    {"modelo": "AMD Ryzen 5 8400F", "tdp": 65, "ano": 2024, "socket": "AM5", "frequencia_base": 4.2, "frequencia_turbo": 4.7, "arquitetura": "Zen 5"},
    {"modelo": "AMD Ryzen 5 8500G", "tdp": 65, "ano": 2024, "socket": "AM5", "frequencia_base": 3.5, "frequencia_turbo": 5.0, "arquitetura": "Zen 5 (G)"},
    {"modelo": "AMD Ryzen 5 8600G", "tdp": 65, "ano": 2024, "socket": "AM5", "frequencia_base": 4.3, "frequencia_turbo": 5.0, "arquitetura": "Zen 5 (G)"},
    {"modelo": "AMD Ryzen 5 9600X", "tdp": 65, "ano": 2024, "socket": "AM5", "frequencia_base": 3.9, "frequencia_turbo": 5.4, "arquitetura": "Zen 5"},
    {"modelo": "AMD Ryzen 7 7700", "tdp": 65, "ano": 2023, "socket": "AM5", "frequencia_base": 3.8, "frequencia_turbo": 5.3, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 7 7700X", "tdp": 105, "ano": 2023, "socket": "AM5", "frequencia_base": 4.5, "frequencia_turbo": 5.4, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 7 5800X", "tdp": 105, "ano": 2020, "socket": "AM4", "frequencia_base": 3.8, "frequencia_turbo": 4.7, "arquitetura": "Zen 3"},
    {"modelo": "AMD Ryzen 7 5800X3D", "tdp": 105, "ano": 2022, "socket": "AM4", "frequencia_base": 3.4, "frequencia_turbo": 4.5, "arquitetura": "Zen 3 (3D)"},
    {"modelo": "AMD Ryzen 9 5900X", "tdp": 105, "ano": 2020, "socket": "AM4", "frequencia_base": 3.7, "frequencia_turbo": 4.8, "arquitetura": "Zen 3"},
    {"modelo": "AMD Ryzen 9 5950X", "tdp": 105, "ano": 2020, "socket": "AM4", "frequencia_base": 3.4, "frequencia_turbo": 4.9, "arquitetura": "Zen 3"},
    {"modelo": "AMD Ryzen 9 7950X", "tdp": 170, "ano": 2022, "socket": "AM5", "frequencia_base": 4.5, "frequencia_turbo": 5.7, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 9 7950X3D", "tdp": 120, "ano": 2023, "socket": "AM5", "frequencia_base": 4.2, "frequencia_turbo": 5.7, "arquitetura": "Zen 4 (3D)"},
    {"modelo": "Intel Core 2 Duo E8400", "tdp": 65, "ano": 2008, "socket": "LGA775", "frequencia_base": 3.0, "frequencia_turbo": 3.0, "arquitetura": "Core (65nm)"},
    {"modelo": "Intel Core i3-530", "tdp": 73, "ano": 2010, "socket": "LGA1156", "frequencia_base": 2.93, "frequencia_turbo": 3.06, "arquitetura": "Clarksfield"},
    {"modelo": "Intel Core i3-3240", "tdp": 55, "ano": 2012, "socket": "LGA1155", "frequencia_base": 3.4, "frequencia_turbo": 3.4, "arquitetura": "Ivy Bridge"},
    {"modelo": "Intel Core i7-920", "tdp": 130, "ano": 2008, "socket": "LGA1366", "frequencia_base": 2.66, "frequencia_turbo": 2.93, "arquitetura": "Nehalem"},
    {"modelo": "Intel Core i3-6100", "tdp": 51, "ano": 2015, "socket": "LGA1151", "frequencia_base": 3.7, "frequencia_turbo": 3.7, "arquitetura": "Skylake"},
    {"modelo": "Intel Core i5-6600K", "tdp": 91, "ano": 2015, "socket": "LGA1151", "frequencia_base": 3.5, "frequencia_turbo": 3.9, "arquitetura": "Skylake"},
    {"modelo": "Intel Core i5-8400", "tdp": 65, "ano": 2018, "socket": "LGA1151", "frequencia_base": 2.8, "frequencia_turbo": 4.0, "arquitetura": "Coffee Lake"},
    {"modelo": "Intel Core i5-10400F", "tdp": 65, "ano": 2020, "socket": "LGA1200", "frequencia_base": 2.9, "frequencia_turbo": 4.3, "arquitetura": "Comet Lake"},
    {"modelo": "Intel Core i5-10600K", "tdp": 125, "ano": 2020, "socket": "LGA1200", "frequencia_base": 4.1, "frequencia_turbo": 4.8, "arquitetura": "Comet Lake"},
    {"modelo": "Intel Core i5-12400F", "tdp": 65, "ano": 2022, "socket": "LGA1700", "frequencia_base": 2.5, "frequencia_turbo": 4.4, "arquitetura": "Alder Lake"},
    {"modelo": "Intel Core i5-13400F", "tdp": 65, "ano": 2023, "socket": "LGA1700", "frequencia_base": 2.5, "frequencia_turbo": 4.6, "arquitetura": "Raptor Lake"},
    {"modelo": "Intel Core i5-14600K", "tdp": 180, "ano": 2024, "socket": "LGA1700", "frequencia_base": 3.1, "frequencia_turbo": 5.1, "arquitetura": "Raptor Lake Refresh"},
    {"modelo": "Intel Core i7-11700K", "tdp": 125, "ano": 2021, "socket": "LGA1200", "frequencia_base": 3.6, "frequencia_turbo": 5.0, "arquitetura": "Rocket Lake"},
    {"modelo": "Intel Core i7-12700K", "tdp": 190, "ano": 2022, "socket": "LGA1700", "frequencia_base": 3.6, "frequencia_turbo": 5.0, "arquitetura": "Alder Lake"},
    {"modelo": "Intel Core i7-13700K", "tdp": 250, "ano": 2023, "socket": "LGA1700", "frequencia_base": 3.4, "frequencia_turbo": 5.4, "arquitetura": "Raptor Lake"},
    {"modelo": "Intel Core i9-10900K", "tdp": 125, "ano": 2020, "socket": "LGA1200", "frequencia_base": 3.7, "frequencia_turbo": 5.3, "arquitetura": "Comet Lake"},
    {"modelo": "Intel Core i9-12900K", "tdp": 240, "ano": 2022, "socket": "LGA1700", "frequencia_base": 3.2, "frequencia_turbo": 5.2, "arquitetura": "Alder Lake"},
    {"modelo": "Intel Core i9-13900K", "tdp": 250, "ano": 2023, "socket": "LGA1700", "frequencia_base": 3.0, "frequencia_turbo": 5.8, "arquitetura": "Raptor Lake"},
    {"modelo": "Intel Core i9-14900K", "tdp": 250, "ano": 2024, "socket": "LGA1700", "frequencia_base": 3.2, "frequencia_turbo": 6.0, "arquitetura": "Raptor Lake Refresh"},
    {"modelo": "Intel Xeon E5-2666 v3", "tdp": 115, "ano": 2014, "socket": "LGA2011-v3", "frequencia_base": 2.9, "frequencia_turbo": 3.5, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2667 v3", "tdp": 135, "ano": 2014, "socket": "LGA2011-v3", "frequencia_base": 3.2, "frequencia_turbo": 3.6, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2667 v4", "tdp": 160, "ano": 2016, "socket": "LGA2011-v3", "frequencia_base": 3.2, "frequencia_turbo": 3.7, "arquitetura": "Broadwell-EP"},
    {"modelo": "Intel Xeon E5-2680 v4", "tdp": 120, "ano": 2016, "socket": "LGA2011-v3", "frequencia_base": 2.4, "frequencia_turbo": 3.3, "arquitetura": "Broadwell-EP"},
    {"modelo": "Intel Xeon E5-1660 v3", "tdp": 140, "ano": 2014, "socket": "LGA2011-v3", "frequencia_base": 3.0, "frequencia_turbo": 3.7, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2680 v3", "tdp": 135, "ano": 2014, "socket": "LGA2011-v3", "frequencia_base": 2.5, "frequencia_turbo": 3.3, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2690 v3", "tdp": 135, "ano": 2014, "socket": "LGA2011-v3", "frequencia_base": 2.6, "frequencia_turbo": 3.5, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2670 v3", "tdp": 120, "ano": 2014, "socket": "LGA2011-v3", "frequencia_base": 2.3, "frequencia_turbo": 3.1, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2699 v4", "tdp": 145, "ano": 2016, "socket": "LGA2011-v3", "frequencia_base": 2.2, "frequencia_turbo": 3.6, "arquitetura": "Broadwell-EP"},
    {"modelo": "AMD FX-8350", "tdp": 125, "ano": 2012, "socket": "AM3+", "frequencia_base": 4.0, "frequencia_turbo": 4.2, "arquitetura": "Piledriver"},
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
    {"modelo": "Rise Mode Black 240 (Water)", "tipo": "Water", "tdp_manufacturer": 250, "ruido_db": 30, "durabilidade_anos": 5},
    {"modelo": "GameMax IceBurg 240 (Water)", "tipo": "Water", "tdp_manufacturer": 245, "ruido_db": 31, "durabilidade_anos": 6},
    {"modelo": "Corsair H100i (AIO 240) (Water)", "tipo": "Water", "tdp_manufacturer": 300, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Arctic Liquid Freezer II 240 (Water)", "tipo": "Water", "tdp_manufacturer": 320, "ruido_db": 27, "durabilidade_anos": 7},
    {"modelo": "TGT Storm 240 (Water)", "tipo": "Water", "tdp_manufacturer": 280, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "DeepCool LS720 (AIO 360) (Water)", "tipo": "Water", "tdp_manufacturer": 300, "ruido_db": 32, "durabilidade_anos": 7},
    {"modelo": "Corsair H150i (AIO 360) (Water)", "tipo": "Water", "tdp_manufacturer": 350, "ruido_db": 30, "durabilidade_anos": 7},
    {"modelo": "NZXT Kraken X63 (AIO 280) (Water)", "tipo": "Water", "tdp_manufacturer": 350, "ruido_db": 29, "durabilidade_anos": 7},
    {"modelo": "DeepCool Castle 360EX (AIO 360) (Water)", "tipo": "Water", "tdp_manufacturer": 350, "ruido_db": 31, "durabilidade_anos": 7},
    {"modelo": "Rise Mode Gamer Black 240 (AIO) (Water)", "tipo": "Water", "tdp_manufacturer": 220, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Pichau AIO 240 (Water)", "tipo": "Water", "tdp_manufacturer": 270, "ruido_db": 34, "durabilidade_anos": 5},
    {"modelo": "Husky Hunter 240 (AIO)", "tipo": "Water", "tdp_manufacturer": 260, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "Rise Mode Sentinel 240 (AIO)", "tipo": "Water", "tdp_manufacturer": 300, "ruido_db": 32, "durabilidade_anos": 6},
    {"modelo": "Rise Mode Ventus (Air)", "tipo": "Air", "tdp_manufacturer": 150, "ruido_db": 36, "durabilidade_anos": 4},
    {"modelo": "Redragon TYR (Air)", "tipo": "Air", "tdp_manufacturer": 130, "ruido_db": 22, "durabilidade_anos": 4},
    {"modelo": "DeepCool AK620 (Air)", "tipo": "Air", "tdp_manufacturer": 260, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "DeepCool Castle 360EX (AIO 360) (Water)", "tipo": "Water", "tdp_manufacturer": 350, "ruido_db": 31, "durabilidade_anos": 7},
    {"modelo": "Corsair H150i (AIO 360) (Water)", "tipo": "Water", "tdp_manufacturer": 350, "ruido_db": 30, "durabilidade_anos": 7},
    {"modelo": "NZXT Kraken X63 (AIO 280) (Water)", "tipo": "Water", "tdp_manufacturer": 350, "ruido_db": 29, "durabilidade_anos": 7},
    {"modelo": "DeepCool LS720 (AIO 360) (Water)", "tipo": "Water", "tdp_manufacturer": 300, "ruido_db": 32, "durabilidade_anos": 7},
    {"modelo": "Arctic Liquid Freezer II 240 (Water)", "tipo": "Water", "tdp_manufacturer": 320, "ruido_db": 27, "durabilidade_anos": 7},
    {"modelo": "Corsair H100i (AIO 240) (Water)", "tipo": "Water", "tdp_manufacturer": 300, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "TGT Storm 240 (Water)", "tipo": "Water", "tdp_manufacturer": 280, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "Pichau AIO 240 (Water)", "tipo": "Water", "tdp_manufacturer": 270, "ruido_db": 34, "durabilidade_anos": 5},
    {"modelo": "Rise Mode Gamer Black 240 (AIO) (Water)", "tipo": "Water", "tdp_manufacturer": 220, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Husky Hunter 240 (AIO)", "tipo": "Water", "tdp_manufacturer": 260, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "Rise Mode Sentinel 240 (AIO) (Water)", "tipo": "Water", "tdp_manufacturer": 300, "ruido_db": 32, "durabilidade_anos": 6},
    {"modelo": "Rise Mode Storm 8 (Air) - DUP (entry)", "tipo": "Air", "tdp_manufacturer": 280, "ruido_db": 30, "durabilidade_anos": 5},
    {"modelo": "Cooler Master Hyper 212 (Air) - DUP (entry)", "tipo": "Air", "tdp_manufacturer": 150, "ruido_db": 35, "durabilidade_anos": 5},
]

# apply nominal adjust (this matches your last provided code, uses 95% of manufacturer)
for c in COOLERS:
    c["tdp_nominal"] = round(0.95 * c.get("tdp_manufacturer", 0.0), 1)

# --------------------------
# GLOBAL PARAMETERS (calibration knobs)
# --------------------------
BASE_SAFETY_PCT = 0.10        # conservative reduction of cooler capacity
R_JC_BY_AGE = {               # heuristic for junction->case (°C/W) by CPU era
    "old": 0.6,  # very old
    "mid": 0.3,
    "new": 0.18
}
R_CS_DEFAULT = 0.08           # case->heatsink via TIM (°C/W)
C_TH_DEFAULT = 350.0          # thermal mass (J/°C) - adjust to match transient

# Profiles (how aggressive the workload is vs TDP)
WORKLOAD_PROFILES = {
    "Idle / Light": 0.15,
    "Office / Browsing": 0.30,
    "Gaming (typical)": 0.55,
    "Sustained bench (Cinebench)": 1.00,
    "AVX-heavy / Prime": 1.30
}

# --------------------------
# HELPER MODELS
# --------------------------
def avg_frequency(cpu):
    b = cpu.get("frequencia_base", 3.5)
    t = cpu.get("frequencia_turbo", b)
    return (b + t) / 2.0

def cpu_power_model(cpu_tdp, workload_pct, profile_factor=1.0, freq_scale=1.0):
    """
    cpu_tdp: manufacturer TDP (W) used as reference only
    workload_pct: slider 0..100
    profile_factor: multiplier from WORKLOAD_PROFILES
    freq_scale: scaling of frequency (1.0 normal; >1 overclock)
    returns: estimated instantaneous power (W)
    """
    # idle + dynamic + leakage heuristics
    idle = 0.10 * cpu_tdp
    dynamic = cpu_tdp * (workload_pct / 100.0) * (0.80 * profile_factor) * freq_scale
    leakage = 0.02 * cpu_tdp * (1.0 + 0.05 * (freq_scale - 1.0))
    return max(0.0, idle + dynamic + leakage)

def derive_rth_from_nominal(tdp_nominal_w):
    """Heuristic: higher nominal -> lower Rth. Tunable coefficient."""
    if tdp_nominal_w <= 0: return 10.0
    coef = 28.0
    rth = max(0.02, coef / tdp_nominal_w)
    return rth

def fan_rpm_from_util(util_pct, rpm_idle=600, rpm_max=2200):
    if util_pct <= 15: return rpm_idle
    if util_pct >= 100: return rpm_max
    return int(rpm_idle + (rpm_max - rpm_idle) * ((util_pct - 15) / 85.0))

def rth_with_fan(rth_nominal, rpm, rpm_ref=1500):
    if rpm <= 0: return rth_nominal * 2.0
    return rth_nominal * (rpm_ref / rpm) ** 0.8

def cpu_jc_by_age(cpu):
    # simple heuristic mapping by year
    year = cpu.get("ano", 2018)
    if year < 2012: return R_JC_BY_AGE["old"]
    if year < 2019: return R_JC_BY_AGE["mid"]
    return R_JC_BY_AGE["new"]

def compute_PLs(cpu):
    """
    Heuristic PL1/PL2 derived from TDP and era.
    PL1 ~ 1.0-1.6 * TDP (sustained), PL2 ~ 1.1-2.0 * TDP (short burst).
    These are heuristics to model bursting behaviour.
    """
    tdp = cpu.get("tdp", 65)
    year = cpu.get("ano", 2018)
    if year >= 2022:
        pl1 = tdp * 1.2
        pl2 = tdp * 1.8
        tau = 28.0  # seconds
    elif year >= 2017:
        pl1 = tdp * 1.05
        pl2 = tdp * 1.4
        tau = 20.0
    else:
        pl1 = tdp * 1.0
        pl2 = tdp * 1.2
        tau = 10.0
    return round(pl1,1), round(pl2,1), tau

def steady_temp_from_power(P_watts, Tamb, Rth_total):
    return Tamb + P_watts * Rth_total

def simulate_transient_power_profile(power_func, Rth_total, C_th=C_TH_DEFAULT, Tamb=25.0, dt=1.0, t_total=300.0):
    n = int(t_total / dt) + 1
    T = np.zeros(n); T[0] = Tamb
    times = np.linspace(0.0, t_total, n)
    for i in range(1, n):
        t = times[i-1]
        P = power_func(t)
        dTdt = (P - (T[i-1] - Tamb) / Rth_total) / C_th
        T[i] = T[i-1] + dTdt * dt
    return times, T

# --------------------------
# UI: inputs & calibration panel
# --------------------------
st.title("Simulador de Refrigeração — Final (Realismo + Calibração)")
st.markdown("Selecionar CPU e cooler → escolher perfil de carga → Simular. Use o painel lateral para calibrar parâmetros (R_jc, R_cs, C_th).")

left, right = st.columns((2,1))

with right:
    st.subheader("Calibração (ajuste se desejar)")
    R_cs = st.slider("R_cs (case→heatsink °C/W)", 0.02, 0.3, 0.08, 0.01)
    C_th = st.slider("C_th (J/°C, inércia térmica)", 50.0, 2000.0, C_TH_DEFAULT, 10.0)
    safety_pct = st.slider("Base safety % (redução da capacidade do cooler)", 0.0, 0.30, BASE_SAFETY_PCT, 0.01)
    st.caption("Use calibração para ajustar resultados ao seu equipamento real (ver instruções nos comentários do código).")

with left:
    cpu_model = st.selectbox("Processador", [c["modelo"] for c in CPUS])
    cooler_model = st.selectbox("Cooler", [c["modelo"] for c in COOLERS])
    ambient = st.number_input("Temperatura ambiente (°C)", 10.0, 45.0, 25.0, 0.5)
    workload_slider = st.slider("Carga (slider % do TDP)", 10, 150, 100, 1)
    profile = st.selectbox("Tipo de carga (perfil)", list(WORKLOAD_PROFILES.keys()), index=3)
    freq_scale = st.slider("Fator de frequência (%)", 80, 140, 100) / 100.0
    allow_pl2 = st.checkbox("Permitir burst (PL2) por Tau", value=True)
    show_transient = st.checkbox("Mostrar transiente (curva tempo x temp)", value=True)
    if st.button("Simular"):

        cpu = next(c for c in CPUS if c["modelo"] == cpu_model)
        cooler = next(c for c in COOLERS if c["modelo"] == cooler_model)

        # basic references
        cpu_tdp = cpu["tdp"]
        profile_factor = WORKLOAD_PROFILES.get(profile, 1.0)

        # compute power (instantaneous) from model (before PL caps)
        power_generated = cpu_power_model(cpu_tdp, workload_slider, profile_factor, freq_scale)

        # heuristics PL1/PL2 and tau
        PL1, PL2, tau = compute_PLs(cpu)
        power_allowed = power_generated
        if allow_pl2:
            # simple handling: if requested power <= PL2 -> allow burst; else clamp to PL2
            power_allowed = min(power_generated, PL2)
            # For steady display, also show sustained PL1
        else:
            power_allowed = min(power_generated, PL1)

        # cooler capacity modeling
        nominal = cooler.get("tdp_nominal", 0.0)
        rth_sh_nominal = derive_rth_from_nominal(nominal)
        # ventilation effect: small heuristic from workload->ventilation
        vent_choice = st.radio("Condição do gabinete", ("Bem ventilado", "Moderado", "Pouco ventilado"), index=0)
        vent_factor = 1.0 if vent_choice == "Bem ventilado" else (0.92 if vent_choice == "Moderado" else 0.85)
        nominal_v = nominal * vent_factor * (1.0 - safety_pct)
        # effective capacity similar to old model but using nominal_v
        dyn_pct = min(0.20, 0.15 * (power_allowed / max(1.0, nominal_v)))
        capacity_effective = nominal_v * (1.0 - dyn_pct)

        # fan/ rpm / rth dynamic
        util_pct = round((power_allowed / max(1.0, capacity_effective)) * 100.0, 1) if capacity_effective>0 else 999.9
        rpm = fan_rpm_from_util(util_pct)
        rth_sh = rth_with_fan(rth_sh_nominal, rpm)
        rth_total = cpu_jc_by_age(cpu) + R_cs + rth_sh

        # steady temperature (junction approx via IHS-model)
        temp_steady = steady_temp_from_power(power_allowed, ambient, rth_total)

        # transient simulation: use power profile that starts at 10% then steps to requested power at t=5s
        def power_profile(t):
            if t < 5: return cpu_power_model(cpu_tdp, 10.0, 0.5, freq_scale)
            # If PL2 allowed but power_generated > PL1, emulate burst then drop to PL1
            if allow_pl2 and power_generated > PL1:
                if t < 5 + tau:
                    return min(power_generated, PL2)
                else:
                    return min(power_generated, PL1)
            return power_allowed

        times, temps = simulate_transient_power_profile(power_profile, rth_total, C_th=C_th, Tamb=ambient, dt=1.0, t_total=180.0)

        # throttling indicator: compare steady temp vs threshold (safe heuristic)
        throttle_warn = temp_steady >= 95.0

        # OUTPUTS
        st.markdown("## Resultado")
        st.write(f"**CPU:** {cpu['modelo']} — TDP (referência): {cpu_tdp} W")
        st.write(f"**Perfil:** {profile} (fator {profile_factor:.2f}) • Freq scale: {freq_scale:.2f}")
        st.write(f"**Power (modelo):** {power_generated:.1f} W (potência gerada pelo perfil/carga)")
        st.write(f"**Power aplicado após PL/limites:** {power_allowed:.1f} W  (PL1={PL1} W, PL2={PL2} W, tau={tau}s)")
        st.write(f"**Cooler:** {cooler['modelo']} — nominal aplicado: {nominal:.1f} W (vent_factor {vent_factor:.2f}, safety {safety_pct*100:.0f}%)")
        st.write(f"**Capacidade efetiva do cooler:** {capacity_effective:.1f} W (dinâmico {dyn_pct*100:.1f}%)")
        st.write(f"**Utilização da capacidade efetiva:** {util_pct}%")
        st.write(f"**RPM estimado (fan curve):** {rpm} RPM — Rth_heatsink ≈ {rth_sh:.3f} °C/W")
        st.write(f"**Rth_total (J→amb):** {rth_total:.3f} °C/W (Rjc + Rcs + Rsh)")
        st.write(f"**Temperatura estimada (steady junction ≈ IHS):** {temp_steady:.1f} °C (ambiente {ambient}°C)")
        if throttle_warn:
            st.error("Temperatura estimada >= 95°C — risco de throttling/proteção térmica.")
        else:
            st.success("Temperatura estimada dentro de limites operacionais.")

        st.write(f"**Ruído estimado:** {round(cooler.get('ruido_db',30) * (0.6 + 0.4 * sqrt(min(1.0, util_pct/100.0))),1)} dB")
        st.write(f"**Durabilidade estimada:** ~{estimate_durability(cooler, util_pct)} anos")

        # charts
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Temperatura (transiente)")
            if show_transient:
                fig, ax = plt.subplots(figsize=(8,3))
                ax.plot(times, temps, linewidth=2)
                ax.axhline(95.0, color="r", linestyle="--", label="Temp throttle ~95°C")
                ax.set_xlabel("Tempo (s)"); ax.set_ylabel("Temp (°C)")
                ax.set_title(f"{cpu['modelo']} + {cooler['modelo']}")
                ax.grid(alpha=0.5, linestyle='--')
                st.pyplot(fig)
            else:
                st.write("Transiente escondido (toggle no painel).")

        with col2:
            st.markdown("### Comparativo potência x capacidade")
            labels = ["Power applied (W)", "Capacidade efetiva (W)"]
            values = [power_allowed, capacity_effective]
            fig2, ax2 = plt.subplots(figsize=(5,3))
            bars = ax2.bar(labels, values)
            for i,v in enumerate(values):
                ax2.text(i, v + max(1, 0.02*v), f"{v:.1f}", ha='center')
            ax2.set_ylim(0, max(values) * 1.3 if max(values)>0 else 1)
            st.pyplot(fig2)

        # show numeric table for quick copy/paste
        df = pd.DataFrame([{
            "cpu": cpu['modelo'],
            "tdp_ref_W": cpu_tdp,
            "power_model_W": round(power_generated,1),
            "power_applied_W": round(power_allowed,1),
            "cooler_nominal_W": round(nominal,1),
            "capacity_eff_W": round(capacity_effective,1),
            "rth_total_CperW": round(rth_total,3),
            "temp_steady_C": round(temp_steady,1),
            "rpm": rpm,
            "util_pct": util_pct
        }])
        st.markdown("### Dados (tabela)")
        st.dataframe(df)

st.markdown("---")
st.caption("Notas: este simulador usa modelos heurísticos para aproximar comportamento real. Para alta fidelidade, calibre Rth e C_th usando medições reais com HWiNFO/Intel Power Gadget e benchs controlados.")
