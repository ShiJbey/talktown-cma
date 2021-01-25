import json
from collections import OrderedDict
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


BAR_LABELS = [
    'love triangle',
    'extramarital romance',
    'unrequited love',
    'asymmetric friendship',
    'misanthropy',
    'rivalry',
    'sibling rivalry',
    'business rivalry'
]

TARGET_DISTRIBUTION = OrderedDict([
    ('love_triangles', 0.3),
    ('extramarital_romance', 0.3),
    ('unrequited_love', 0.3),
    ('asymmetric_friendships', 0.3),
    ('misanthropes', 0.3),
    ('rivalries', 0.3),
    ('sibling_rivalries', 0.3),
    ('business_owner_rivalries', 0.3)
])

def load_narrative_data(filename):
    """Load narrative data from JSON"""
    with open(filename, 'r') as f:
        data = json.load(f)

    data_matrix = np.zeros((len(data), len(TARGET_DISTRIBUTION)))

    for i, data_entry in enumerate(data):
        for j, key in enumerate(TARGET_DISTRIBUTION):
            data_matrix[i][j] = data_entry[key]

    return data_matrix

data_100yr = load_narrative_data('./data/initial_distr_100_years_50_samples.json')
data_50yr = load_narrative_data('./data/initial_distr_50_years_50_samples.json')
data_25yr = load_narrative_data('./data/initial_distr_25_years_50_samples.json')


x = np.arange(len(BAR_LABELS))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()

rects1 = ax.bar(x - width/2,
                np.mean(data_25yr, axis=0),
                width/3,
                yerr= np.std(data_25yr, axis=0),
                label='25 years')
rects2 = ax.bar(x - width/6,
                np.mean(data_50yr, axis=0),
                width/3,
                yerr= np.std(data_50yr, axis=0),
                label='50 years')
rects3 = ax.bar(x + width/6,
                np.mean(data_100yr, axis=0),
                width/3,
                yerr= np.std(data_100yr, axis=0),
                label='100 years')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('Distribution of Emergent Narratives')
ax.set_ylabel('Proportion of Residents')
ax.set_xticks(x)
ax.set_xticklabels(BAR_LABELS, rotation = -90)
ax.legend()

fig.tight_layout()

plt.show()
