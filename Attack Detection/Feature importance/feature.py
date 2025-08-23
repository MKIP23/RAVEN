import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# The data provided from the screenshot
data = {
    'l1icaches.tags.tagsInUse': 0.017865,
    'l1dcaches.LoadLockedReq.hits::total': 0.012189,
    'l1dcaches.LoadLockedReq.missRate::total': 0.012163,
    'l1dcaches.LoadLockedReq.hits::processor.cores.core.data': 0.011980,
    'l1dcaches.LoadLockedReq.missRate::processor.cores.core.data': 0.011886,
    'l1dcaches.tags.tagsInUse': 0.010788,
    'l1dcaches.LoadLockedReq.mshrMissRate::total': 0.010068,
    'l1dcaches.SwapReq.mshrHits::total': 0.009986,
    'l1dcaches.LoadLockedReq.mshrMissRate::processor.cores.core.data': 0.009914,
    'l1dcaches.SwapReq.mshrHits::processor.cores.core.data': 0.009833,
    'processor.cores.core.branchPred.targetWrong_0::CallIndirect': 0.008557,
    'processor.cores.core.mmu.dtb.readMisses': 0.008250,
    'processor.cores.core.fpInstQueueWrites': 0.007734,
    'processor.cores.core.fpAluAccesses': 0.007635,
    'processor.cores.core.fpInstQueueReads': 0.007504
}

# The user-specified short labels
short_labels_map = {
    'l1icaches.tags.tagsInUse': 'l1i tags usage',
    'l1dcaches.LoadLockedReq.hits::total': 'l1d hits total',
    'l1dcaches.LoadLockedReq.missRate::total': 'l1d miss rate total',
    'l1dcaches.LoadLockedReq.hits::processor.cores.core.data': 'l1d hits data',
    'l1dcaches.LoadLockedReq.missRate::processor.cores.core.data': 'l1d miss rate data',
    'l1dcaches.tags.tagsInUse': 'l1d tags usage',
    'l1dcaches.LoadLockedReq.mshrMissRate::total': 'l1d l mshr miss rate total',
    'l1dcaches.SwapReq.mshrHits::total': 'l1d mshr hits total',
    'l1dcaches.LoadLockedReq.mshrMissRate::processor.cores.core.data': 'l1d mshr miss rate data',
    'l1dcaches.SwapReq.mshrHits::processor.cores.core.data': 'l1d mshr hits data',
    'processor.cores.core.branchPred.targetWrong_0::CallIndirect': 'branch pred target wrong',
    'processor.cores.core.mmu.dtb.readMisses': 'mmu dbt read misses',
    'processor.cores.core.fpInstQueueWrites': 'fp inst queue writes',
    'processor.cores.core.fpAluAccesses': 'fp alu accesses',
    'processor.cores.core.fpInstQueueReads': 'fp inst queue reads',
}

# Sort the data from highest to lowest value
sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=False)
sorted_features_full, sorted_values = zip(*sorted_data)
sorted_features_short = [short_labels_map[f] for f in sorted_features_full]

# Define colors and hatches for each bar
colors = [
    '#FF6347', '#4682B4', '#32CD32', '#FFD700', '#DA70D6',
    '#6A5ACD', '#87CEFA', '#FF69B4', '#CD5C5C', '#8FBC8F',
    '#9ACD32', '#D2B48C', '#F4A460', '#BA55D3', '#B0C4DE'
]

hatches = [
    '/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*',
    '//', '..', 'xx', '||', '--'
]

# Create the plot
# Use 'seaborn-v0_8-white' to get a white background and no grid
plt.style.use('seaborn-v0_8-white')
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the bars with different colors and hatches
bars = ax.barh(sorted_features_short, sorted_values)
for i, bar in enumerate(bars):
    # Set the facecolor to white to make the bars transparent
    bar.set_facecolor('white')
    # Set the edgecolor to match the facecolor for colored hatches
    bar.set_edgecolor(colors[i % len(colors)])
    bar.set_hatch(hatches[i % len(hatches)])

# Set title and labels
ax.set_title('Feature Importance', fontsize=22, fontweight='bold', pad=20)
ax.set_xlabel('Feature Importance Value', fontsize=18)
ax.set_ylabel('Features', fontsize=18)

# Set the font size for the y-axis labels
plt.yticks(fontsize=16)
plt.xticks(fontsize=16)

# Add a legend for the hatches (since there are too many colors to label)
# We create a patch for each hatch and add it to the legend
hatches_legend_patches = [mpatches.Patch(facecolor='grey', edgecolor='black', hatch=h, label=f'Hatch {i+1}') for i, h in enumerate(hatches)]
# ax.legend(handles=hatches_legend_patches, title='Bar Hatches', bbox_to_anchor=(1.05, 1), loc='upper left')

# Add values on the bars
for index, value in enumerate(sorted_values):
    ax.text(value, index, f'  {value:.4f}', va='center', fontsize=14)

# Adjust the x-axis limits to create space for the text labels
ax.set_xlim(right=sorted_values[0] + 0.012)

# Set tight layout to prevent labels from being cut off
plt.tight_layout()

# Save the plot to a high-quality PDF file
plt.savefig('feature_importance_plot.pdf', bbox_inches='tight', dpi=300)

# Display the plot
plt.show()

# A print statement to inform the user that the plot has been generated and saved.
print("Plot generated and saved as 'feature_importance_plot.pdf'.")
