# 6Dof-visual-Localization

In this work, I research methods for style transfer based on Generative Adversarial Network (GAN) and apply them to image retrieval and visual localization. I implement the ToDayGAN model, which can transfer the style of images between different illumination, weather and seasonal conditions. After researching the state-of-the-art visual localization methods on the effect of changing conditions, I apply the style transfer model to implement hierarchical localization, and use SuperPoint to export the dense local descriptors and NetVLAD to export global image-wide descriptors, finally, the SolvePnPRansac pose estimation algorithm is used to obtain a more accurate 6-DoF pose. 

The results of ToDayGAN:

![Image text](https://github.com/zhufangzheng/Images/blob/dfd115486e321e8c027b6fdcee588dd88d6d6ab2/TODAYGAN1.jpg)

![Image text](https://github.com/zhufangzheng/Images/blob/dfd115486e321e8c027b6fdcee588dd88d6d6ab2/TODAYGAN2.jpg)



The results of applying the style transfer model to implement hierarchical localization.

Aachen的结果：

![Image text](https://github.com/zhufangzheng/Images/blob/5321b5434514917d05bd38bc86348267a6ccaf44/AACHEN2.png)

RobotCar Seasons的结果：

![Image text](https://github.com/zhufangzheng/Images/blob/b5c0902e8284d95ae0f64a5a0cb1df46dae65d77/robotcar.png)
