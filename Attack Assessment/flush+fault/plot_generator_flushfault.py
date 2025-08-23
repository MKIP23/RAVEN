import matplotlib.pyplot as plt
import numpy as np

# Set style for professional plots
plt.style.use('seaborn-whitegrid')

# Time axis (adjust to max data length)
time_points = np.linspace(0, 11, 12)

# Independent metric data decode resolved, fetch sent
mispred_attack = [
    4.308e+4, 1.466e+4, 1.495e+7, 1.514e+7, 1.514e+7, 1.512e+7, 7.962e+5, 5.475e+3, 6.492e+3, 5.425e+3, 5.440e+3, 6.128e+3, 5.425e+3, 5.444e+3, 5.425e+3, 5.425e+3, 6.045e+3, 5.425e+3, 6.516e+3, 5.421e+3
]
lookups_attack = [
    6.694e+4, 3.134e+4, 2.295e+7, 2.320e+7, 2.320e+7, 2.319e+7, 1.217e+6, 1.095e+4, 1.240e+4, 1.055e+4, 1.057e+4, 1.183e+4, 1.070e+4, 1.079e+4, 1.078e+4, 1.078e+4, 1.181e+4, 1.078e+4, 1.238e+4, 1.077e+4
]

mispred_benign = [
    5.258e+3, 5.258e+3, 5.259e+3, 5.258e+3, 5.878e+3, 5.261e+3, 5.258e+3, 6.368e+3, 5.275e+3, 5.276e+3, 5.897e+3, 5.275e+3, 5.275e+3, 5.275e+3]

lookups_benign = [
    1.052e+4, 1.051e+4, 1.052e+4, 1.052e+4, 1.153e+4, 1.053e+4, 1.051e+4, 1.227e+4, 1.058e+4, 1.058e+4, 1.156e+4, 1.058e+4, 1.058e+4, 1.058e+4]

# Main data dictionary
data = {
    "L1I Cache Miss Rate": {
        "attack": [6.895e-2, 4.486e-2, 2.442e-2, 2.547e-2, 2.544e-2, 2.546e-2, 2.856e-2, 1.748e-2, 3.551e-2, 1.805e-2, 1.883e-2, 2.730e-2, 1.795e-2],
        "benign": [6.895e-2, 1.470e-2, 1.471e-2, 1.470e-2, 1.470e-2, 2.268e-2, 1.468e-2, 1.471e-2, 3.073e-2, 1.463e-2, 1.578e-2, 2.372e-2, 1.463e-2]
    },
    "Branch Mispredict Rate": {
        "attack": [round((m / l), 3) for m, l in zip(mispred_attack, lookups_attack)],
        "benign": [round((m / l), 3) for m, l in zip(mispred_benign, lookups_benign)]
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
