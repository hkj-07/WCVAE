import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.utils.spectral_norm as spectral_norm
from Opt import Opt

"""
最终训练的半监督分类器
输入：解码器/生成器生成的数据(x,y)
输出：softmax分类结果
"""

class Classifier(nn.Module):
    def __init__(self):
        super(Classifier2, self).__init__()
        self.opt = Opt()

        def conv_block(in_channels, out_channels, bn=True):
            layers = [spectral_norm(nn.Conv2d(in_channels, out_channels, 4, stride=1))]
            if bn:
                layers.append(nn.BatchNorm2d(out_channels, 0.8))
            layers.append(nn.LeakyReLU(0.2, inplace=True))
            layers.append(spectral_norm(nn.Conv2d(out_channels, out_channels, 3, stride=1, padding=1)))
            if bn:
                layers.append(nn.BatchNorm2d(out_channels, 0.8))
            layers.append(nn.LeakyReLU(0.2, inplace=True))
            layers.append(nn.Dropout2d(0.25))
            return layers

        self.model = nn.Sequential(
            *conv_block(self.opt.img_channels+1, 64),
            *conv_block(64, 128),
            *conv_block(128, 256),
            *conv_block(256, 512)
        )

        self.output_layers = [spectral_norm(nn.Linear(16*16*512, self.opt.n_classes)), nn.]

    def forward(self, imgs):
        input1 = self.conv_blocks(imgs)
        input1 = input1.view(input1.shape[0], -1)
        output_predict = self.output_layer(input1)
        return output_predict