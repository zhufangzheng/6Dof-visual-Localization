'''python test.py --phase test --serial_test --name robotcar_2day --dataroot ./datasets --n_domains 2 --which_epoch 150 --loadSize 512
下面我用预训练的模型对ToDayGAN model用更多图片进行了测试。运行test.py 文件，
--serial_test 表示按顺序从文件夹中读取每个图像一次，--name表示预训练模型的名字，dataroot表示测试集，n_domains_2表示两个域，
150个 epoch，并且把图片缩放到512像素再载入。'''

import os
from options.test_options import TestOptions
from data.data_loader import DataLoader
from models.combogan_model import ComboGANModel
from util.visualizer import Visualizer
from util import html

opt = TestOptions().parse()
opt.nThreads = 1   # test code only supports nThreads = 1
opt.batchSize = 1  # test code only supports batchSize = 1

dataset = DataLoader(opt)
model = ComboGANModel(opt)
visualizer = Visualizer(opt)
# create website
web_dir = os.path.join(opt.results_dir, opt.name, '%s_%d' % (opt.phase, opt.which_epoch))
webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %d' % (opt.name, opt.phase, opt.which_epoch))
# store images for matrix visualization
vis_buffer = []

# test
#dataset是一个包含测试图片的数据集，enumerate是python中自带的枚举函数，可遍历的对象（如列表、字符串），enumerate将其组成一个索引序列，利用它可以同时获得索引和值。
for i, data in enumerate(dataset):
    #serial_test 表示按顺序从文件夹中读取每个图像一次
    if not opt.serial_test and i >= opt.how_many:
        break
    model.set_input(data)
    model.test()
    #visuals就是转换后的图片
    visuals = model.get_current_visuals(testing=True)
    img_path = model.get_image_paths()
    print('process image... %s' % img_path)
    #visualizer用来显示结果图片
    visualizer.save_images(webpage, visuals, img_path)

    if opt.show_matrix:
        vis_buffer.append(visuals)
        if (i+1) % opt.n_domains == 0:
            save_path = os.path.join(web_dir, 'mat_%d.png' % (i//opt.n_domains))
            visualizer.save_image_matrix(vis_buffer, save_path)
            vis_buffer.clear()

webpage.save()

