import os
import glob
import torch
import imageio
import numpy as np
from network import ResnetYarn

def predict_params(num_params, model_file, image_file, resnet_num=18):
    """
    Predicts parameters using a pretrained ResNet model on a given image.

    Args:
        num_params (int): Number of output parameters.
        model_file (str): Path to the model checkpoint file.
        image_file (str): Path to the image file.
        resnet_num (str): Type of ResNet model. Default is '18'.

    Returns:
        np.ndarray: Predicted parameters.
    """
    # Load model
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    model = ResnetYarn(resnet_num, num_params, -1)
    model = torch.nn.DataParallel(model)
    dict_import = torch.load(model_file)
    model.load_state_dict(dict_import['state_dict'])
    model = model.to(device)
    model.eval()

    # Load image
    im = imageio.imread(image_file)
    if im.shape[2] > 3:
        im = im[:, :, :3]

    img = np.array(im) / 255.0
    img = np.transpose(img, (2, 1, 0))
    img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2])
    xs = torch.Tensor(img).to(device)

    with torch.no_grad():
        prediction = model(xs)
        prediction_np = prediction.cpu().numpy()

    return prediction_np

def main():
    """
    Main function to predict parameters for multiple images and models.
    """
    dir_images = "../data/Test_yarns/"
    model_params = [
        ('thickness', 2, 'models/thickness_resnet18.pth', 18),
        ('numfibers', 1, 'models/numfibers_resnet18.pth', 18),
        ('plyradius', 1, 'models/plyradius_resnet18.pth', 18),
        ('alpha', 1, 'models/alpha_resnet18.pth', 18),
        ('numplies', 5, 'models/numplies_resnet34.pth', 34),
        ('yarnradius', 1, 'models/yarnradius_resnet18.pth', 18),
        ('alphaply', 1, 'models/alphaply_resnet34.pth', 34),
        ('ellipse', 1, 'models/plyradiusy_resnet18.pth', 18),
        ('flyaways', 10, 'models/flyaways_resnet18.pth', 18)
    ]

    fnames_png = glob.glob(os.path.join(dir_images, '*.png'))
    fnames_png.sort()
    plyradius = None

    for image_file in fnames_png:
        print(image_file)

        for param_name, num_params, model_file, resnet_num in model_params:
            print(param_name)
            temp = predict_params(num_params, model_file, image_file, resnet_num)
            #print(temp)
            if param_name == 'thickness':
                temp = np.argmax(temp) + 1
               # print(temp)
            elif param_name == 'numplies':
                temp = np.argmax(temp) + 2
                #print(temp)
            elif param_name == 'plyradius':
                plyradius = temp
            elif param_name == 'ellipse':
                if plyradius is not None:
                    temp = temp / plyradius
                else:
                    temp = "plyradius not calculated yet"
            elif param_name == 'flyaways':
                temp = temp.flatten()
                print(f'amount: {temp[0]}')
                print(f'loop_prob: {temp[1]}')
                print(f'hair_length_mean: {temp[2]}')
                print(f'hair_angle: {temp[3]}')
                print(f'hair_squeeze: {temp[4]}')
                print(f'loop_length_mean: {temp[5]}')
                print(f'loop_distance_mean: {temp[6]}')
                print(f'loop_distance_std: {temp[7]}')
                print(f'jitter_xy: {temp[8]}')
                print(f'migration: {temp[9]}')
            print(temp)

if __name__ == "__main__":
    main()
