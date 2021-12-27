
# HF-Net: Robust Hierarchical Localization at Large Scale 
![Image text](https://github.com/zhufangzheng/Images/blob/3b6f88f1a38d86afc04386c45cdf00edc4256568/teaser.jpg)


# 步骤0：Setup
1.1先执行make install，生成编译后的文件DATA_PATH和EXPER_PATH
如：
```bash
/home/guohao/fangzheng/hfnet_local_feature_evaluation/DATA_PATH/
/home/guohao/fangzheng/hfnet_local_feature_evaluation/EXPER_PATH/
```

# 步骤1： 数据准备



1.2 NetVLAD预训练权重，存放在编译hfnet后生成的$DATA_PATH/weights/路径下

1.3 Aachen Day-Night和RobotCar Seasons数据下载，存放在编译hfnet后生成的$DATA_PATH/路径下

1.4 基于superpoint生成的aachen三维点云场景

1.5 aachen和robotcar数据对应的每张图像相机内参文件

Aachen Day-Night dataset该数据集目录结构如下：存放在编译HF-Net时设置的DATA_PATH下
```
aachen/
├── aachen.db
├── day_time_queries_with_intrinsics.txt
├── night_time_queries_with_intrinsics.txt
├── databases/
├── images_upright/
│   ├── db/
│   │   └── ...
│   └── query/
│       └── ...
└── models/
    └── hfnet_model/
        ├── cameras.bin
        ├── images.bin
        └── points3D.bin
```
RobotCar Seasons该数据集目录结构如下：存放在编译HF-Net时设置的DATA_PATH下
```
robotcar/
├── overcast-reference.db
├── query.db
├── images/
│   ├── overcast-reference/
│   ├── sun/
│   ├── dusk/
│   ├── night/
│   └── night-rain/
├── intrinsics/
│   ├── left_intrinsics.txt
│   ├── rear_intrinsics.txt
│   └── right_intrinsics.txt
├── queries/
│   ├── dusk_queries_with_intrinsics.txt
│   ├── night_queries_with_intrinsics.txt
│   ├── night-rain_queries_with_intrinsics.txt
│   └── sun_queries_with_intrinsics.txt
└── models/
    └── hfnet_model/
        ├── cameras.bin
        ├── images.bin
        └── points3D.bin
```
下载及具体要求见：
#### Required assets

Download the datasets as indicated in the [dataset documentation](doc/datasets.md). SfM models of Aachen, RobotCar, CMU, and Extended CMU, built SuperPoint and usable with HF-Net, are provided [here](https://projects.asl.ethz.ch/datasets/doku.php?id=cvpr2019hfnet). Download and unpack the HF-Net weights in `$EXPER_PATH/hfnet/`. To localize with NV+SP, download the network weights of [NetVLAD](http://rpg.ifi.uzh.ch/datasets/netvlad/vd16_pitts30k_conv5_3_vlad_preL2_intra_white.zip) and [SuperPoint](https://github.com/MagicLeapResearch/SuperPointPretrainedNetwork/blob/master/superpoint_v1.pth) and put them in `$DATA_PATH/weights/`.
	

# 步骤2： 执行特征提取
## 步骤2.1：基于NetVLAD生成aachen所有图像的global descriptors
aachen：
```bash
CUDA_VISIBLE_DEVICES=3 python3 hfnet/export_predictions.py hfnet/configs/netvlad_export_aachen.yaml netvlad/aachen --keys global_descriptor
```
robotcar:
```robotcar
CUDA_VISIBLE_DEVICES=3 python3 hfnet/export_predictions.py hfnet/configs/netvlad_export_robotcar.yaml netvlad/robotcar --keys global_descriptor
```
// [需要修改netvlad_export_robotcar.yaml中的内容]
## 步骤2.2 对底库图像的superpoint特征提取
（成功）aachen：
```
CUDA_VISIBLE_DEVICES=0 python3 hfnet/export_predictions.py hfnet/configs/superpoint_export_aachen_db.yaml superpoint/aachen --keys keypoints,scores,local_descriptor_map
#对查询图像的superpoint特征提取
CUDA_VISIBLE_DEVICES=0 python3 hfnet/export_predictions.py hfnet/configs/superpoint_export_aachen_queries.yaml superpoint/aachen --keys keypoints,scores,local_descriptor_map
```
robotcar：
```
（完成）CUDA_VISIBLE_DEVICES=4 python3 hfnet/export_predictions.py hfnet/configs/superpoint_export_robotcar_db.yaml superpoint/robotcar --keys keypoints,scores,local_descriptor_map
#对查询图像的superpoint特征提取
（完成）CUDA_VISIBLE_DEVICES=3 python3 hfnet/export_predictions.py hfnet/configs/superpoint_export_robotcar_queries.yaml superpoint/robotcar --keys keypoints,scores,local_descriptor_map
```
[需要修改superpoint_export_robotcar_queries.yaml中的内容]

## 步骤2.3 对底库图像的hfnet特征提取
python3 hfnet/export_predictions.py hfnet/configs/hfnet_export_aachen_db.yaml hfnet/aachen --keys keypoints,scores,local_descriptor_map
#对查询图像的hfnet特征提取
python3 hfnet/export_predictions.py hfnet/configs/hfnet_export_aachen_queries.yaml hfnet/aachen --keys keypoints,scores,local_descriptor_map

# 步骤3： 基于NetVLAD及superpoint构建的sfm场景模型的查询图像位姿解算
For Aachen:
```
CUDA_VISIBLE_DEVICES=0 python3 hfnet/evaluate_aachen.py /home/guohao/fangzheng/hfnet_local_feature_evaluation/DATA_PATH/aachen/superpoint_sfm/ night1 --local_method superpoint --global_method netvlad --build_db --queries night_time --export_poses
（可用）CUDA_VISIBLE_DEVICES=4 python3 hfnet/evaluate_aachen.py /home/guohao/fangzheng/hfnet_local_feature_evaluation/DATA_PATH/aachen/superpoint_sfm/ night --local_method superpoint --global_method netvlad --build_db --queries night_time --export_poses
```
For RobotCar:
```
//night2day
CUDA_VISIBLE_DEVICES=3 python3 hfnet/evaluate_robotcar.py /home/guohao/fangzheng/hfnet_local_feature_evaluation/DATA_PATH/robotcar/superpoint_sfm/ night2day --local_method superpoint --global_method netvlad --build_db --queries night2day --export_poses
//night-rain2day:
CUDA_VISIBLE_DEVICES=3 python3 hfnet/evaluate_robotcar.py /home/guohao/fangzheng/hfnet_local_feature_evaluation/DATA_PATH/robotcar/superpoint_sfm/ night-rain2day --local_method superpoint --global_method netvlad --build_db --queries night-rain2day --export_poses
```

# 原作者


<p align="center">
  <b>
    ➡️ For state-of-the-art visual localization and SfM, checkout our new toolbox hloc: </br><a href="https://github.com/cvg/Hierarchical-Localization/">cvg/Hierarchical-Localization</a> 🔥
  </b>
</p>


This repository accompanies our CVPR 2019 paper *[From Coarse to Fine: Robust Hierarchical Localization at Large Scale](https://arxiv.org/abs/1812.03506)*. We introduce a 6-DoF visual localization method that is accurate, scalable, and efficient, using HF-Net, a monolithic deep neural network for descriptor extraction. The proposed solution achieves state-of-the-art accuracy on several large-scale public benchmarks while running in real-time.

The proposed approach __won the visual localization challenge__ of the [CVPR 2019 workshop on Long-Term Visual Localization](https://sites.google.com/view/ltvl2019/home) using this codebase. We also provide [trained weights for HF-Net and reconstructed SfM 3D models](https://projects.asl.ethz.ch/datasets/doku.php?id=cvpr2019hfnet).

<p align="center">
  <img src="doc/assets/teaser.jpg" width="80%"/>
  <br /><em>Our method is significantly more robust, accurate, and scalable than standard approaches based on direct matching.</em>
</p>

##

This code allows to:
- Perform state-of-the-art 6-DoF hierarchical localization using a flexible Python pipeline
- Train HF-Net with multi-task distillation in TensorFlow
- Evaluate feature detectors and descriptors on standard benchmarks
- Build Structure-from-Motion models based on state-of-the-art learned features

## Setup

Python 3.6 is required. It is advised to run the following  command within a virtual environment. By default, TensorFlow 1.12 GPU will be installed. You will be prompted to provide the path to a data folder (subsequently referred as `$DATA_PATH`) containing the datasets and pre-trained models and to an experiment folder (`$EXPER_PATH`) containing the trained models, training and evaluation logs, and CNN predictions. Create them wherever you wish and make sure to provide absolute paths. PyTorch 0.4.1 is also required to run the original SuperPoint and perform GPU-accelerated feature matching.
```bash
make install  # install Python requirements, setup paths
```

Refer to our [dataset documentation](doc/datasets.md) for an overview of the supported datasets and their expected directory structure.

## Demo

We provide a __minimal example of the inference and localization with HF-Net__ in [`demo.ipynb`](demo.ipynb). Download the trained model [here](https://projects.asl.ethz.ch/datasets/doku.php?id=cvpr2019hfnet) and unpack it in `$EXPER_PATH/saved_models/`.

<p align="center">
  <img src="doc/assets/hfnet.jpg" width="70%"/>
  <br /><em>HF-Net simultaneously computes global descriptors and local features with an efficient architecture.</em>
</p>

## 6-DoF Localization

<p align="center">
  <img src="doc/assets/pipeline.jpg" width="70%"/>
</p>

We provide code to perform and evaluate our hierarchical localization on the three challenging benchmark datasets of [Sattler et al](https://arxiv.org/abs/1707.09092): Aachen Day-Night, RobotCar Seasons, and CMU Seasons.

#### Required assets

Download the datasets as indicated in the [dataset documentation](doc/datasets.md). SfM models of Aachen, RobotCar, CMU, and Extended CMU, built SuperPoint and usable with HF-Net, are provided [here](https://projects.asl.ethz.ch/datasets/doku.php?id=cvpr2019hfnet). Download and unpack the HF-Net weights in `$EXPER_PATH/hfnet/`. To localize with NV+SP, download the network weights of [NetVLAD](http://rpg.ifi.uzh.ch/datasets/netvlad/vd16_pitts30k_conv5_3_vlad_preL2_intra_white.zip) and [SuperPoint](https://github.com/MagicLeapResearch/SuperPointPretrainedNetwork/blob/master/superpoint_v1.pth) and put them in `$DATA_PATH/weights/`.

#### Exporting the predictions

We first export the local features and global descriptors for all database and query images as `.npz` files. For the sake of flexibility, local descriptors are exported as dense maps for database images, but as sparse samples for query images.

For HF-Net or SuperPoint:
```bash
python3 hfnet/export_predictions.py \
	hfnet/configs/[hfnet|superpoint]_export_[aachen|cmu|robotcar]_db.yaml \
	[superpoint/][aachen|cmu|robotcar] \
	[--exper_name hfnet] \ # for HF-Net only
	--keys keypoints,scores,local_descriptor_map[,global_descriptor]
python3 hfnet/export_predictions.py \
	hfnet/configs/[hfnet|superpoint]_export_[aachen|cmu|robotcar]_queries.yaml \
	[superpoint/][aachen|cmu|robotcar] \
	[--exper_name hfnet] \ # for HF-Net only
	--keys keypoints,scores,local_descriptors[,global_descriptor]
```

For NetVLAD:
```bash
python3 hfnet/export_predictions.py \
	hfnet/configs/netvlad_export_[aachen|cmu|robotcar].yaml \
	netvlad/[aachen|cmu|robotcar] \
	--keys global_descriptor
```

#### Localization

For Aachen:
```bash
python3 hfnet/evaluate_aachen.py \
	<sfm_model_name_or_path> \
	<eval_name>_[night|day] \
	--local_method [hfnet|superpoint|sift] \
	--global_method [hfnet|netvlad] \
	--build_db \
	--queries [night_time|day_time] \
	--export_poses
```

For RobotCar:
```bash
python3 hfnet/evaluate_robotcar.py \
	<sfm_model_name_or_path> \
	<eval_name> \
	--local_method [hfnet|superpoint|sift] \
	--global_method [hfnet|netvlad] \
	--build_db \
	--queries [dusk|sun|night|night-rain] \
	--export_poses
```

For CMU:
```bash
python3 hfnet/evaluate_cmu.py \
	<sfm_model_name_or_path> \
	<eval_name> \
	--local_method [hfnet|superpoint|sift] \
	--global_method [hfnet|netvlad] \
	--build_db \
	--slice [2|3|4|5|6|7|8|9|10|17] \
	--export_poses
```

The localization parameters can be adjusted in `hfnet/evaluate_[aachen|robotcar|cmu].py`. The evaluation logs and estimated poses are written to `$EXPER_PATH/eval/[aachen|robotcar|cmu]/<eval_name>*`. Of particular interest are the PnP+RANSAC success rate, the average number of inliers per query, and the average inlier ratio.

#### Visualization

Successful and failed queries can be visualized in `notebooks/visualize_localization_[aachen|robotcar|cmu].ipynb`.

## Training with multi-task distillation

Instructions to train HF-Net are provided in the [training documentation](doc/training.md).

## Evaluation of local features

Instructions to evaluate feature detectors and descriptors on the HPatches and SfM datasets are provided in the [local evaluation documentation](doc/local_evaluation.md).

## Building new SfM models

Instructions and scripts to build SfM models using [COLMAP](https://colmap.github.io/) for any learned features are provided in `colmap-helpers`.

## Citation

Please consider citing the corresponding publication if you use this work in an academic context:
```
@inproceedings{sarlin2019coarse,
  title={From Coarse to Fine: Robust Hierarchical Localization at Large Scale},
  author={Sarlin, Paul-Edouard and Cadena, Cesar and Siegwart, Roland and Dymczyk, Marcin},
  booktitle={CVPR},
  year={2019}
}
```
