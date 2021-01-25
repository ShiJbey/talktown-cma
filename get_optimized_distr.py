import json
import random
from collections import OrderedDict
import numpy as np
import talktown
from talktown.simulation import Simulation

CMA_CONFIG = './data/cma-result_inter_10_sample_20.json'
TALKTOWN_CONFIG = './talktown_config.json'
OUTPUT_FILE = "./data/opt_distr_100_years_50_samples.json"
SAMPLES = 60




if __name__ == '__main__':

    histogram_data = []
    simulation_config = talktown.config.Config()
    simulation_config.load_json(TALKTOWN_CONFIG)

    # Load the parameters from CMAES
    with open(CMA_CONFIG, 'r') as f:
        cma_solution = json.load(f)["solution"]
        # Modify config with given parameters
        simulation_config.story_recognition.spark_threshold_for_being_captivated = cma_solution[0]
        simulation_config.social_sim.spark_decay_rate = cma_solution[1]


    try:
        for i in range(SAMPLES):


            try:
                print("Sample: {} of {}".format(i + 1, SAMPLES))

                #Randomize seed every run
                simulation_config.basic.seed = int(random.random()*9999999)
                sim = Simulation(config=simulation_config, verbose=True)

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

                histogram_data.append(resulting_distribution)

            except KeyboardInterrupt:
                print("Stopping simualtion.")
                break

            except Exception as e:
                print("Caught error: {}".format(e))
                print("Skipping Sample")
                continue

    finally:
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(histogram_data, f)

        print("Done")
