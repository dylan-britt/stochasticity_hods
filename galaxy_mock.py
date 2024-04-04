import h5py
import time
import yaml
import datetime
import argparse
from abacusnbody.hod.abacus_hod import AbacusHOD


def main(config_path):
    
    # load settings for simulation and HOD from the config file
    config = yaml.safe_load(open(config_path))
    want_rsd = config['hod_params']['want_rsd']
    write_to_disk = config['hod_params']['write_to_disk']
    
    # create the HOD object
    print(f"\n{config['sim_params']['sim_name']}, z={config['sim_params']['z_mock']}\n" + '-' * 50)
    hod = AbacusHOD(config['sim_params'], config['hod_params'])
    print('-' * 50)
    
    param_names = ['logM_cut', 'logM1', 'sigma', 'alpha', 'ic', 'Acent', 'Asat', 'Bcent', 'Bsat']
    
    # load selected HOD from file and set LRG parameters in hod.tracers
    hod_filepath = config['hod_filepath']
    hod_index = config['hod_index']
    with h5py.File(hod_filepath, 'r') as f:
        for _name in param_names:
            hod.tracers['LRG'][_name] = f[_name][hod_index]
            
    print(f'loaded HOD index {hod_index} from file: {hod_filepath}\n')
    
    # run the HOD to generate a mock galaxy catalog (first run will be slower due to compiling)
    mock = hod.run_hod(hod.tracers, want_rsd, reseed=None,
                       write_to_disk=write_to_disk, Nthread=config['nthread'])

    ntot = len(mock['LRG']['x'])

    print('-' * 50)
    print(f"{'total galaxy count:':<25}{ntot:,}")
    print(f"{'mean density:':<25}{ntot / (hod.params['Lbox'] ** 3):.3e} h^3 Mpc^{{-3}}")
    print(f"{'satellite fraction:':<25}{1.0 - mock['LRG']['Ncent'] / ntot:.4f}")
    print(f"{'mock dictionary keys:':<25}{list(mock['LRG'].keys())}")

    # extend this script as needed to compute properties of your mock catalogs, run mocks for multiple HODs, save data, etc.


    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='path to .yaml configuration file')
    args = parser.parse_args()
    
    t0 = time.time()
    main(args.config)
    print(f'done, script took {datetime.timedelta(seconds=round(time.time()-t0))}')
