#Done
import numpy as np
import time
import torch
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime
import socket
import os

from dataloader import YarnDataset
from utils import export, read_file
from network import ResnetYarn

def initialize_experiment(config_file='config.json'):
    """
    Initialize experiment configuration, directories, and logging.

    Args:
        config_file (str): Path to the configuration file. Defaults to 'config.json'.

    Returns:
        tuple: Contains configuration dictionary, training input base path, validation input base path, 
               checkpoint directory path, and timestamp string.
    """
    config = read_file(config_file)

    input_base_train = config['inputBaseTrain']
    input_base_val = config['inputBaseVal']
    output_dir = config['outputPath'] + config['paramFlag']
    checkpoint_dir = os.path.join(output_dir, 'checkpoints')

    # Create directories if they don't exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(checkpoint_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%y%m%d_%H%M%S_") + socket.gethostname()

    return config, input_base_train, input_base_val, checkpoint_dir, timestamp

def get_loss_function(param_flag):
    """
    Return the appropriate loss function and number of parameters based on the parameter flag.

    Args:
        param_flag (str): Parameter flag indicating the type of parameter.

    Returns:
        tuple: Contains the loss function and the number of parameters.
    """
    if param_flag == 'num_plies' or param_flag == 'thickness':
        return torch.nn.CrossEntropyLoss(), 2 if param_flag == 'thickness' else 5
    elif param_flag == 'flyaways':
        return torch.nn.L1Loss(reduction='mean'), 10
    else:
        return torch.nn.L1Loss(reduction='mean'), 1

def setup_device_and_model(resnet_num, num_params, freeze, device_ids):
    """
    Setup the device and model for training.

    Args:
        resnet_num (int): The ResNet model number (18, 34, 50, 101).
        num_params (int): Number of parameters for the model output.
        freeze (int): Number of ResNet blocks to freeze (-1 for no freezing).
        device_ids (list): List of device IDs for multi-GPU setup.

    Returns:
        tuple: Contains the model and the device.
    """
    model = ResnetYarn(resnet_num, num_params, freeze)
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)

    if torch.cuda.device_count() > 1:
        model = torch.nn.DataParallel(model, device_ids=device_ids)

    return model, device

def setup_dataloaders(input_base_train, input_base_val, param_flag, batch_size):
    """
    Setup training and validation data loaders.

    Args:
        input_base_train (str): Path to the training dataset.
        input_base_val (str): Path to the validation dataset.
        param_flag (str): Parameter flag indicating the type of parameter.
        batch_size (int): Batch size for the data loaders.

    Returns:
        tuple: Contains the training and validation data loaders.
    """
    train_dataset = YarnDataset(input_base_train, param_flag)
    val_dataset = YarnDataset(input_base_val, param_flag)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=True, num_workers=0)

    return train_loader, val_loader

def validate_directories(directories):
    """
    Validate that the specified directories exist.

    Args:
        directories (list): List of directory paths to validate.

    Raises:
        AssertionError: If any of the directories do not exist.
    """    
    for directory in directories:
        assert os.path.exists(directory), f"Directory '{directory}' does not exist."

def validate_parameters(resnet_num, freeze):
    """
    Validate the ResNet model number and the freeze parameter.

    Args:
        resnet_num (int): The ResNet model number (18, 34, 50, 101).
        freeze (int): Number of ResNet blocks to freeze (-1 for no freezing).

    Raises:
        AssertionError: If resnet_num or freeze values are invalid.
    """
    assert resnet_num in [18, 34, 50, 101], f"Invalid resnet_num '{resnet_num}'. Must be one of [18, 34, 50, 101]."
    assert isinstance(freeze, int) and (freeze == -1 or (0 <= freeze <= 5)), f"Invalid freeze value '{freeze}'. Must be -1 or an integer between 0 and 5."


def main():
    config, input_base_train, input_base_val, checkpoint_dir, timestamp = initialize_experiment()

    num_epochs = config['numEpochs']
    learning_rate_start = config['learningRateStart']
    batch_size = config['batchSize']
    resnet_num = config['resnetNum']
    freeze = config['freeze']
    param_flag = config['paramFlag']
    eval_interval = config['evalInterval']
    checkpoint_interval = config['checkpointInterval']
    device_ids = [0, 1, 2, 3]  # Example for multi-GPU setup

    validate_directories([input_base_train, input_base_val])
    
    validate_parameters(resnet_num, freeze)

    loss_fn, num_params = get_loss_function(param_flag)
    model, device = setup_device_and_model(resnet_num, num_params, freeze, device_ids)
    train_loader, val_loader = setup_dataloaders(input_base_train, input_base_val, param_flag, batch_size)

    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate_start, betas=(0.99, 0.9999), eps=1e-8, amsgrad=True, weight_decay=0.005)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=500)

    writer = SummaryWriter()
    global_step = 0
    initial_seed = 123
    iter_plot_interval = max(1, len(train_loader) // 10)

    print(f'len_Dataset: {len(train_loader.dataset)}')

    if param_flag == 'flyaways':
        weights = np.array([0.1, 32, 7, 20, 32, 3, 3, 10, 1086, 106]).reshape(1, num_params)
        weights = torch.from_numpy(weights).to(device, dtype=torch.float)

    for epoch in range(num_epochs):
        np.random.seed(initial_seed + epoch)
        model.train()

        time_epoch_start = time.time()
        train_losses = np.zeros(len(train_loader))

        for batch_idx, (x_batch, y_batch, _) in enumerate(train_loader):
            x_batch, y_batch = x_batch.to(device, dtype=torch.float), y_batch.to(device, dtype=torch.float)
            y_pred = model(x_batch)

            if param_flag == 'flyaways':
                y_pred *= weights
                y_batch *= weights

            loss = loss_fn(y_pred, y_batch)
            train_losses[batch_idx] = loss.item()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if global_step % iter_plot_interval == 0:
                writer.add_scalar(f'lossIter_{param_flag}', train_losses[batch_idx], global_step)
            global_step += 1

        time_epoch = time.time() - time_epoch_start
        print(f'epoch {epoch:05d} / {num_epochs:05d}, {time_epoch:9.2f} s, train loss {train_losses.mean():5.5f}')
        writer.add_scalar(f'training loss_{param_flag}', train_losses.mean(), epoch)

        if epoch % eval_interval == 0:
            model.eval()
            val_losses = np.zeros(len(val_loader))

            with torch.no_grad():
                for batch_idx, (x_val, y_val, _) in enumerate(val_loader):
                    x_val, y_val = x_val.to(device, dtype=torch.float), y_val.to(device, dtype=torch.float)
                    y_val_pred = model(x_val)

                    if param_flag == 'flyaways':
                        y_val_pred *= weights
                        y_val *= weights

                    val_loss = loss_fn(y_val_pred, y_val)
                    val_losses[batch_idx] = val_loss.item()

            print(f'epoch {epoch:05d}, val loss {val_losses.mean():5.5f}')
            writer.add_scalar(f'val loss_{param_flag}', val_losses.mean(), epoch)

            if epoch % checkpoint_interval == 0:
                export(model, checkpoint_dir, timestamp, epoch=epoch, scheduler=scheduler)

        if scheduler is not None:
            scheduler.step()

    export(model, checkpoint_dir, timestamp, epoch=epoch, label='final', scheduler=scheduler)

if __name__ == "__main__":
    main()
