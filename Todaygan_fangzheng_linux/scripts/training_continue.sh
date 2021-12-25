python ../train.py  \
    --continue_train  --which_epoch 10  \
    --checkpoints_dir ../checkpoints \
    --dataroot ../../../code/datasets/robotcar \
    --name robotcar_night2day_20201217  \
    --n_domains 2  \
    --niter 25  --niter_decay 25  \
    --loadSize 512  --fineSize 384 \
    --gpu_ids '1,2' --gpu_parallel\
    --contexfeature