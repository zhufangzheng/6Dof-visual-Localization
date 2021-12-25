python -m torch.distributed.launch  ../train.py  \
    --dataroot ../../../code/datasets/robotcar \
    --checkpoints_dir ../checkpoints \
    --name robotcar_night2day_20201217  \
    --n_domains 2  \
    --niter 25  --niter_decay 25  \
    --loadSize 512  --fineSize 384 \
    --gpu_ids '0,1' --gpu_parallel\
    --contexfeature