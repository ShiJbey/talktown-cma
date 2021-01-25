# plot bar chart with distributions of the
# different types of storiescharacter are involved with
import json
from collections import OrderedDict
import numpy as np
from matplotlib import pyplot as plt

INITIAL_DISTR_FILENAME = './data/initial_distr_1_years_50_samples.json'

LABELS = (
    'love triangle',
    'extramarital romance',
    'unrequited love',
    'asymmetric friendship',
    'misanthropy',
    'rivalry',
    'sibling rivalry',
    'business rivalry'
)

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

if __name__ == '__main__':



    with open(INITIAL_DISTR_FILENAME, 'r') as f:
        data = json.load(f)

    data_matrix = np.zeros((len(data), len(LABELS)))

    for i, data_entry in enumerate(data):
        for j, key in enumerate(TARGET_DISTRIBUTION):
            data_matrix[i][j] = data_entry[key]

    mean = np.mean(data_matrix, axis=0)
    std = np.std(data_matrix, axis=0)

    print("mean: ", mean)
    print("std: ", std)

    width = 0.35

    fig, ax = plt.subplots()
    p1 = ax.bar(np.arange(mean.size), mean, width, yerr=std)
    ax.set_title('Distribution of Emergent Narratives (100 years)')
    ax.set_ylabel('Proportion of Residents')
    ax.set_xticks(np.arange(len(LABELS)))
    ax.set_xticklabels(LABELS, rotation = -90)

    fig.tight_layout()
    plt.show()
