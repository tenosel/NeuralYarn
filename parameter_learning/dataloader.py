import glob
import numpy as np
import imageio
from torch.utils import data
from utils import read_file

def initialize_param_storage(num_files, param_config):
    """
    Initialize parameter storage arrays based on the given configuration.

    Args:
        num_files (int): Number of files to process.
        param_config (dict): Configuration dictionary specifying which parameters to extract.

    Returns:
        dict: A dictionary with initialized numpy arrays for parameter storage.
    """
    if 'thickness_y' in param_config:
        return {'threshold_y1': np.zeros(num_files), 'threshold_y2': np.zeros(num_files)}
    elif 'num_plies' in param_config:
        return {
            'num_plies2': np.zeros(num_files),
            'num_plies3': np.zeros(num_files),
            'num_plies4': np.zeros(num_files),
            'num_plies5': np.zeros(num_files),
            'num_plies6': np.zeros(num_files)
        }
    else:
        return {param: np.zeros(num_files) for param in param_config.keys()}

def read_files(folder_name):
    """
    Read and sort PNG and JSON files from the given folder.

    Args:
        folder_name (str): The path to the folder containing PNG and JSON files.

    Returns:
        tuple: A tuple containing two lists: sorted PNG filenames and sorted JSON filenames.
    """
    fnames_png = sorted(glob.glob(f"{folder_name}/*.png"))
    fnames_json = sorted(glob.glob(f"{folder_name}/*.json"))
    return fnames_png, fnames_json

def process_params(yarn, param_config, param_arrays, index):
    """
    Process and store parameters from the yarn data based on the configuration.

    Args:
        yarn (dict): The dictionary containing yarn data.
        param_config (dict): Configuration dictionary specifying which parameters to extract.
        param_arrays (dict): A dictionary with initialized numpy arrays for parameter storage.
        index (int): The current index of the file being processed.
    """
    if 'thickness_y' in param_config:
        thickness_y = yarn['thickness']['fiber_thickness_y']
        if thickness_y < 0.018:
            param_arrays['threshold_y1'][index] = 1
            param_arrays['threshold_y2'][index] = 0
        else:
            param_arrays['threshold_y1'][index] = 0
            param_arrays['threshold_y2'][index] = 1
    elif 'num_plies' in param_config:
        num_plies = yarn['fiber']['placement_params']['num_points']
        if num_plies == 2:
            param_arrays['num_plies2'][index] = 1
        elif num_plies == 3:
            param_arrays['num_plies3'][index] = 1
        elif num_plies == 4:
            param_arrays['num_plies4'][index] = 1
        elif num_plies == 5:
            param_arrays['num_plies5'][index] = 1
        elif num_plies == 6:
            param_arrays['num_plies6'][index] = 1
    else:
        for param, keys in param_config.items():
            value = yarn
            for key in keys:
                value = value[key]
            param_arrays[param][index] = value
            if 'ellipse' in param_config:
                ply_radius = yarn['fiber']['fiber_params']['yarn']['placement_params']['radius']
                param_arrays[param][index] *= ply_radius

def read_png_yarn_folder(folder_name, param_config):
    """Read PNG and JSON files from the folder and process the images and parameters.

    Args:
        folder_name (str): The path to the folder containing PNG and JSON files.
        param_config (dict): Configuration dictionary specifying which parameters to extract from the JSON files.

    Returns:
        tuple: A tuple containing the list of processed images and the corresponding parameter list.
    """
    fnames_png, fnames_json = read_files(folder_name)
    param_arrays = initialize_param_storage(len(fnames_png), param_config)
    ims = []
    
    for i, (fn_png, fn_json) in enumerate(zip(fnames_png, fnames_json)):
        if i % 10 == 0:
            print(f'Reading image {i + 1} / {len(fnames_png)}')
        
        # Read image
        im = imageio.imread(fn_png)
        im = im[:, :, :-1]
        img = np.array(im) / 255.0
        ims.append(img)

        yarn = read_file(fn_json)
        process_params(yarn, param_config, param_arrays, i)
    
    ims_params_list = np.array([param_arrays[param] for param in param_arrays.keys()]).T

    # Print means of parameters for debugging
    for param, array in param_arrays.items():
        print(f'mean {param}: {np.mean(array)}')

    return ims, ims_params_list

class YarnDataset(data.Dataset):
    """
    Dataset class for yarn images and parameters.

    Args:
        folder_path (str): Path to the folder containing the dataset.
        param_flag (str): Flag to specify which parameter configuration to use. Defaults to 'alphaply'.

    Attributes:
        ims_list (list): List of processed images.
        ims_params_list (list): List of corresponding parameters.
        dataset_size (int): Total number of samples in the dataset.
    """

    PARAM_CONFIGS = {
        'alphaply': {'alpha_ply': ['fiber', 'curve_params', 'dif_z']},
        'num_plies': {'num_plies': ['fiber', 'placement_params', 'num_points']},
        'flyaways': {
            'amount': ['flyaways', 'mapping_parameters', 'amount'],
            'loop_prob': ['flyaways', 'mapping_parameters', 'loop_prob'],
            'hair_length_mean': ['flyaways', 'mapping_parameters', 'hair_length_mean'],
            'hair_angle': ['flyaways', 'mapping_parameters', 'hair_angle'],
            'hair_squeeze': ['flyaways', 'mapping_parameters', 'fuzzyness'],
            'loop_length_mean': ['flyaways', 'mapping_parameters', 'loop_length_mean'],
            'loop_distance_mean': ['flyaways', 'mapping_parameters', 'loop_distance_mean'],
            'loop_distance_std': ['flyaways', 'mapping_parameters', 'loop_distance_std'],
            'jitter_xy': ['fiber', 'fiber_params', 'yarn', 'placement_params', 'jitter_xy'],
            'migration': ['fiber', 'fiber_params', 'yarn', 'curve_params', 'migration']
        },
        'thickness': {'thickness_y': ['thickness', 'fiber_thickness_y']},
        'numfibers': {'num_fibers': ['fiber', 'fiber_params', 'yarn', 'placement_params', 'num_points']},
        'plyradius': {'ply_radius': ['fiber', 'fiber_params', 'yarn', 'placement_params', 'radius']},
        'alpha': {'alpha': ['fiber', 'fiber_params', 'yarn', 'curve_params', 'dif_z']},
        'plyradiusy': {'ellipse': ['fiber', 'ellipse']},
        'yarnradius': {'yarn_radius': ['fiber', 'placement_params', 'radius']}
    }

    def __init__(self, folder_path, param_flag='alphaply'):
        assert param_flag in self.PARAM_CONFIGS, f"Invalid param_flag '{param_flag}'. Must be one of {list(self.PARAM_CONFIGS.keys())}"
        
        param_config = self.PARAM_CONFIGS[param_flag]
        self.ims_list, self.ims_params_list = read_png_yarn_folder(folder_path, param_config)
        self.dataset_size = len(self.ims_list)

    def __len__(self):
        return self.dataset_size

    def __getitem__(self, index):
        inputs = self.ims_list[index]
        
        # Random crop
        h, new_h, new_w = 2000, 1200, 584
        bottom = np.random.randint(0, h - new_h)
        top = bottom + new_h
        left = np.random.randint(8, 28)
        right = left + new_w
        inputs = inputs[bottom:top, left:right]
        
        inputs = np.transpose(inputs, (2, 1, 0))
        label = self.ims_params_list[index]

        return inputs, label, index
