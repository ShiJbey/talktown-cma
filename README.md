# Talktown CMA-ES (Unsupported)

This was my final project for UCSC's CMPM280X - Machine Playtesting class. I attempted to use Covariance Matrix Adaptation - Evolutionary Strategy to optimize the input parameters of Talk of the Town to produce a target distribution of emergent stories.

My attempt was not successful, but I am leaving this code here incase anyone finds it interesting in the future.

## File structure
* ```cma-test.py``` - main file that runs all CMA-ES and Talk of the Town. It outputs a JSON file with the  final results of CMA-ES
```typescript
{
  // Error after each sample
  error: number[];
  // Final solution for input parameters
  solution: number[];
}
```
* ```compare_initial_distr.py``` - Compare the initila distributions of emergent stories
* ```get_initial_distr.py``` - Get the initial distribution of stories from talk of the town
* ```get_optimized_distr.py``` - Get the distribution of emergent stories using the parameters found by CMA-ES
* ```plot_all_distros.py``` - Plots multiple story distributions in the same bar graph
* ```plot_distro.py``` - Plot a single distribution as a bar graph
* ```Plot the error curve from CMA-ES results.```
* ```talktown_config.json``` - Config file passed to the Talk of the Town instance
