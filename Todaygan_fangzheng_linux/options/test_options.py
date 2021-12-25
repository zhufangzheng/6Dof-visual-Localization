# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 12:04:23 2020

@author: 12399
"""

from .base_options import BaseOptions


class TestOptions(BaseOptions):
    def initialize(self):
        BaseOptions.initialize(self)
        self.isTrain = False

        self.parser.add_argument('--results_dir', type=str, default='./results/', help='saves results here.')
        #图片的纵横比
        self.parser.add_argument('--aspect_ratio', type=float, default=1.0, help='aspect ratio of result images')
        #判断载入哪一个epoch
        self.parser.add_argument('--which_epoch', required=True, type=int, help='which epoch to load for inference?')
        self.parser.add_argument('--phase', type=str, default='test', help='train, val, test, etc (determines name of folder to load from)')

        self.parser.add_argument('--how_many', type=int, default=50, help='how many test images to run (if serial_test not enabled)')
        #按顺序从文件夹中读取每个图像一次
        #store_true表示只要运行时该变量有传参就将该变量设为True。
        self.parser.add_argument('--serial_test', action='store_true', help='read each image once from folders in sequential order')

        self.parser.add_argument('--autoencode', action='store_true', help='translate images back into its own domain')
        self.parser.add_argument('--reconstruct', action='store_true', help='do reconstructions of images during testing')
        #以矩阵格式可视化图像
        self.parser.add_argument('--show_matrix', action='store_true', help='visualize images in a matrix format as well')
