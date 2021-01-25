import json
from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


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

def get_distrb_vector(distrb_dict):
    """Covert dictionary of distribution values to a vector"""
    vect = np.zeros(len(TARGET_DISTRIBUTION))

    for i, key in enumerate(TARGET_DISTRIBUTION):
        if key in distrb_dict:
            vect[i] = distrb_dict[key]
        else:
            vect[i] = 0.0

    return vect

def load_narrative_data(filename):
    """Load narrative data from JSON"""
    with open(filename, 'r') as f:
        data = json.load(f)

    data_matrix = np.zeros((len(data), len(TARGET_DISTRIBUTION)))

    for i, data_entry in enumerate(data):
        for j, key in enumerate(TARGET_DISTRIBUTION):
            data_matrix[i][j] = data_entry[key]

    return data_matrix


initial = load_narrative_data('./data/initial_distr_100_years_50_samples.json')
target = get_distrb_vector(TARGET_DISTRIBUTION)
optimized = load_narrative_data('./data/opt_distr_100_years_50_samples.json')

x = np.arange(len(BAR_LABELS))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()

rects1 = ax.bar(x - width/2,
                np.mean(initial, axis=0),
                width/3,
                yerr= np.std(initial, axis=0),
                label='initial')
rects2 = ax.bar(x - width/6,
                np.mean(target, axis=0),
                width/3,
                yerr= np.std(target, axis=0),
                label='target')
rects3 = ax.bar(x + width/6,
                np.mean(optimized, axis=0),
                width/3,
                yerr= np.std(optimized, axis=0),
                label='optimized')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('Distribution of Emergent Narratives')
ax.set_ylabel('Proportion of Residents')
ax.set_xticks(x)
ax.set_xticklabels(BAR_LABELS, rotation = -90)
ax.legend()

fig.tight_layout()

plt.show()
