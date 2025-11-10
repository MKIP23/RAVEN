import matplotlib.pyplot as plt
import numpy as np

# Set style for professional plots
plt.style.use('seaborn-whitegrid')

# Time axis (adjust to max data length)
time_points = np.linspace(0, 11, 12)

# Independent metric data decode resolved, fetch sent
mispred_attack = [
    4.112e+6, 4.363e+5, 5.750e+3, 5.025e+3, 6.255e+3, 5.025e+3, 5.042e+3, 5.800e+3, 5.025e+3, 5.025e+3, 5.025e+3, 5.025e+3, 5.617e+3, 5.044e+3
]
lookups_attack = [
    7.736e+6, 9.053e+5, 1.143e+4, 1.018e+4, 1.205e+4, 1.015e+4, 1.017e+4, 1.136e+4, 1.015e+4, 1.015e+4, 1.015e+4, 1.015e+4, 1.106e+4, 1.019e+4
]

mispred_benign = [
    5.258e+3, 5.258e+3, 5.259e+3, 5.258e+3, 5.878e+3, 5.261e+3, 5.258e+3, 6.368e+3, 5.275e+3, 5.276e+3, 5.897e+3, 5.275e+3, 5.275e+3, 5.275e+3]

lookups_benign = [
    1.052e+4, 1.051e+4, 1.052e+4, 1.052e+4, 1.153e+4, 1.053e+4, 1.051e+4, 1.227e+4, 1.058e+4, 1.058e+4, 1.156e+4, 1.058e+4, 1.058e+4, 1.058e+4]
# Branch prediction hit ratios
attack_hit_ratios = [4.005e-1, 4.996e-1, 4.228e-1, 4.272e-1, 4.155e-1, 4.309e-1, 4.134e-1, 4.126e-1, 4.309e-1, 4.143e-1, 4.143e-1, 4.143e-1, 4.143e-1, 4.259e-1, 4.147e-1, 4.368e-1, 4.153e-1, 4.155e-1, 4.274e-1, 4.168e-1]

benign_hit_ratios = [8.516e-1, 8.860e-1, 8.323e-1, 8.317e-1, 8.323e-1, 8.328e-1, 8.316e-1, 8.316e-1, 8.321e-1, 8.314e-1, 8.318e-1, 8.317e-1, 8.314e-1, 8.322e-1, 8.319e-1, 8.320e-1, 8.324e-1, 8.319e-1]

# Calculate mispredict rates (1 - hit ratio)
attack_mispredict_rates = [round(1 - hit_ratio, 3) for hit_ratio in attack_hit_ratios]
benign_mispredict_rates = [round(1 - hit_ratio, 3) for hit_ratio in benign_hit_ratios]


# Main data dictionary
data = {
    "L1D Cache Miss Rate": {
        "attack": [3.019e-3, 1.197e-2, 2.993e-2, 1.859e-2, 3.428e-2, 1.862e-2, 1.962e-2, 2.711e-2, 1.862e-2, 1.862e-2, 1.862e-2, 1.862e-2],
        "benign": [4.214e-4, 0.000e+0, 0.000e+0, 0.000e+0, 3.417e-5, 0.000e+0, 0.000e+0, 4.447e-3, 0.000e+0, 3.646e-6, 2.783e-4, 0.000e+0, 0.000e+0, 0.000e+0, 0.000e+0, 3.420e-5, 0.000e+0, 3.951e-4, 0.000e+0]
    },
    "Branch Mispredict Rate": {
        "attack": attack_mispredict_rates,
        "benign": benign_mispredict_rates
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
