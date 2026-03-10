import matplotlib
matplotlib.use("Agg")
import re
import numpy as np
import matplotlib.pyplot as plt

# Files and status
files = {
    "tau001000um_M3000 (SUCCESS)": "condor_mfv_neu_tau001000um_M3000_20161.log",
    "tau010000um_M1600 (SUCCESS)": "condor_mfv_neu_tau010000um_M1600_20161.log",
    "tau010000um_M3000 (FAILED)":  "condor_mfv_neu_tau010000um_M3000_20161.log",
    "tau030000um_M3000 (FAILED)":  "condor_mfv_neu_tau030000um_M3000_20161.log",
}

def extract_seed_tracks(filename):
    values = []
    pattern = re.compile(r"n_seed_tracks=(\d+)")
    with open(filename) as f:
        for line in f:
            match = pattern.search(line)
            if match:
                values.append(int(match.group(1)))
    return values

# Collect data
data = {}
all_values = []
for label, fname in files.items():
    vals = extract_seed_tracks(fname)
    data[label] = vals
    all_values.extend(vals)

# Define bins of width 5
max_val = max(all_values)
bins = np.arange(0, max_val + 5, 5)

# Plot
plt.figure(figsize=(8,6))

for label, vals in data.items():
    if len(vals) == 0:
        continue
    mean = np.mean(vals)
    sigma = np.std(vals)
    n_events = len(vals)
    legend_label = f"{label} (N={n_events}, μ={mean:.1f}, σ={sigma:.1f})"
    plt.hist(
        vals,
        bins=bins,
        histtype='step',
        linewidth=2,
        density=True,   # normalize to compare shapes
        label=legend_label
    )

plt.xlabel("Number of seed tracks")
plt.ylabel("Normalized events")
plt.title("Seed Track Distribution (Normalized Comparison)")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig("seed_track_comparison.png")