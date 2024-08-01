import json
import os
import torch

def read_file(filepath):
    """
    Reads a JSON file and returns the data.
    
    Args:
        filepath (str): The path to the JSON file.
    
    Returns:
        dict: The data read from the JSON file.
    """
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
    return data

def export(model, checkpoint_dir, timestamp, optimizer=None, epoch=-1, label='', scheduler=None):
    """
    Exports the model state and optionally the optimizer and scheduler states to a file.
    
    Args:
        model (torch.nn.Module): The model to save.
        checkpoint_dir (str): Directory to save the checkpoint file.
        timestamp (str): Timestamp string to include in the filename.
        optimizer (torch.optim.Optimizer, optional): The optimizer to save. Default is None.
        epoch (int, optional): The current epoch number to include in the filename. Default is -1.
        label (str, optional): A label to include in the filename. Default is ''.
        scheduler (torch.optim.lr_scheduler._LRScheduler, optional): The scheduler to save. Default is None.
    """
    export_dict = {'state_dict': model.state_dict()}

    if scheduler is not None:
        export_dict['scheduler'] = scheduler.state_dict()
    
    if optimizer is not None:
        export_dict['optimizer'] = optimizer.state_dict()

    if label:
        label += '_'
    
    filename = os.path.join(checkpoint_dir, f'{timestamp}_epoch{epoch:06d}_{label}checkpoint.pth')
    torch.save(export_dict, filename)
