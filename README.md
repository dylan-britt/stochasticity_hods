# stochasticity_hods
Example script for generating mock galaxy catalogs from halo occupation distributions (HODs) described in Britt et al. 2024 (https://arxiv.org/abs/2404.04252).

Included are the following files:

  - galaxy_mock.py: an example script for loading an HOD and populating one of the AbacusSummit cosmological simulations
  - config.yaml: a configuration file with simulation and HOD settings, passed to the python script via --config
  - hods_ab_200.hdf5: data file containing parameters for 200 Monte Carlo sampled HODs with redMaGiC-like galaxy bias and density
  - hods_noab_500.hdf5: likewise for a set of 500 HODs with assembly bias parameters turned off
