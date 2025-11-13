# simulador_refrigeracao_unico.py
# Versão final integrada: CPUS originais + cálculo térmico aprimorado (+30% TDP, ventilação)
# Requisitos: streamlit, matplotlib, pandas, numpy
#
# Uso:
# pip install streamlit matplotlib pandas numpy
# streamlit run simulador_refrigeracao_unico.py

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import sqrt

st.set_page_config(page_title="Simulador de Refrigeração - 2010–2025", layout="wide")

# --------------------------
# CPUS (dados originais — NÃO ALTEREI)
# --------------------------
CPUS = [
    # --- AMD Ryzen (ordenado cronologicamente / gerações) ---
    {"modelo": "AMD Ryzen 5 1600X", "tdp": 95, "ano": 2017, "socket": "AM4",
     "frequencia_base": 3.6, "frequencia_turbo": 4.0, "arquitetura": "Zen"},
    {"modelo": "AMD Ryzen 5 3600", "tdp": 65, "ano": 2019, "socket": "AM4",
     "frequencia_base": 3.6, "frequencia_turbo": 4.2, "arquitetura": "Zen 2"},
    {"modelo": "AMD Ryzen 5 5600", "tdp": 65, "ano": 2021, "socket": "AM4",
     "frequencia_base": 3.5, "frequencia_turbo": 4.4, "arquitetura": "Zen 3"},
    {"modelo": "AMD Ryzen 5 5600X", "tdp": 65, "ano": 2020, "socket": "AM4",
     "frequencia_base": 3.7, "frequencia_turbo": 4.6, "arquitetura": "Zen 3"},
    {"modelo": "AMD Ryzen 5 5600X3D", "tdp": 105, "ano": 2022, "socket": "AM4",
     "frequencia_base": 3.3, "frequencia_turbo": 4.4, "arquitetura": "Zen 3 (3D)"},
    {"modelo": "AMD Ryzen 5 5500X3D", "tdp": 105, "ano": 2024, "socket": "AM4",
     "frequencia_base": 3.0, "frequencia_turbo": 4.0, "arquitetura": "Zen 3 (3D)"},
    {"modelo": "AMD Ryzen 5 7400F", "tdp": 65, "ano": 2024, "socket": "AM5",
     "frequencia_base": 3.7, "frequencia_turbo": 4.7, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 5 7500F", "tdp": 65, "ano": 2024, "socket": "AM5",
     "frequencia_base": 3.7, "frequencia_turbo": 5.0, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 5 7600", "tdp": 65, "ano": 2022, "socket": "AM5",
     "frequencia_base": 3.8, "frequencia_turbo": 5.1, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 5 7600X", "tdp": 105, "ano": 2022, "socket": "AM5",
     "frequencia_base": 4.7, "frequencia_turbo": 5.3, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 5 7600X3D", "tdp": 65, "ano": 2024, "socket": "AM5",
     "frequencia_base": 4.1, "frequencia_turbo": 4.7, "arquitetura": "Zen 4 (3D)"},
    {"modelo": "AMD Ryzen 5 8400F", "tdp": 65, "ano": 2024, "socket": "AM5",
     "frequencia_base": 4.2, "frequencia_turbo": 4.7, "arquitetura": "Zen 5"},
    {"modelo": "AMD Ryzen 5 8500G", "tdp": 65, "ano": 2024, "socket": "AM5",
     "frequencia_base": 3.5, "frequencia_turbo": 5.0, "arquitetura": "Zen 5 (G)"},
    {"modelo": "AMD Ryzen 5 8600G", "tdp": 65, "ano": 2024, "socket": "AM5",
     "frequencia_base": 4.3, "frequencia_turbo": 5.0, "arquitetura": "Zen 5 (G)"},
    {"modelo": "AMD Ryzen 5 9600X", "tdp": 65, "ano": 2024, "socket": "AM5",
     "frequencia_base": 3.9, "frequencia_turbo": 5.4, "arquitetura": "Zen 5"},
    {"modelo": "AMD Ryzen 7 7700", "tdp": 65, "ano": 2023, "socket": "AM5",
     "frequencia_base": 3.8, "frequencia_turbo": 5.3, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 7 7700X", "tdp": 105, "ano": 2023, "socket": "AM5",
     "frequencia_base": 4.5, "frequencia_turbo": 5.4, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 7 5800X", "tdp": 105, "ano": 2020, "socket": "AM4",
     "frequencia_base": 3.8, "frequencia_turbo": 4.7, "arquitetura": "Zen 3"},
    {"modelo": "AMD Ryzen 7 5800X3D", "tdp": 105, "ano": 2022, "socket": "AM4",
     "frequencia_base": 3.4, "frequencia_turbo": 4.5, "arquitetura": "Zen 3 (3D)"},
    {"modelo": "AMD Ryzen 9 5900X", "tdp": 105, "ano": 2020, "socket": "AM4",
     "frequencia_base": 3.7, "frequencia_turbo": 4.8, "arquitetura": "Zen 3"},
    {"modelo": "AMD Ryzen 9 5950X", "tdp": 105, "ano": 2020, "socket": "AM4",
     "frequencia_base": 3.4, "frequencia_turbo": 4.9, "arquitetura": "Zen 3"},
    {"modelo": "AMD Ryzen 9 7950X", "tdp": 170, "ano": 2022, "socket": "AM5",
     "frequencia_base": 4.5, "frequencia_turbo": 5.7, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 9 7950X3D", "tdp": 120, "ano": 2023, "socket": "AM5",
     "frequencia_base": 4.2, "frequencia_turbo": 5.7, "arquitetura": "Zen 4 (3D)"},

    # --- Intel (ordenado cronologicamente/generations aproximadas) ---
    {"modelo": "Intel Core 2 Duo E8400", "tdp": 65, "ano": 2008, "socket": "LGA775",
     "frequencia_base": 3.0, "frequencia_turbo": 3.0, "arquitetura": "Core (65nm)"},
    {"modelo": "Intel Core i3-530", "tdp": 73, "ano": 2010, "socket": "LGA1156",
     "frequencia_base": 2.93, "frequencia_turbo": 3.06, "arquitetura": "Clarksfield"},
    {"modelo": "Intel Core i3-3240", "tdp": 55, "ano": 2012, "socket": "LGA1155",
     "frequencia_base": 3.4, "frequencia_turbo": 3.4, "arquitetura": "Ivy Bridge"},
    {"modelo": "Intel Core i7-920", "tdp": 130, "ano": 2008, "socket": "LGA1366",
     "frequencia_base": 2.66, "frequencia_turbo": 2.93, "arquitetura": "Nehalem"},
    {"modelo": "Intel Core i3-6100", "tdp": 51, "ano": 2015, "socket": "LGA1151",
     "frequencia_base": 3.7, "frequencia_turbo": 3.7, "arquitetura": "Skylake"},
    {"modelo": "Intel Core i5-6600K", "tdp": 91, "ano": 2015, "socket": "LGA1151",
     "frequencia_base": 3.5, "frequencia_turbo": 3.9, "arquitetura": "Skylake"},
    {"modelo": "Intel Core i5-8400", "tdp": 65, "ano": 2018, "socket": "LGA1151",
     "frequencia_base": 2.8, "frequencia_turbo": 4.0, "arquitetura": "Coffee Lake"},
    {"modelo": "Intel Core i5-10400F", "tdp": 65, "ano": 2020, "socket": "LGA1200",
     "frequencia_base": 2.9, "frequencia_turbo": 4.3, "arquitetura": "Comet Lake"},
    {"modelo": "Intel Core i5-10600K", "tdp": 125, "ano": 2020, "socket": "LGA1200",
     "frequencia_base": 4.1, "frequencia_turbo": 4.8, "arquitetura": "Comet Lake"},
    {"modelo": "Intel Core i5-12400F", "tdp": 65, "ano": 2022, "socket": "LGA1700",
     "frequencia_base": 2.5, "frequencia_turbo": 4.4, "arquitetura": "Alder Lake"},
    {"modelo": "Intel Core i5-13400F", "tdp": 65, "ano": 2023, "socket": "LGA1700",
     "frequencia_base": 2.5, "frequencia_turbo": 4.6, "arquitetura": "Raptor Lake"},
    {"modelo": "Intel Core i5-14600K", "tdp": 180, "ano": 2024, "socket": "LGA1700",
     "frequencia_base": 3.1, "frequencia_turbo": 5.1, "arquitetura": "Raptor Lake Refresh"},
    {"modelo": "Intel Core i7-11700K", "tdp": 125, "ano": 2021, "socket": "LGA1200",
     "frequencia_base": 3.6, "frequencia_turbo": 5.0, "arquitetura": "Rocket Lake"},
    {"modelo": "Intel Core i7-12700K", "tdp": 190, "ano": 2022, "socket": "LGA1700",
     "frequencia_base": 3.6, "frequencia_turbo": 5.0, "arquitetura": "Alder Lake"},
    {"modelo": "Intel Core i7-13700K", "tdp": 250, "ano": 2023, "socket": "LGA1700",
     "frequencia_base": 3.4, "frequencia_turbo": 5.4, "arquitetura": "Raptor Lake"},
    {"modelo": "Intel Core i9-10900K", "tdp": 125, "ano": 2020, "socket": "LGA1200",
     "frequencia_base": 3.7, "frequencia_turbo": 5.3, "arquitetura": "Comet Lake"},
    {"modelo": "Intel Core i9-12900K", "tdp": 240, "ano": 2022, "socket": "LGA1700",
     "frequencia_base": 3.2, "frequencia_turbo": 5.2, "arquitetura": "Alder Lake"},
    {"modelo": "Intel Core i9-13900K", "tdp": 250, "ano": 2023, "socket": "LGA1700",
     "frequencia_base": 3.0, "frequencia_turbo": 5.8, "arquitetura": "Raptor Lake"},
    {"modelo": "Intel Core i9-14900K", "tdp": 250, "ano": 2024, "socket": "LGA1700",
     "frequencia_base": 3.2, "frequencia_turbo": 6.0, "arquitetura": "Raptor Lake Refresh"},

    # --- Intel Xeon (v3 / v4 entries, corrected) ---
    {"modelo": "Intel Xeon E5-2666 v3", "tdp": 115, "ano": 2014, "socket": "LGA2011-v3",
     "frequencia_base": 2.9, "frequencia_turbo": 3.5, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2667 v3", "tdp": 135, "ano": 2014, "socket": "LGA2011-v3",
     "frequencia_base": 3.2, "frequencia_turbo": 3.6, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2667 v4", "tdp": 160, "ano": 2016, "socket": "LGA2011-v3",
     "frequencia_base": 3.2, "frequencia_turbo": 3.7, "arquitetura": "Broadwell-EP"},
    {"modelo": "Intel Xeon E5-2680 v4", "tdp": 120, "ano": 2016, "socket": "LGA2011-v3",
     "frequencia_base": 2.4, "frequencia_turbo": 3.3, "arquitetura": "Broadwell-EP"},
    {"modelo": "Intel Xeon E5-1660 v3", "tdp": 140, "ano": 2014, "socket": "LGA2011-v3",
     "frequencia_base": 3.0, "frequencia_turbo": 3.7, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2680 v3", "tdp": 135, "ano": 2014, "socket": "LGA2011-v3",
     "frequencia_base": 2.5, "frequencia_turbo": 3.3, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2690 v3", "tdp": 135, "ano": 2014, "socket": "LGA2011-v3",
     "frequencia_base": 2.6, "frequencia_turbo": 3.5, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2670 v3", "tdp": 120, "ano": 2014, "socket": "LGA2011-v3",
     "frequencia_base": 2.3, "frequencia_turbo": 3.1, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2699 v4", "tdp": 145, "ano": 2016, "socket": "LGA2011-v3",
     "frequencia_base": 2.2, "frequencia_turbo": 3.6, "arquitetura": "Broadwell-EP"},

    # --- Legacy / others kept for compatibility ---
    {"modelo": "AMD FX-8350", "tdp": 125, "ano": 2012, "socket": "AM3+",
     "frequencia_base": 4.0, "frequencia_turbo": 4.2, "arquitetura": "Piledriver"},
]

# --------------------------
# COOLERS (ATUALIZADA: adições solicitadas e nomes com indicação Air/Water)
# Ordem: approximada DO MAIS FRACO para O MAIS FORTE (conforme solicitado).
# Mantive os campos: modelo (com indicação), tipo ("Air" ou "AIO"/"Water"), tdp_manufacturer (W),
# ruido_db (dB), durabilidade_anos (anos).
# --------------------------

COOLERS = [
    # Fracos / entrada
    {"modelo": "SuperFrame SuperFlow 450 (Air)", "tipo": "Air", "tdp_manufacturer": 95, "ruido_db": 25, "durabilidade_anos": 4},
    {"modelo": "Gamdias Boreas E1-410 (Air)", "tipo": "Air", "tdp_manufacturer": 95, "ruido_db": 28, "durabilidade_anos": 4},
    {"modelo": "TGT Glacier 120 (Air)", "tipo": "Air", "tdp_manufacturer": 100, "ruido_db": 36, "durabilidade_anos": 3},
    {"modelo": "DeepCool Gammaxx 400 (Air)", "tipo": "Air", "tdp_manufacturer": 120, "ruido_db": 38, "durabilidade_anos": 4},
    {"modelo": "Redragon TYR (Air)", "tipo": "Air", "tdp_manufacturer": 130, "ruido_db": 22, "durabilidade_anos": 4},

    # Médio-baixa
    {"modelo": "Cooler Master Hyper 212 (Air)", "tipo": "Air", "tdp_manufacturer": 150, "ruido_db": 35, "durabilidade_anos": 5},
    {"modelo": "DeepCool AK500S (Air)", "tipo": "Air", "tdp_manufacturer": 150, "ruido_db": 28, "durabilidade_anos": 6},  # fonte: DeepCool / revendas
    {"modelo": "Thermalright TRUE Spirit 140 (Air)", "tipo": "Air", "tdp_manufacturer": 200, "ruido_db": 28, "durabilidade_anos": 6},

    # Médio
    {"modelo": "Arctic Freezer 34 (Air)", "tipo": "Air", "tdp_manufacturer": 180, "ruido_db": 28, "durabilidade_anos": 5},
    {"modelo": "DeepCool AK400 (Air)", "tipo": "Air", "tdp_manufacturer": 220, "ruido_db": 29, "durabilidade_anos": 6},  # fonte: DeepCool (até ~220W)
    {"modelo": "DeepCool Gammaxx AG400 (Air)", "tipo": "Air", "tdp_manufacturer": 220, "ruido_db": 28, "durabilidade_anos": 4},  # revendas BR
    {"modelo": "GameMax Sigma 520 (Air)", "tipo": "Air", "tdp_manufacturer": 220, "ruido_db": 30, "durabilidade_anos": 5},  # GameMax specs (~220W)
    {"modelo": "Rise Mode Storm 8 (Air)", "tipo": "Air", "tdp_manufacturer": 280, "ruido_db": 30, "durabilidade_anos": 5},  # Rise Mode (TDP anunciado 280W)

    # Alto desempenho air
    {"modelo": "Be Quiet! Dark Rock Pro 4 (Air)", "tipo": "Air", "tdp_manufacturer": 250, "ruido_db": 24, "durabilidade_anos": 7},
    {"modelo": "Noctua NH-D15 (Air)", "tipo": "Air", "tdp_manufacturer": 250, "ruido_db": 24, "durabilidade_anos": 8},
    {"modelo": "DeepCool AK620 (Air)", "tipo": "Air", "tdp_manufacturer": 260, "ruido_db": 28, "durabilidade_anos": 6},

    # AIO / Water coolers (entrada → médio)
    {"modelo": "Rise Mode Black 240 (Water)", "tipo": "Water", "tdp_manufacturer": 250, "ruido_db": 30, "durabilidade_anos": 5},  # loja RiseMode / Kabum
    {"modelo": "GameMax IceBurg 240 (Water)", "tipo": "Water", "tdp_manufacturer": 245, "ruido_db": 31, "durabilidade_anos": 6},  # GameMax spec (~245W)
    {"modelo": "Corsair H100i (AIO 240) (Water)", "tipo": "Water", "tdp_manufacturer": 300, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Arctic Liquid Freezer II 240 (Water)", "tipo": "Water", "tdp_manufacturer": 320, "ruido_db": 27, "durabilidade_anos": 7},

    # AIO / Water coolers (alto)
    {"modelo": "TGT Storm 240 (Water)", "tipo": "Water", "tdp_manufacturer": 280, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "DeepCool LS720 (AIO 360) (Water)", "tipo": "Water", "tdp_manufacturer": 300, "ruido_db": 32, "durabilidade_anos": 7},  # DeepCool LS720 spec (~300W)
    {"modelo": "Corsair H150i (AIO 360) (Water)", "tipo": "Water", "tdp_manufacturer": 350, "ruido_db": 30, "durabilidade_anos": 7},
    {"modelo": "NZXT Kraken X63 (AIO 280) (Water)", "tipo": "Water", "tdp_manufacturer": 350, "ruido_db": 29, "durabilidade_anos": 7},
    {"modelo": "DeepCool Castle 360EX (AIO 360) (Water)", "tipo": "Water", "tdp_manufacturer": 350, "ruido_db": 31, "durabilidade_anos": 7},

    # Extras / compatibilidade e modelos de referência (manter compatibilidade com lista antiga)
    {"modelo": "Rise Mode Gamer Black 240 (AIO) (Water)", "tipo": "Water", "tdp_manufacturer": 220, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Pichau AIO 240 (Water)", "tipo": "Water", "tdp_manufacturer": 270, "ruido_db": 34, "durabilidade_anos": 5},
    {"modelo": "Husky Hunter 240 (AIO) (Water)", "tipo": "Water", "tdp_manufacturer": 260, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "Rise Mode Sentinel 240 (AIO) (Water)", "tipo": "Water", "tdp_manufacturer": 300, "ruido_db": 32, "durabilidade_anos": 6},

    # Mantidos (como no seu código original, em ordem de referência)
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
    {"modelo": "Husky Hunter 240 (AIO) (Water)", "tipo": "Water", "tdp_manufacturer": 260, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "Rise Mode Sentinel 240 (AIO) (Water)", "tipo": "Water", "tdp_manufacturer": 300, "ruido_db": 32, "durabilidade_anos": 6},
    {"modelo": "Rise Mode Storm 8 (Air) - DUP (entry)", "tipo": "Air", "tdp_manufacturer": 280, "ruido_db": 30, "durabilidade_anos": 5},
    {"modelo": "Cooler Master Hyper 212 (Air) - DUP (entry)", "tipo": "Air", "tdp_manufacturer": 150, "ruido_db": 35, "durabilidade_anos": 5},
]

# calcular tdp_nominal ajustado = 0.90 * tdp_manufacturer
for c in COOLERS:
    if "tdp_manufacturer" in c and c["tdp_manufacturer"] is not None:
        c["tdp_nominal"] = round(0.90 * c["tdp_manufacturer"], 1)
    else:
        c["tdp_nominal"] = c.get("tdp_nominal", 0.0)

# Safety configuration (base safety reduction applied to all coolers)
BASE_SAFETY_PCT = 0.10  # 10% base safety

# --------------------------
# Funções utilitárias e modelo térmico (REVISADAS)
# - compute_adjusted_tdp_for_frequency: relaciona frequência média com TDP ajustado (não altera CPUS)
# - compute_effective_capacity: agora aceita factor_ventilacao para reduzir capacidade efetiva dos coolers
# - estimate_temperature: sensibilidade aumentada com frequência média
# --------------------------

def avg_frequency(cpu):
    b = cpu.get("frequencia_base")
    t = cpu.get("frequencia_turbo")
    if b and t:
        return (b + t) / 2.0
    if b:
        return b
    return 3.5

def architecture_factor(cpu):
    ano = cpu.get("ano", 2018)
    if ano >= 2022:
        return 0.95
    elif ano >= 2017:
        return 1.00
    elif ano >= 2010:
        return 1.05
    else:
        return 1.10

def compute_adjusted_tdp_for_frequency(cpu):
    """
    Retorna: adjusted_tdp_no_extra, freq_pct, arch_factor
    - adjusted_tdp_no_extra: TDP ajustado por frequência e arquitetura (sem o +30% extra).
    """
    base_tdp = cpu["tdp"]
    f_avg = avg_frequency(cpu)
    delta = f_avg - 3.5  # referência em 3.5 GHz
    # impacto não-linear da frequência
    freq_factor = 0.16 * delta + 0.02 * (delta ** 2)
    freq_factor = max(-0.30, min(0.60, freq_factor))
    arch = architecture_factor(cpu)
    dissipation_bonus = 1.0
    if cpu.get("ano", 0) >= 2022:
        dissipation_bonus -= 0.03
    extra_penalty = 1.0
    if cpu.get("ano", 0) < 2018 and delta > 0:
        extra_penalty += 0.05 * delta
    adjusted = base_tdp * (1.0 + freq_factor * extra_penalty) * arch * dissipation_bonus
    adjusted = max(5.0, adjusted)
    return adjusted, round(freq_factor * 100, 1), arch

def compute_effective_capacity(cooler_nominal, cpu_adjusted_tdp, vent_factor=1.0):
    """
    cooler_nominal: tdp_nominal (já aplicado o 90% do fabricante)
    vent_factor: 1.0 (bem ventilado), 0.9 (moderado), 0.8 (pouco ventilado)
    """
    if cooler_nominal <= 0:
        return 0.0, 0.0, 0.0
    # aplicar fator de ventilação na capacidade nominal
    nominal_adjusted_for_vent = cooler_nominal * vent_factor
    dynamic_pct = min(0.20, 0.15 * (cpu_adjusted_tdp / nominal_adjusted_for_vent))
    effective = nominal_adjusted_for_vent * (1.0 - BASE_SAFETY_PCT) * (1.0 - dynamic_pct)
    return effective, round(BASE_SAFETY_PCT * 100, 1), round(dynamic_pct * 100, 1)

def estimate_temperature(cpu_adjusted_tdp, capacity_effective, ambient_c=25.0, workload=1.0, f_avg=3.5):
    power = cpu_adjusted_tdp * workload
    if capacity_effective <= 0:
        return 120.0
    ratio = power / capacity_effective
    K_base = 55.0
    freq_sensitivity = max(0.0, f_avg - 3.5)
    K = K_base + (freq_sensitivity * 10.0)  # heurístico: 10°C por GHz acima de 3.5
    if ratio <= 1.0:
        delta = ratio * (K * 0.9)
    else:
        delta = (1.0 * (K * 0.9)) + ((ratio - 1.0) * (K * 2.0))
    return round(ambient_c + delta, 1)

def estimate_noise(cooler, utilization_pct):
    base = cooler.get("ruido_db", 30)
    scale = sqrt(min(1.0, max(0.0, utilization_pct / 100.0)))
    return round(base * (0.6 + 0.4 * scale), 1)

def estimate_durability(cooler, utilization_pct):
    base_years = cooler.get("durabilidade_anos", 5)
    if utilization_pct <= 80:
        return base_years
    else:
        excess = (utilization_pct - 80) / 20.0
        return max(1, int(base_years * (1.0 - 0.5 * excess)))

# ordenar coolers por desempenho (tdp_nominal decrescente)
COOLERS.sort(key=lambda x: x.get("tdp_nominal", 0.0), reverse=True)

# --------------------------
# Interface Streamlit (mantida com adição: ventilação)
# --------------------------
st.title("Simulador de Refrigeração de CPU (2010–2025)")
st.markdown("Simulação comparativa com fator de segurança dinâmico. Selecione CPU e cooler e clique em 'Simular'.")

with st.expander("Instruções rápidas (clique para abrir)"):
    st.write("""
    - Selecione o processador e o cooler nos menus.
    - O simulador ajusta o TDP do CPU pela frequência média (fator agressivo) e pela arquitetura (ano).
    - Agora aplicamos +30% no TDP ajustado para aproximar consumo real de boost (aplicado apenas nos cálculos).
    - Os valores de TDP dos coolers foram ajustados para refletir eficiência prática (-10% nominal).
    - Adicione a condição do gabinete (ventilação) para estimar melhor o airflow.
    - O gráfico mostra Temperatura × Carga; painel lateral apresenta métricas detalhadas.
    """)

col_left, col_right = st.columns((2, 1))

with col_left:
    st.subheader("Seleção")
    CPUS_sorted = sorted(CPUS, key=lambda x: (x.get("ano", 9999), x["modelo"]))
    cpu_choice = st.selectbox("Selecione o processador para simular", [c["modelo"] for c in CPUS_sorted])
    cooler_choice = st.selectbox("Selecione o cooler", [c["modelo"] for c in COOLERS])

    # Nova opção: ventilação do gabinete (abaixo de escolha de cooler)
    ventilacao = st.selectbox("Nível de ventilação do gabinete",
                              ["Bem ventilado 🟢", "Moderado 🟡", "Pouco ventilado 🔴"])

    ambient = st.number_input("Temperatura ambiente (°C)", min_value=10.0, max_value=40.0, value=25.0, step=1.0)
    workload_slider = st.slider("Carga (percentual do TDP)", 10, 150, 100)
    show_detailed = st.checkbox("Mostrar gráfico detalhado (Temperatura vs carga)", value=True)

    if st.button("Simular"):
        cpu = next((c for c in CPUS_sorted if c["modelo"] == cpu_choice), None)
        cooler = next((c for c in COOLERS if c["modelo"] == cooler_choice), None)

        if cpu is None or cooler is None:
            st.error("Selecionar CPU e cooler válidos.")
        else:
            # --- TDP ajustado por freq/arquitetura (SEM o +30%) ---
            cpu_tdp_adj_no_extra, freq_pct, arch_factor = compute_adjusted_tdp_for_frequency(cpu)
            f_avg_cpu = avg_frequency(cpu)

            # aplicando +30% ao TDP ajustado apenas para o cálculo realista (mantemos os dados originais)
            cpu_tdp_adj = cpu_tdp_adj_no_extra * 1.30  # <-- AQUI aplicamos o +30%

            # determinar fator de ventilação numérico
            if ventilacao == "Bem ventilado 🟢":
                vent_factor = 1.0
            elif ventilacao == "Moderado 🟡":
                vent_factor = 0.9
            else:
                vent_factor = 0.8

            nominal = cooler.get("tdp_nominal", 0.0)
            capacity_eff, base_pct, dynamic_pct = compute_effective_capacity(nominal, cpu_tdp_adj, vent_factor)

            power_generated = cpu_tdp_adj * (workload_slider / 100.0)
            utilization_pct = round((power_generated / capacity_eff) * 100.0, 1) if capacity_eff > 0 else 999.9

            temp_est = estimate_temperature(cpu_tdp_adj, capacity_eff, ambient_c=ambient, workload=workload_slider / 100.0, f_avg=f_avg_cpu)
            noise_est = estimate_noise(cooler, utilization_pct)
            dur_est = estimate_durability(cooler, utilization_pct)

            st.markdown("### Resultado")
            st.write(f"*CPU:* {cpu['modelo']} — TDP nominal: {cpu['tdp']} W")
            st.write(f"*Frequência média (base/turbo):* {f_avg_cpu:.2f} GHz (ajuste freq: {freq_pct}%)")
            st.write(f"*Arquitetura / fator aplicado:* {cpu.get('arquitetura','-')} → fator {arch_factor}")
            st.write(f"*TDP ajustado (freq + arquitetura) (sem +30%):* {cpu_tdp_adj_no_extra:.1f} W")
            st.write(f"*TDP usado no cálculo (aplicando +30%):* {cpu_tdp_adj:.1f} W")
            st.write(f"*Cooler:* {cooler['modelo']} ({cooler['tipo']}) — Nominal ajustado (90%): {nominal} W")
            if "tdp_manufacturer" in cooler:
                st.write(f"*Especificação fabricante:* {cooler['tdp_manufacturer']} W (aplicado → {nominal} W)")
            st.write(f"*Condição do gabinete:* {ventilacao} (fator aplicado: {vent_factor})")
            st.write(f"*Capacidade efetiva aplicada:* {capacity_eff:.1f} W (redução base {base_pct}% + dinâmica {dynamic_pct}%)")
            st.write(f"*Carga aplicada:* {workload_slider}% → potência gerada: {power_generated:.1f} W")
            st.write(f"*Utilização da capacidade efetiva:* {utilization_pct}%")
            st.write(f"*Temperatura estimada (IHS) em carga:* {temp_est} °C (ambiente {ambient} °C)")
            st.write(f"*Ruído estimado:* {noise_est} dB")
            st.write(f"*Durabilidade estimada:* ~{dur_est} anos")

            if utilization_pct <= 70:
                st.success("Sistema seguro: cooler com folga adequada.")
            elif utilization_pct <= 90:
                st.info("Sistema adequado: operação dentro dos limites.")
            else:
                st.error("Risco: capacidade efetiva do cooler pode ser insuficiente. Considere um modelo mais potente.")

            if show_detailed:
                st.markdown("### Gráfico: Temperatura vs Carga")
                loads = np.linspace(10, 150, 50)
                temps = [estimate_temperature(cpu_tdp_adj, capacity_eff, ambient_c=ambient, workload=l/100.0, f_avg=f_avg_cpu) for l in loads]

                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(loads, temps, linewidth=2)
                ax.scatter([workload_slider], [temp_est], color="red", zorder=5)
                ax.set_xlabel("Carga do processador (% do TDP)")
                ax.set_ylabel("Temperatura estimada (°C)")
                ax.set_title(f"Temperatura estimada — {cpu['modelo']} + {cooler['modelo']}")
                ax.grid(True, linestyle='--', alpha=0.6)
                ax.axvline(workload_slider, color='gray', linestyle=':', linewidth=1)
                st.pyplot(fig)

            st.markdown("### Comparativo: TDP efetivo vs Capacidade efetiva do cooler")
            fig2, ax2 = plt.subplots(figsize=(6, 3))
            ax2.bar(["TDP efetivo (W)", "Capacidade Efetiva (W)"], [power_generated, capacity_eff], color=["#2f72b7", "#7f8fa6"])
            ax2.set_ylabel("Potência (W)")
            ax2.set_ylim(0, max(capacity_eff, power_generated) + 20)
            for i, (val, lab) in enumerate(zip([power_generated, capacity_eff], ["TDP", "Capacidade"])):
                ax2.text(i, val + max(1, 0.02 * val), f"{val:.1f}", ha='center', fontsize=10)
            st.pyplot(fig2)

with col_right:
    st.subheader("Detalhes rápidos")
    st.write("Use este painel para comparar rapidamente as métricas do cooler.")
    selected_cooler = st.selectbox("Visualizar dados do cooler", [c["modelo"] for c in COOLERS])
    cinfo = next((c for c in COOLERS if c["modelo"] == selected_cooler), None)
    if cinfo:
        st.write(f"Modelo: {cinfo['modelo']}")
        st.write(f"Tipo: {cinfo['tipo']}")
        st.write(f"Nominal (ajustado): {cinfo['tdp_nominal']} W")
        if "tdp_manufacturer" in cinfo:
            st.write(f"Especificação do fabricante: {cinfo['tdp_manufacturer']} W (aplicado → {cinfo['tdp_nominal']} W)")
        sample_cpu_tdp = 95.0
        sample_adj, _, _ = compute_adjusted_tdp_for_frequency({"tdp": sample_cpu_tdp, "frequencia_base": 3.5, "frequencia_turbo": 3.5, "ano": 2018})
        eff_ex, bp_ex, dp_ex = compute_effective_capacity(cinfo['tdp_nominal'], sample_adj, vent_factor=1.0)
        st.write(f"Capacidade efetiva (exemplo CPU 95W): {eff_ex:.1f} W")
        st.write(f"Ruído (médio): {cinfo['ruido_db']} dB")
        st.write(f"Durabilidade (estimada): {cinfo['durabilidade_anos']} anos")
    st.markdown("---")
    st.subheader("Observações sobre o modelo")
    st.write("""
    - Este simulador usa modelos heurísticos para comparações e estimativas.  
    - `tdp` do processador NÃO foi alterado; aplicamos um ajuste dinâmico baseado em frequência média e arquitetura para estimar comportamento térmico.  
    - Para aproximar consumo real em boost, aplicamos +30% ao TDP ajustado (aplicado somente nos cálculos).  
    - `tdp_manufacturer` (quando presente) foi ajustado para `tdp_nominal = 90%` como margem prática.  
    - A ventilação do gabinete reduz a capacidade efetiva do cooler (Bem ventilado 100%, Moderado 90%, Pouco 80%).  
    - Para medições precisas de temperatura utilize sensores reais (HWMonitor, HWiNFO) e testes práticos.
    """)

st.markdown("---")
st.caption("Versão final — CPUS originais preservadas; cálculo dinâmico (+30% TDP, ventilação, frequência ↔ temperatura) integrado.")
