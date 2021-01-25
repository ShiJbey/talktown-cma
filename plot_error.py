import json
import numpy as np
from matplotlib import pyplot as plt

CMA_OUT = './data/cma-result_inter_10_sample_20.json'

if __name__ == '__main__':
    with open(CMA_OUT, 'r') as f:
        error = np.array(json.load(f)["error"])

    x = np.arange(len(error))
    fig, ax = plt.subplots()
    p1 = ax.plot(x, error)
    ax.set_title('CMA-ES Error')
    ax.set_ylabel('Error')
    ax.set_xlabel('batch sample')
    fig.tight_layout()
    plt.show()
