# AI2SARShip
这个repo是我做2020年本科毕业设计的记录，我的研究课题是：高分辨率SAR影像舰船检测模型设计与优化。  
本repo于2020/03/06开源，每隔一周更新一次，直到5月底验收。 
## 2020/03/26更新  
**研究了一些模型的PR曲线绘制**  
[参考链接](https://blog.csdn.net/hongxingabc/article/details/80064574)  
FasterRCNN + VOC2007：（ mAP = 74.8 ）  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/results/Figure_2.png)  
FasterRCNN + VOC2007 + SSDD：（ mAP = 81.2 ）  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/results/Figure_1.png)  
[参考链接](https://blog.csdn.net/qq_33350808/article/details/83178002)  
[参考链接](https://blog.csdn.net/amusi1994/article/details/81564504)  
YOLOv3 + SSDD ( mAP = 72.2 )  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/results/yolov3.png)  


## 2020/03/20更新
**实现YOLOv3的训练和对SSDD图像的目标检测**  
训练：  
```
./darknet detector train cfg/voc.data cfg/yolov3-voc.cfg ./model/darknet53.conv.74 
```

实现效果  
![图片1](https://github.com/aulaywang/AI2SARShip/blob/master/yolo_sar/000089.jpg)  
![图片2](https://github.com/aulaywang/AI2SARShip/blob/master/yolo_sar/000403.jpg)  
![图片3](https://github.com/aulaywang/AI2SARShip/blob/master/yolo_sar/000641.jpg)  
![图片4](https://github.com/aulaywang/AI2SARShip/blob/master/yolo_sar/000846.jpg)  

## 2020/03/13更新  
实现YOLOv3对本地数据集的预测  
实现效果  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/predictions.jpg)  
**实现YOLO的图片批量处理导出**  
[视频地址](https://www.zhihu.com/zvideo/1221754129061982208)  
## 2020/03/11更新  
本周贡献：**实现了Faster RCNN算法在VOC2007数据集上的预测，并实现了SSDD数据集的迁移**  
参考代码：https://github.com/jwyang/faster-rcnn.pytorch/tree/pytorch-1.0
### 调试步骤
* 预装环境介绍：*Ubuntu16.04 + CUDA10.0 + cuDNN7.6.3 + anaconda3 + python3.6 + pytorch1.4.0*
* 克隆[项目](https://github.com/jwyang/faster-rcnn.pytorch/tree/pytorch-1.0)到本地
```
git clone https://github.com/jwyang/faster-rcnn.pytorch/tree/pytorch-1.0
```
* 准备VOC2007数据集，用软链接的方式链接到项目下，指令类似这样（**一定要是绝对路径**）：  
```
ln -s /path/to/VOCdevkit/ /path/to/faster-rcnn.pytorch/
```
* 准备预加载模型放在data/pretrained_models/下  
VGG16:[下载链接](https://filebox.ece.vt.edu/~jw2yang/faster-rcnn/pretrained-base-models/vgg16_caffe.pth)  
Res101:[下载链接](https://filebox.ece.vt.edu/~jw2yang/faster-rcnn/pretrained-base-models/resnet101_caffe.pth)  
* 编译  
激活虚拟环境，输入以下指令：
```
pip install -r requirements.txt
cd lib
python setup.py build develop
```

* 训练  
用vgg16训练：  
```
CUDA_VISIBLE_DEVICES=$GPU_ID python trainval_net.py \
                   --dataset pascal_voc --net vgg16 \
                   --bs $BATCH_SIZE --nw $WORKER_NUMBER \
                   --lr $LEARNING_RATE --lr_decay_step $DECAY_STEP \
                   --cuda
```
当然可以考虑简化一下：  
```
#基于VGG的模型
CUDA_VISIBLE_DEVICES=0 python trainval_net.py --dataset pascal_voc --net vgg16 --bs 1 --nw 1 --cuda
#基于Res101的模型
CUDA_VISIBLE_DEVICES=0 python trainval_net.py --dataset pascal_voc --net res101 --bs 1 --nw 1 --cuda
#基于VGG的模型训练2007+2012
CUDA_VISIBLE_DEVICES=0 python trainval_net.py --dataset pascal_voc_0712 --net vgg16 --bs 1 --nw 1 --cuda
```
* 模型评估  
```
python test_net.py --dataset pascal_voc --net vgg16 \
                   --checksession $SESSION --checkepoch $EPOCH --checkpoint $CHECKPOINT \
                   --cuda
```
当然也可以考虑简化一下：
```
#基于VGG的模型（训练7epochs）
python test_net.py --dataset pascal_voc --net vgg16 --checksession 1 --checkepoch 7 --checkpoint 10021 --cuda
#基于Res101的模型
python test_net.py --dataset pascal_voc --net res101 --checksession 1 --checkepoch 7 --checkpoint 10021 --cuda
#基于VGG的2007+2012模型（训练2epochs）
python test_net.py --dataset pascal_voc_0712 --net vgg16 --checksession 1 --checkepoch 2 --checkpoint 33101 --cuda
```
* 跑一个demo  
```
python demo.py --net vgg16 \
               --checksession $SESSION --checkepoch $EPOCH --checkpoint $CHECKPOINT \
               --cuda --load_dir path/to/model/directoy
```
比如用res101的模型来检测：  
```
python demo.py --net res101 --checksession 1 --checkepoch 7 --checkpoint 10021 --cuda --load_dir models
```
检测效果  
![kon](https://github.com/aulaywang/AI2SARShip/blob/master/kon5._det.jpg)
### 模型效果  

VOC2007   

 -- | fps | mAP
 -- | -- | -- 
 VGG+07 | 12.56 | 70.7
 Res | 11.75 | 74.8
 VGG+0712 | 12.3 | 67.4
 Res(bs4) | 11.83 | 72.1  
 
详细数据见最后的[模型效果](https://github.com/aulaywang/AI2SARShip#%E6%A8%A1%E5%9E%8B%E6%95%88%E6%9E%9C-1)  
### 模型迁移
有了在VOC上训练数据的经验我们就可以在SSDD上训练了。总体思路是这样的，把SSDD的数据集做成和VOC的一样，然后“骗”算法进行训练。  
为了做到数据集格式一致，我参考了[链接](https://www.cnblogs.com/wind-chaser/p/11359521.html)对原先的SSDD数据集进行改动。  
效果：**13.89fps/81.2mAP**  
检测效果  
![图1a](https://github.com/aulaywang/AI2SARShip/blob/master/sar_image/000199.jpg)  
![图1b](https://github.com/aulaywang/AI2SARShip/blob/master/sar_image/000199_det.jpg)  
![图2a](https://github.com/aulaywang/AI2SARShip/blob/master/sar_image/000806.jpg)  
![图2b](https://github.com/aulaywang/AI2SARShip/blob/master/sar_image/000806_det.jpg)  
![图3a](https://github.com/aulaywang/AI2SARShip/blob/master/sar_image/000018.jpg)  
![图3b](https://github.com/aulaywang/AI2SARShip/blob/master/sar_image/000018_det.jpg)  
![图4a](https://github.com/aulaywang/AI2SARShip/blob/master/sar_image/000750.jpg)  
![图4b](https://github.com/aulaywang/AI2SARShip/blob/master/sar_image/000750_det.jpg)  
![图5a](https://github.com/aulaywang/AI2SARShip/blob/master/sar_image/000224.jpg)  
![图5b](https://github.com/aulaywang/AI2SARShip/blob/master/sar_image/000224_det.jpg)  
## 2020/03/06更新
由于之前调研了AI目标检测的相关文献（如Faster RCNN、SSD、YOLO等），于是本周主要工作是完成对这些基础算法的复现。    
本周贡献：**实现了SSD算法在VOC2007数据集上的预测。**   
参考代码：https://github.com/amdegroot/ssd.pytorch  
### 调试步骤  
* 预装环境介绍：*Ubuntu16.04 + CUDA10.0 + cuDNN7.6.3 + anaconda3 + python3.6 + pytorch1.4.0*
* 克隆[项目](https://github.com/amdegroot/ssd.pytorch)到本地
```
git clone https://github.com/amdegroot/ssd.pytorch
```
* 下载COCO2014、VOC2007和2012数据集  
百度云：[COCO2014](https://pan.baidu.com/s/1eQn9492l0UHZpBWYLST4iQ )（yy52）<br>
注意只要下载test2014、train2014、val2014和annotations_trainval2014.zip就行  
[VOC2007](https://pan.baidu.com/s/1Dv2Kt7MVv-HPtY0rl_4AYw )（e9u9）  
[VOC2012](https://pan.baidu.com/s/1Kvk_AffRJANlxnnbe4SnuA )（bvw5）
在home下新建data/文件夹，分别解压数据集到data/文件夹下，文件目录如下：  
-data  
--coco  
---annotations  
---images(包含test2014、train2014和val2014)  
---coco_labels.txt  
--VOCdevkit  
---VOC2007  
---VOC2012  
* 下载[预训练模型](https://pan.baidu.com/s/1ueXlQbX3BYVek68Ag1doZQ ) （296i），复制到[项目](https://github.com/amdegroot/ssd.pytorch)下的weights/中
* 正式训练(training)  
激活虚拟环境，输入命令
```
cd ~
cd ssd.pytorch/
python train.py
```
如果不出意外这里模型就开始训练了。  
特别感谢[链接](https://blog.csdn.net/qq_30614451/article/details/100137358)和[链接](https://blog.csdn.net/qq_30614451/article/details/100137358)提供的帮助。如果你弄不明白就直接拷贝我的ssd_pytorch/吧。  
注：*由于我的pytorch是大于1.0的版本*，会报这个错误：
```
IndexError: invalid index of a 0-dim tensor. Use tensor.item()
```
**只需要把.data[0]改成.item()就可以正常运行啦！**
* 模型评估(evaluation)
```
python eval.py
```
### 模型效果
VOC2007

 -- | Average | Aeroplane | Bicycle | Bird | Boat | Bottle | Bus | Car | Cat | Chair | Cow | Diningtable | Dog | Horse | Motorbike | Person | Pottedplant | Sheep | Sofa | Train | Tvmonitor |
-- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
SSD | 77.5 | 82.1 | 85.7 | 75.5 | 69.5 | 50.2 | 84.8 | 85.8 | 87.3 | 61.4 | 82.4 | 79.1 | 85.7 | 87.1 | 84.0 | 79.0 | 50.7 | 77.7 | 78.9 | 86.2 | 76.7 |
FRCN-VGG07 | 70.7 | 74.5 | 79.1 | 68.7 | 51.3 | 53.8 | 78.4 | 85.5 | 84.1 | 48.6 | 80.5 | 63.8 | 77.8 | 83.6 | 76.0 | 77.8 | 44.5 | 72.8 | 65.5 | 73.0 | 74.0 |
FRCN-Res | 74.8 | 77.7 | 79.4 | 77.4 | 65.2 | 61.4 | 78.3 | 85.8 | 87.1 | 55.0 | 82.0 | 65.9 | 87.2 | 86.1 | 78.7 | 78.8 | 48.1 | 76.6 | 73.8 | 77.3 | 74.8 |
FRCN-VGG0712 | 67.4 | 68.2 | 74.2 | 67.1 | 47.9 | 58.5 | 74.0 | 80.2 | 78.3 | 49.3 | 72.4 | 60.9 | 77.1 | 81.7 | 73.8 | 75.8 | 34.5 | 68.0 | 63.1 | 74.3 | 68.7 |
FRCN-Res(bs4) | 72.1 | 77.9 | 77.6 | 74.7 | 57.4 | 60.6 | 82.3 | 84.3 | 85.5 | 47.4 | 81.5 | 54.8 | 83.2 | 83.3 | 76.1 | 77.4 | 48.4 | 78.3 | 71.2 | 78.4 | 62.5 |

 
