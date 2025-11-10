import matplotlib.pyplot as plt
import numpy as np

# Set style for professional plots
plt.style.use('seaborn-whitegrid')

# Time axis (adjust to max data length)
time_points = np.linspace(0, 11, 12)

# Independent metric data decode resolved, fetch sent
mispred_attack = [
    1.739e+7, 1.986e+7, 1.988e+7, 1.934e+7, 7.876e+3, 4.967e+3, 4.950e+3, 6.019e+3, 4.950e+3, 4.956e+3, 5.584e+3, 4.950e+3, 4.950e+3, 4.950e+3, 4.950e+3, 5.538e+3, 4.950e+3, 6.007e+3, 4.950e+3
]
lookups_attack = [
    2.771e+7, 2.985e+7, 2.987e+7, 2.907e+7, 1.487e+4, 9.857e+3, 9.825e+3, 1.147e+4, 9.825e+3, 9.828e+3, 1.081e+4, 9.825e+3, 9.825e+3, 9.825e+3, 9.825e+3, 1.075e+4, 9.825e+3, 1.138e+4, 9.825e+3
]

mispred_benign = [
    5.258e+3, 5.258e+3, 5.259e+3, 5.258e+3, 5.878e+3, 5.261e+3, 5.258e+3, 6.368e+3, 5.275e+3, 5.276e+3, 5.897e+3, 5.275e+3, 5.275e+3, 5.275e+3]

lookups_benign = [
    1.052e+4, 1.051e+4, 1.052e+4, 1.052e+4, 1.153e+4, 1.053e+4, 1.051e+4, 1.227e+4, 1.058e+4, 1.058e+4, 1.156e+4, 1.058e+4, 1.058e+4, 1.058e+4]
# Branch prediction hit ratios
attack_hit_ratios = [4.052e-1, 5.502e-1, 5.640e-1, 5.630e-1, 4.263e-1, 4.186e-1, 4.193e-1, 4.270e-1, 4.184e-1, 4.179e-1, 4.294e-1, 4.193e-1, 4.193e-1, 4.193e-1, 4.193e-1, 4.282e-1, 4.193e-1, 4.338e-1, 4.184e-1]
benign_hit_ratios = [8.516e-1, 8.860e-1, 8.323e-1, 8.317e-1, 8.323e-1, 8.328e-1, 8.316e-1, 8.316e-1, 8.321e-1, 8.314e-1, 8.318e-1, 8.317e-1, 8.314e-1, 8.322e-1, 8.319e-1, 8.320e-1, 8.324e-1, 8.319e-1]

# Calculate mispredict rates (1 - hit ratio)
attack_mispredict_rates = [round(1 - hit_ratio, 3) for hit_ratio in attack_hit_ratios]
benign_mispredict_rates = [round(1 - hit_ratio, 3) for hit_ratio in benign_hit_ratios]

# Main data dictionary
data = {
    "L1D Cache Miss Rate": {
        "attack": [ 6.302e-3, 6.747e-3, 6.758e-3, 6.813e-3, 1.032e-2, 3.715e-5, 0.000e+0, 5.517e-3, 0.000e+0, 3.711e-5, 4.168e-4, 0.000e+0],
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
