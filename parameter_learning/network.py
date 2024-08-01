import torch.nn as nn
from torchvision import models

class ResnetYarn(nn.Module):
    """
    ResnetYarn: A neural network model using pretrained ResNet as the backbone.
    
    Args:
        resnet_type (str): Type of ResNet model ('18', '34', '50', '101'). Default is '34'.
        num_params (int): Number of output parameters. Default is 1.
        freeze_blocks (int): Number of ResNet blocks to freeze. Default is -1 (no freezing).
    """

    def __init__(self, resnet_type='34', num_params=1, freeze_blocks=-1):
        super(ResnetYarn, self).__init__()

        resnet = self._get_resnet_model(resnet_type)
        self._freeze_blocks(resnet, freeze_blocks)
        
        num_features = resnet.fc.in_features
        resnet.fc = nn.Identity()

        self.resnet = resnet
        self.classifier = nn.Sequential(
            nn.Linear(num_features, num_features),
            nn.ELU(),
            nn.Linear(num_features, num_params),
        )

    def _get_resnet_model(self, resnet_type):
        """Returns the specified ResNet model."""
        resnet_models = {
            18: models.resnet18,
            34: models.resnet34,
            50: models.resnet50,
            101: models.resnet101
        }
        return resnet_models[resnet_type](pretrained=True)

    def _freeze_blocks(self, resnet, freeze_blocks):
        """Freezes the specified number of blocks in the ResNet model."""
        if freeze_blocks >= 0:
            for block_counter, block in enumerate(resnet.children()):
                if block_counter <= freeze_blocks:
                    print("Freezing block nr.", block_counter)
                    for param in block.parameters():
                        param.requires_grad = False

    def forward(self, x):
        x = self.resnet(x)
        return self.classifier(x)
