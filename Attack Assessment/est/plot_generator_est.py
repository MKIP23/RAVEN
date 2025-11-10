import matplotlib.pyplot as plt
import numpy as np

# Set style for professional plots
plt.style.use('seaborn-whitegrid')

# Time axis (adjust to max data length)
time_points = np.linspace(0, 11, 12)

# Independent metric data
mispred_attack = [
    1.336e+4, 3.650e+2, 1.176e+4, 1.500e+2, 1.500e+2, 2.030e+2, 1.510e+2, 1.500e+2, 2.860e+2, 1.500e+2, 1.580e+2, 1.920e+2, 1.500e+2, 1.500e+2, 1.500e+2, 1.500e+2, 1.860e+2, 1.500e+2, 2.090e+2, 1.500e+2
]
lookups_attack = [
    5.145e+6, 1.080e+7, 1.022e+7, 1.713e+4, 1.710e+4, 1.897e+4, 1.686e+4, 1.677e+4, 2.011e+4, 1.680e+4, 1.689e+4, 1.852e+4, 1.680e+4, 1.680e+4, 1.680e+4, 1.680e+4, 1.849e+4, 1.687e+4, 1.969e+4, 1.687e+4
]

mispred_benign = [
    4.001e+2, 1.500e+2, 1.500e+2, 1.500e+2, 1.500e+2, 1.890e+2, 1.500e+2, 1.500e+2, 2.910e+2, 1.500e+2, 1.540e+2, 1.910e+2, 1.500e+2, 1.500e+2, 1.500e+2, 1.500e+2, 1.860e+2, 1.500e+2, 2.070e+2, 1.500e+2]

lookups_benign = [
    1.406e+5, 1.670e+4, 1.670e+4, 1.670e+4, 1.670e+4, 1.837e+4, 1.670e+4, 1.667e+4, 2.013e+4, 1.670e+4, 1.672e+4, 1.842e+4, 1.673e+4, 1.673e+4, 1.673e+4, 1.673e+4, 1.834e+4, 1.673e+4, 1.972e+4, 1.680e+4]
# Branch prediction hit ratios
attack_hit_ratios = [6.716e-1, 4.607e-1, 4.160e-1, 4.159e-1, 4.254e-1, 4.119e-1, 4.122e-1, 4.233e-1, 4.145e-1, 4.136e-1, 4.252e-1, 4.144e-1, 4.145e-1, 4.144e-1, 4.145e-1, 4.263e-1, 4.170e-1, 4.335e-1, 4.170e-1]
benign_hit_ratios = [8.516e-1, 8.860e-1, 8.323e-1, 8.317e-1, 8.323e-1, 8.328e-1, 8.316e-1, 8.316e-1, 8.321e-1, 8.314e-1, 8.318e-1, 8.317e-1, 8.314e-1, 8.322e-1, 8.319e-1, 8.320e-1, 8.324e-1, 8.319e-1]

# Calculate mispredict rates (1 - hit ratio)
attack_mispredict_rates = [round(1 - hit_ratio, 3) for hit_ratio in attack_hit_ratios]
benign_mispredict_rates = [round(1 - hit_ratio, 3) for hit_ratio in benign_hit_ratios]

# Main data dictionary
data = {
    "L1D Cache Miss Rate": {
        "attack": [ 4.464e-4, 7.343e-4, 0.000e+0, 0.000e+0, 4.720e-3, 0.000e+0, 0.000e+0, 7.024e-3, 0.000e+0, 3.748e-5, 5.610e-4, 0.000e+0, 0.000e+0, 0.000e+0, 0.000e+0, 7.015e-5, 0.000e+0, 5.081e-4, 0.000e+0],
        "benign": [4.214e-4, 0.000e+0, 0.000e+0, 0.000e+0, 3.417e-5, 0.000e+0, 0.000e+0, 4.447e-3, 0.000e+0, 3.646e-6, 2.783e-4, 0.000e+0, 0.000e+0, 0.000e+0, 0.000e+0, 3.420e-5, 0.000e+0, 3.951e-4, 0.000e+0]
    },
    "L1I Cache Miss Rate": {
        "attack": [6.658e-3, 4.647e-5, 4.354e-3, 1.759e-2, 1.760e-2, 2.791e-2, 1.819e-2, 1.816e-2, 3.515e-2, 1.816e-2, 1.921e-2, 2.704e-2, 1.814e-2, 1.816e-2, 1.814e-2, 1.816e-2, 2.472e-2, 1.819e-2, 3.049e-2, 1.819e-2],
        "benign":[6.895e-2, 1.470e-2,  1.470e-2, 1.471e-2, 1.470e-2, 1.470e-2, 2.268e-2, 1.468e-2, 1.471e-2, 3.073e-2, 1.463e-2, 1.578e-2, 2.372e-2, 1.463e-2, 1.463e-2, 1.463e-2, 1.463e-2, 2.208e-2, 1.463e-2, 2.624e-2, 1.468e-2]
    },
    # "Branch Mispredict Rate": {
    #     "attack": [round((m / l), 3) for m, l in zip(mispred_attack, lookups_attack)],
    #     "benign": [round((m / l), 3) for m, l in zip(mispred_benign, lookups_benign)]
    # },
    # Update the data dictionary
    "Branch Mispredict Rate": {
        "attack": attack_mispredict_rates,
        "benign": benign_mispredict_rates
    },
    "ROB Full Events": {
        "attack": [1.849e+3, 1.188e+5, 1.003e+5, 0.000e+0, 0.000e+0, 1.000e+1, 0.000e+0, 0.000e+0, 8.200e+1, 0.000e+0, 0.000e+0, 0.000e+0, 0.000e+0, 0.000e+0, 0.000e+0, 0.000e+0, 0.000e+0, 0.000e+0, 0.000e+0, 0.000e+0],
        "benign": [1.420e+2, 0.000e+0, 0.000e+0, 0.000e+0, 0.000e+0, 3.000e+0, 0.000e+0, 0.000e+0, 8.300e+1, 0.000e+0, 0.000e+0, 3.000e+0, 0.000e+0, 0.000e+0, 0.000e+0, 0.000e+0, 1.000e+0, 0.000e+0, 0.000e+0, 0.000e+0]
    }
}

def create_plots(metric_name, values):
    # Length checks
    min_len = min(len(values['attack']), len(values['benign']), len(time_points))
    x_axis = time_points[:min_len]
    y_attack = values['attack'][:min_len]
    y_benign = values['benign'][:min_len]

    fig, ax = plt.subplots(figsize=(5, 5), dpi=600)

    ax.plot(x_axis, y_attack, color='maroon', linewidth=2, label='Attack')
    ax.plot(x_axis, y_benign, color='blue', linestyle=':', linewidth=2, label='Benign')

    ax.tick_params(axis='both', which='major', labelsize=18)
    ax.set_xlabel('Time (ticks)', fontsize=18)
    ax.set_ylabel(metric_name, fontsize=18)
    ax.legend(fontsize=18, loc='best')
    ax.grid(True, alpha=0.3)

    # Save figure
    plt.tight_layout()
    plt.savefig(f'{metric_name.replace(" ", "_")}_comparison.pdf')
    plt.close()

# Generate plots for all metrics
for metric_name, values in data.items():
    create_plots(metric_name, values)
