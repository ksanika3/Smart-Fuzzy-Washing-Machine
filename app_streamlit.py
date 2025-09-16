import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from fuzzy_logic import compute_settings

st.set_page_config(page_title="Smart Fuzzy Washing Machine", layout="wide")
st.title("🧺 Smart Fuzzy Washing Machine")

# ------------------ Streamlit sliders ------------------
dirt = st.slider("Dirtiness (0 = clean, 10 = very dirty)", 0, 10, 5)
load_val = st.slider("Load (0 = small, 10 = full)", 0, 10, 5)
stain_val = st.slider("Stains (0 = none, 10 = heavy)", 0, 10, 5)
fabric_str = st.selectbox("Fabric Type", ["Delicate", "Normal", "Heavy"])
fabric_val = {"Delicate": 0, "Normal": 5, "Heavy": 10}[fabric_str]
water_val = st.slider("Water Hardness (0 = soft, 10 = hard)", 0, 10, 5)
temp_val = st.slider("Temperature Preference (0 = low, 10 = high)", 0, 10, 5)
eco = st.checkbox("Eco Mode")
prewash = st.checkbox("Pre-Wash")

# ------------------ Compute fuzzy logic results ------------------
try:
    results = compute_settings(dirt, load_val, stain_val, fabric_val, water_val, temp_val, eco, prewash)
except Exception as e:
    st.error(f"Error computing fuzzy settings: {e}")
    st.stop()

# ------------------ Display results with explanations ------------------
st.subheader("Recommended Settings")

# Wash Time + Explanation
wash_explanation = []
if dirt < 4 and load_val > 6:
    wash_explanation.append("Low dirt but high load → extra time added for better cleaning.")
if dirt > 7:
    wash_explanation.append("High dirtiness → longer wash cycle.")
if temp_val > 7:
    wash_explanation.append("High temperature → slightly shorter cycle since hot water cleans faster.")
st.write(f"**Wash Time:** {results['wash_time']:.1f} min")
if wash_explanation:
    for e in wash_explanation:
        st.caption(f"📝 {e}")

# Detergent + Explanation
detergent_explanation = []
if dirt > 7:
    detergent_explanation.append("High dirtiness → more detergent needed.")
if water_val > 6:
    detergent_explanation.append("Hard water detected → extra detergent required.")
if eco:
    detergent_explanation.append("Eco mode reduces detergent by 10%.")
st.write(f"**Detergent:** {results['detergent']:.1f} ml")
if detergent_explanation:
    for e in detergent_explanation:
        st.caption(f"🧴 {e}")

# Rinse Cycles + Explanation
rinse_explanation = []
if load_val > 6:
    rinse_explanation.append("Large load → more rinse cycles needed.")
if prewash:
    rinse_explanation.append("Prewash enabled → extra rinse added.")
st.write(f"**Rinse Cycles:** {results['rinse_cycles']}")
if rinse_explanation:
    for e in rinse_explanation:
        st.caption(f"💧 {e}")

# Spin Speed + Explanation
spin_explanation = []
if stain_val < 3:
    spin_explanation.append("Low stains → gentle spin used.")
if stain_val > 7:
    spin_explanation.append("Heavy stains → high spin speed selected.")
if fabric_str == "Delicate":
    spin_explanation.append("Delicate fabric → spin speed reduced.")
st.write(f"**Spin Speed:** {results['spin_speed']:.0f} RPM")
if spin_explanation:
    for e in spin_explanation:
        st.caption(f"🔄 {e}")

# Soak Time + Explanation
soak_explanation = []
if stain_val > 6:
    soak_explanation.append("Heavy stains → soak time increased.")
if fabric_str == "Heavy":
    soak_explanation.append("Heavy fabric → more soak time for better water penetration.")
st.write(f"**Soak Time:** {results['soak_time']:.1f} min")
if soak_explanation:
    for e in soak_explanation:
        st.caption(f"⏱️ {e}")

# ------------------ Savings & Usage ------------------
st.subheader("Savings & Usage")
if eco:
    st.success(
        f"You save ₹{results['saving_money']:.2f}, "
        f"{results['saving_energy']*100:.0f}% energy, "
        f"{results['saving_water']:.1f} L water."
    )
else:
    st.info("Turn on Eco Mode to see money, energy and water savings!")

st.caption(
    f"Estimated total usage: {results['energy_kwh']:.2f} kWh energy, "
    f"{results['water_l']:.1f} L water, cost ₹{results['cost']:.2f}"
)

# ------------------ Fuzzy membership function plots ------------------
st.subheader("Membership Functions (Dirtiness & Load)")
dirtiness_plot = ctrl.Antecedent(np.arange(0, 11, 1), 'dirtiness_plot')
load_plot = ctrl.Antecedent(np.arange(0, 11, 1), 'load_plot')
dirtiness_plot.automf(3)
load_plot.automf(3)

fig, axs = plt.subplots(1, 2, figsize=(12, 4))
for label in ['poor', 'average', 'good']:
    axs[0].plot(dirtiness_plot.universe, dirtiness_plot[label].mf, label=label)
axs[0].set_title("Dirtiness")
axs[0].set_xlabel("Dirtiness")
axs[0].set_ylabel("Membership")
axs[0].legend()
axs[0].grid(True)

for label in ['poor', 'average', 'good']:
    axs[1].plot(load_plot.universe, load_plot[label].mf, label=label)
axs[1].set_title("Load")
axs[1].set_xlabel("Load")
axs[1].set_ylabel("Membership")
axs[1].legend()
axs[1].grid(True)

st.pyplot(fig)
