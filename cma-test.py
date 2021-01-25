"""
Runs the Covariance Matrix Adaptation - Evolutionary
Strategy algorithm on a talk of the town simulation
to optimize for a distribution of story events
Distributions are measured as the percentage
of the residents in the town who are actively
engaged in story pattern of that type

For an overview of CMA-ES see:
https://en.wikipedia.org/wiki/CMA-ES
"""
import json
import random
from collections import OrderedDict
import numpy as np
import talktown
from talktown.simulation import Simulation
import cma

TALKTOWN_CONFIG = './talktown_config.json'

# Distribution of emergent stories to optimize for
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

# Error between target distribution and the
# mean disribution of stories during iterations
# of CMA-ES
error_history = []

def get_distrb_vector(distrb_dict):
    """Covert dictionary of distribution values to a vector"""
    vect = np.zeros(len(TARGET_DISTRIBUTION))

    for i, key in enumerate(TARGET_DISTRIBUTION):
        if key in distrb_dict:
            vect[i] = distrb_dict[key]
        else:
            vect[i] = 0.0

    return vect

def euclidian_distance(target, actual):
    """Return euclidian distance between distance vectors"""
    distance = np.subtract(target, actual) ** 2
    return np.sqrt(np.sum(distance))

def optimize_talktown(params):
    """
    Run ralktown and return the distance
    between target and actual story histograms
    """
    # Number of samples to take per CMA iteration
    samples = 20
    # Story distribution vectors from samples
    sample_data = np.zeros((samples, len(TARGET_DISTRIBUTION)))
    # Configuration passed to the simulation
    simulation_config = talktown.config.Config()
    simulation_config.load_json(TALKTOWN_CONFIG)
    # Modify config with given parameters
    simulation_config.story_recognition.spark_threshold_for_being_captivated = params[0]
    simulation_config.social_sim.spark_decay_rate = params[1]

    for i in range(samples):
        print("Sample: ", i)
        # Wrap simualtion in try/except to catch
        # simulation exceptions and ctrl-c keyboard interupts
        try:
            #Randomize seed every run
            simulation_config.basic.seed = int(random.random()*9999999)
            sim = Simulation(config=simulation_config, verbose=False)

            sim.establish_setting()

            sim.story_recognizer.excavate(verbose=False)

            resulting_distribution = {
                'love_triangles': sim.story_recognizer.proportion_in_love_triangle(),
                'extramarital_romance': sim.story_recognizer.proportion_in_extramarital_romance(),
                'unrequited_love': sim.story_recognizer.proportion_in_unrequited_love(),
                'asymmetric_friendships': sim.story_recognizer.proportion_in_asymmetric_friendship(),
                'misanthropes': sim.story_recognizer.proportion_in_misanthropy(),
                'rivalries': sim.story_recognizer.proportion_in_rivalry(),
                'sibling_rivalries': sim.story_recognizer.proportion_in_sibling_rivalry(),
                'business_owner_rivalries': sim.story_recognizer.proportion_in_business_rivalry(),
            }

            sample_data[i,:] = get_distrb_vector(resulting_distribution)

        except KeyboardInterrupt:
            print("Stopping simualtion.")
            break

        except Exception as e:
            print("Caught error: {}".format(e))
            print("Skipping Sample")
            continue

    mean = np.mean(sample_data, axis=0)
    error = euclidian_distance(get_distrb_vector(TARGET_DISTRIBUTION), mean)
    error_history.append(error)
    return error


if __name__ == "__main__":
    es = cma.CMAEvolutionStrategy((20, 0.8), 0.5)
    es.optimize(optimize_talktown, iterations=10)

    results = {
        "error": error_history,
        "solution": list(es.result.xbest)
    }

    with open('./data/cma-result.json', 'w') as f:
        json.dump(results, f)
