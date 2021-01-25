# This script generates a history
# of story distributions from random runs
# of Talk of the Town. All parameters are kept
# constant, but the random seed changes each
# run
import json
import random
import talktown
from talktown.simulation import Simulation

TALKTOWN_CONFIG = './talktown_config.json'
OUTPUT_FILE = "./data/initial_distr_1_years_50_samples.json"
SAMPLES = 60

if __name__ == '__main__':

    histogram_data = []
    simulation_config = talktown.config.Config()
    simulation_config.load_json(TALKTOWN_CONFIG)

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
