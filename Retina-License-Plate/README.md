# Retina-License-Plate

Use [RetinaFace](https://github.com/biubug6/Pytorch_Retinaface) architecture for License Plate Detection

## Prepare

### Data

Download data from [here](https://drive.google.com/file/d/1UxGLrZlYyl5ta9sBJzS9cfnlOU7LfFP-/view?usp=sharing) and place in `./data/` folder. 

Or use custom data with form

```Shell
  ./data/licenseplate/
    train/
      images/
      label.txt
    val/
      images/
      label.txt
```
In `./data/licenseplate/train/images/label.txt`

```Shell
# 10148.jpg
158 157 86 28 158.12 163.300032 0.0 244.65317600000003 157.006722 0.0 242.29317600000002 179.819895 0.0 158.906824 185.32661700000003 0.0 1.0
# 10149.jpg
232 129 81 22 232.85317600000002 131.046591 0.0 313.88 129.473415 0.0 312.306824 150.713412 0.0 232.066824 152.28658800000002 0.0 1.0
...
```

First 4 numbers is location of box `(x_corner, y_corner, h, w)`. 

Each 3 following numbers is `(x_landmark, y_landmark, conf)` with 
- `conf = 0.0` if visible landmark
- `conf = -1.0` if missing landmark
- `conf = 1.0` if non-visible landmark (sunglasses or something)

And the last number is the `conf_label` in `(0.0, 1.0)`

In `./data/licenseplate/val/images/label.txt` only have image paths.

```Shell
/plate_79_croped_1.jpg
/plate_7_croped_1.jpg
/plate_82_croped_1.jpg
...
```

### Pretrain

If you want to train from checkpoint, download from [here](https://drive.google.com/file/d/1JB19a-giVibITFiGYNmfn-aZMo5FE3m7/view?usp=sharing) and put in `./weights/` folder.

## Training

Before training, you can check network configuration (e.g. batch_size, min_sizes and steps etc..) in `./data/config.py` and `./train.py`

Training with

``` Shell
CUDA_VISIBLE_DEVICES=0,1,2,3 python train.py --network resnet18 --resume_net [checkpoint.pth]
```

## Evaluation

``` Shell
python test.py --trained_model [checkpoint.pth] --network resnet50 --save_image
```

More options check `test.py`
