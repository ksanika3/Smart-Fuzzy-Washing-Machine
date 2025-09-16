import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import os

# ---------------- Inputs ----------------
dirtiness = ctrl.Antecedent(np.arange(0, 11, 1), 'dirtiness')
load = ctrl.Antecedent(np.arange(0, 11, 1), 'load')
stains = ctrl.Antecedent(np.arange(0, 11, 1), 'stains')
fabric = ctrl.Antecedent(np.arange(0, 11, 1), 'fabric')  # 0=delicate, 10=heavy
water_hardness = ctrl.Antecedent(np.arange(0, 11, 1), 'water_hardness')
temperature = ctrl.Antecedent(np.arange(0, 11, 1), 'temperature')

# ---------------- Outputs ----------------
wash_time = ctrl.Consequent(np.arange(0, 121, 1), 'wash_time')   # 0-120 min
detergent = ctrl.Consequent(np.arange(0, 101, 1), 'detergent')   # 0-100 ml
rinse_cycles = ctrl.Consequent(np.arange(0, 6, 1), 'rinse_cycles')  # 0-5 cycles
spin_speed = ctrl.Consequent(np.arange(0, 1601, 1), 'spin_speed')
soak_time = ctrl.Consequent(np.arange(0, 61, 1), 'soak_time')

# ---------------- Membership Functions ----------------
# Use automf(3) -> labels: 'poor', 'average', 'good'
for inp in [dirtiness, load, stains, fabric, water_hardness, temperature]:
    inp.automf(3)

wash_time['short'] = fuzz.trimf(wash_time.universe, [0, 20, 50])
wash_time['medium'] = fuzz.trimf(wash_time.universe, [30, 60, 90])
wash_time['long'] = fuzz.trimf(wash_time.universe, [80, 100, 120])

detergent['low'] = fuzz.trimf(detergent.universe, [0, 20, 40])
detergent['medium'] = fuzz.trimf(detergent.universe, [30, 50, 70])
detergent['high'] = fuzz.trimf(detergent.universe, [60, 80, 100])

rinse_cycles['few'] = fuzz.trimf(rinse_cycles.universe, [0, 1, 2])
rinse_cycles['normal'] = fuzz.trimf(rinse_cycles.universe, [1, 3, 4])
rinse_cycles['many'] = fuzz.trimf(rinse_cycles.universe, [3, 4, 5])

spin_speed['low'] = fuzz.trimf(spin_speed.universe, [0, 400, 800])
spin_speed['medium'] = fuzz.trimf(spin_speed.universe, [600, 1000, 1200])
spin_speed['high'] = fuzz.trimf(spin_speed.universe, [1000, 1300, 1600])

soak_time['short'] = fuzz.trimf(soak_time.universe, [0, 5, 15])
soak_time['medium'] = fuzz.trimf(soak_time.universe, [10, 20, 30])
soak_time['long'] = fuzz.trimf(soak_time.universe, [25, 40, 60])

# ---------------- Rules ----------------
rules = [
    # Wash time rules
    ctrl.Rule(dirtiness['poor'] | stains['poor'], wash_time['short']),
    ctrl.Rule(dirtiness['average'] & load['average'], wash_time['medium']),
    ctrl.Rule(dirtiness['good'] & load['good'] & stains['good'], wash_time['long']),
    ctrl.Rule(fabric['good'], wash_time['long']),  # heavy fabric -> longer wash

    # Detergent rules
    ctrl.Rule(dirtiness['poor'], detergent['low']),
    ctrl.Rule(dirtiness['average'], detergent['medium']),
    ctrl.Rule(dirtiness['good'], detergent['high']),
    ctrl.Rule(water_hardness['good'], detergent['high']),  # hard water -> more detergent

    # Rinse cycles rules
    ctrl.Rule(load['poor'], rinse_cycles['few']),
    ctrl.Rule(load['average'], rinse_cycles['normal']),
    ctrl.Rule(load['good'], rinse_cycles['many']),

    # Spin speed rules
    ctrl.Rule(stains['poor'], spin_speed['low']),
    ctrl.Rule(stains['average'], spin_speed['medium']),
    ctrl.Rule(stains['good'], spin_speed['high']),
    ctrl.Rule(fabric['poor'], spin_speed['low']),  # delicate fabric -> low spin

    # Temperature effect on wash time (higher temp shortens wash)
    ctrl.Rule(temperature['poor'], wash_time['short']),
    ctrl.Rule(temperature['average'], wash_time['medium']),
    ctrl.Rule(temperature['good'], wash_time['long']),

    # Soak time rules
    ctrl.Rule(stains['good'], soak_time['long']),
    ctrl.Rule(stains['average'], soak_time['medium']),
    ctrl.Rule(stains['poor'], soak_time['short']),
    ctrl.Rule(fabric['good'], soak_time['medium']),
]

# Build control system (no simulation created at import time)
system = ctrl.ControlSystem(rules)


# ---------------- Compute Function ----------------
def compute_settings(dirt, load_val, stain_val, fabric_val, water_hard_val, temp_val, eco=False, prewash=False):
    """
    Compute fuzzy washing settings.
    Returns a dictionary with results (wash_time, detergent, rinse_cycles, spin_speed, soak_time, energy/water/cost estimations).
    This function uses a fresh ControlSystemSimulation each call to avoid stale state.
    """
    # Adjust for eco / prewash
    if eco:
        # lower temperature preference for eco (optional logic)
        temp_val = max(0, temp_val - 2)
    if prewash:
        dirt = min(10, dirt + 2)

    # Create a fresh simulator each call
    sim = ctrl.ControlSystemSimulation(system)

    sim.input['dirtiness'] = float(dirt)
    sim.input['load'] = float(load_val)
    sim.input['stains'] = float(stain_val)
    sim.input['fabric'] = float(fabric_val)
    sim.input['water_hardness'] = float(water_hard_val)
    sim.input['temperature'] = float(temp_val)

    sim.compute()

    # Read outputs
    wash_out = float(sim.output['wash_time']) + (5.0 if prewash else 0.0)
    detergent_out = float(sim.output['detergent']) * (0.9 if eco else 1.0)
    rinse_out = int(round(float(sim.output['rinse_cycles']))) + (1 if prewash else 0)
    spin_out = float(sim.output['spin_speed'])
    soak_out = float(sim.output['soak_time'])

    # Simple usage & savings estimate (example constants)
    normal_energy_kwh = 1.0
    normal_water_l = 50.0
    normal_cost = 15.0

    if eco:
        energy_kwh = normal_energy_kwh * 0.8
        water_l = normal_water_l * 0.85
        cost = normal_cost * 0.8
    else:
        energy_kwh = normal_energy_kwh
        water_l = normal_water_l
        cost = normal_cost

    return {
        'wash_time': wash_out,
        'detergent': detergent_out,
        'rinse_cycles': rinse_out,
        'spin_speed': spin_out,
        'soak_time': soak_out,
        'energy_kwh': energy_kwh,
        'water_l': water_l,
        'cost': cost,
        'saving_money': normal_cost - cost,
        'saving_energy': normal_energy_kwh - energy_kwh,
        'saving_water': normal_water_l - water_l
    }


# ------------------ Optional: generate and save MF plots when run as script ------------------
if __name__ == "__main__":
    if not os.path.exists("images"):
        os.makedirs("images")

    # Dirtiness
    plt.figure(figsize=(6, 4))
    for label in ['poor', 'average', 'good']:
        plt.plot(dirtiness.universe, dirtiness[label].mf, label=label)
    plt.title("Dirtiness Membership Functions")
    plt.xlabel("Dirtiness")
    plt.ylabel("Membership")
    plt.legend()
    plt.grid(True)
    plt.savefig("images/dirtiness_mf.png")
    plt.close()

    # Load
    plt.figure(figsize=(6, 4))
    for label in ['poor', 'average', 'good']:
        plt.plot(load.universe, load[label].mf, label=label)
    plt.title("Load Membership Functions")
    plt.xlabel("Load")
    plt.ylabel("Membership")
    plt.legend()
    plt.grid(True)
    plt.savefig("images/load_mf.png")
    plt.close()

    print("Saved membership function images to ./images/")
