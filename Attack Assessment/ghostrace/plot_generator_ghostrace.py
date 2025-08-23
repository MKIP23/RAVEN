import matplotlib.pyplot as plt
import numpy as np

# Set style for professional plots
plt.style.use('seaborn-whitegrid')

# Time axis (adjust to max data length)
time_points = np.linspace(0, 11, 12)

# Independent metric data decode resolved, fetch sent
mispred_attack = [
    4.195e+4, 2.543e+4, 1.880e+5, 5.549e+3, 4.975e+3, 6.168e+3, 4.975e+3, 4.981e+3, 5.650e+3, 4.900e+3, 4.900e+3, 4.900e+3, 4.900e+3, 5.486e+3, 4.911e+3, 6.200e+3, 5.000e+3, 4.999e+3, 5.652e+3, 5.001e+3
]
lookups_attack = [
    6.511e+4, 4.579e+4, 2.862e+5, 1.095e+4, 9.800e+3, 1.176e+4, 9.950e+3, 9.954e+3, 1.107e+4, 9.775e+3, 9.775e+3, 9.775e+3, 9.775e+3, 1.071e+4, 9.793e+3, 1.181e+4, 1.028e+4, 1.026e+4, 1.128e+4, 1.028e+4
]

mispred_benign = [
    5.258e+3, 5.258e+3, 5.259e+3, 5.258e+3, 5.878e+3, 5.261e+3, 5.258e+3, 6.368e+3, 5.275e+3, 5.276e+3, 5.897e+3, 5.275e+3, 5.275e+3, 5.275e+3]

lookups_benign = [
    1.052e+4, 1.051e+4, 1.052e+4, 1.052e+4, 1.153e+4, 1.053e+4, 1.051e+4, 1.227e+4, 1.058e+4, 1.058e+4, 1.156e+4, 1.058e+4, 1.058e+4, 1.058e+4]

# Main data dictionary
data = {
    "L1D Cache Miss Rate": {
        "attack": [ 4.235e-2, 2.082e-2, 5.745e-2, 5.019e-3, 0.000e+0, 5.717e-3, 0.000e+0, 3.737e-5, 4.181e-4, 0.000e+0, 0.000e+0, 0.000e+0, 0.000e+0],
        "benign": [4.214e-4, 0.000e+0, 0.000e+0, 0.000e+0, 3.417e-5, 0.000e+0, 0.000e+0, 4.447e-3, 0.000e+0, 3.646e-6, 2.783e-4, 0.000e+0, 0.000e+0, 0.000e+0, 0.000e+0, 3.420e-5, 0.000e+0, 3.951e-4, 0.000e+0]
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
