python ../test.py  \
    --phase test  --which_epoch 25  \
    --how_many 50  \
    --serial_test  \
    --dataroot ../../../code/datasets/robotcar \
    --checkpoints_dir ../checkpoints \
    --results_dir ../results/ \
    --name robotcar_night2day_20201217 \
    --n_domains 2  \
    --loadSize 512 \
    --gpu_ids '1,2' --gpu_parallel \
    --contexfeature