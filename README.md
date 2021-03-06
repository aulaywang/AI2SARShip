# AI2SARShip
这个repo是我做2020年本科毕业设计的记录，我的研究课题是：高分辨率SAR影像舰船检测模型设计与优化。  
本repo于2020/03/06开源，每隔一周更新一次，直到5月底验收。  
**学校通知了，4月15到20号之间有中期答辩。**  
## 2020/04/04更新  
按照下图对darknet53进行fine-tune，主要表现在：  
1.将stage3和stage4的res层从8缩减到6  
2.stage4到stage5的下采样取消，改为维持采样，这样做的目的是增强模型对小目标的检测能力。  
修改过后的yolov3-voc.cfg见[链接](https://github.com/aulaywang/AI2SARShip/blob/master/cfg/yolov3-voc_sar3.cfg)  
检测效果：  
检测准确率（mAP）从92.4提高到95.0。  
pr曲线:  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/pr_95.png)  
loss曲线：  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/visualization/avg_loss_95.png)  
上对比图（左右分别为92.4和95.0）：  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/compare/c11.png)  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/compare/c12.png)  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/compare/c13.png)  
## 2020/04/03更新  
目前的进度总体来说还是围绕YOLOv3架构进行改进，放弃改darknet53了，准备尝试改一改后面的检测算法，看看能不能有突破。  
先回顾一下整套YOLOv3的SAR目标检测的流程。  
准备工作：voc.data_sar（voc.data改） train时设置valid为valid，test时valid改成test文件的路径（这几个文件都是要有路径的）  
yolov3-voc_sar.cfg(yolov3-voc.cfg改)  注意test和train要分别设置一下batch和subdivision  
darknet53.conv.73预训练模型  
把SSDD的1160张图片按8：1：1的比例随机给训练集、验证集和测试集（代码）  
训练：  
```
./darknet detector train cfg/voc.data_sar cfg/yolov3-voc_sar.cfg darknet53.conv.74 | tee visualization/train_yolov3.log 
```
后面的部分可以将训练时产生的文件保存下来方便绘制图像，这时训练产生的所有模型都存到darknet/backup文件夹下了。原始的文件是前1000次每隔100次保存，之后保存就到10000次了，我取消了这个设定（在detector.c下修改，重编译），训练到2000次时avgloss降低到0.3-0.4，我中止训练，此时backup里有21个模型文件。  
测试：（记得把yolov3-voc_sar.cfg改了）
```
./darknet detector valid cfg/voc.data cfg/yolov3-voc_sar.cfg backup/yolov3-voc_2000.weights -out
```
后面的 -out可以在darknet/results文件夹下生成一个ship.txt文件，代表检测结果。  
画precision-recall图：  
```
在python2的环境下
python compute_mAP.py 
```
注意需要voc_eval.py这个文件作为头文件，同时把darknet下原来的annots.pkl删除或者重命名。  
这样就可以画图了，同时会返回precision和recall各自的值。  
mAP = 92.4(YOLO流皮)  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/sar_811_92.png)
画loss图：  
进入visualization文件夹，此时里面应该有一个log文件，准备三个程序：extract_log.py，train_iou_visualization.py和train_loss_visualization.py  
如果要画loss图就运行1和3两个文件。  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/visualization/avg_loss.png)  
图片批量可视化（需要对detector.c修改并重编译[参考链接](https://blog.csdn.net/mieleizhi0522/article/details/79989754?depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-1&utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-1)）：  
```
./darknet detector test cfg/voc.data_sar cfg/yolov3-voc_sar2.cfg backup/yolov3-voc_sar2_2000.weights
Enter path:/home/aulaywang/darknet/2007_test.txt
```
运行完毕后图片会保存在data/out下  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/compare/c1.png)
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/compare/c2.png)
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/compare/c3.png)
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/compare/c4.png)
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/compare/c5.png)
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/compare/c6.png)
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/compare/c7.png)

更新了一些有趣的代码(others文件夹下)：  
flv2jpg.py:视频转图片输出  
voc_labe.py:把voc的xml格式转化成yolo格式(5参数格式)，会在执行完后生成labels文件夹  
test.py:数据集划分程序  

## 2020/03/26更新  
**研究了一些模型的PR曲线绘制**  
[参考链接](https://blog.csdn.net/hongxingabc/article/details/80064574)  
FasterRCNN + VOC2007：（ mAP = 74.8 ）  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/results/Figure_2.png)  
FasterRCNN + Res101 + SSDD：（ mAP = 81.2 ）  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/results/Figure_1.png)  
[参考链接](https://blog.csdn.net/qq_33350808/article/details/83178002)  
[参考链接](https://blog.csdn.net/amusi1994/article/details/81564504)  
YOLOv3 + SSDD ( mAP = 72.2 )  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/results/yolov3.png)  

**研究了一些模型的loss曲线绘制**  
原理：基于tensorboard  
一个槽点是pytorch没找到合适的输出方案，要通过tf输出2333  
```
#基于Res101的模型
CUDA_VISIBLE_DEVICES=0 python trainval_net.py --dataset pascal_voc --net res101 --bs 1 --nw 1 --cuda --use_tfb
tensorboard --logdir=/home/aulaywang/FRCN/AISAR/logs/logs_s_1/losses
```
FasterRCNN + Res101 + SSDD 的loss曲线：（ mAP = 81.2 ）  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/loss_pic/logs_s_1_losses%20(1).svg)  

下午更新：用python重写绘图代码  
FasterRCNN + Res101 + SSDD 的loss曲线：（ mAP = 81.2 ）  
![图片](https://github.com/aulaywang/AI2SARShip/blob/master/loss_pic/loss.png)  
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
[图片](https://github.com/aulaywang/AI2SARShip/blob/master/predictions.jpg)  
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
[kon](https://github.com/aulaywang/AI2SARShip/blob/master/kon5._det.jpg)
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
为了做到数据集格式一致，我参考了[链接](https://www.cnblogs.com/wind-chaser/p/11359521.html)对原先的SSDD数据集进行改动，此时数据集名字为 VOCdevkit2007。  
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
FRCN-VOC07 | 70.7 | 74.5 | 79.1 | 68.7 | 51.3 | 53.8 | 78.4 | 85.5 | 84.1 | 48.6 | 80.5 | 63.8 | 77.8 | 83.6 | 76.0 | 77.8 | 44.5 | 72.8 | 65.5 | 73.0 | 74.0 |
FRCN-Res | 74.8 | 77.7 | 79.4 | 77.4 | 65.2 | 61.4 | 78.3 | 85.8 | 87.1 | 55.0 | 82.0 | 65.9 | 87.2 | 86.1 | 78.7 | 78.8 | 48.1 | 76.6 | 73.8 | 77.3 | 74.8 |
FRCN-VOC0712 | 67.4 | 68.2 | 74.2 | 67.1 | 47.9 | 58.5 | 74.0 | 80.2 | 78.3 | 49.3 | 72.4 | 60.9 | 77.1 | 81.7 | 73.8 | 75.8 | 34.5 | 68.0 | 63.1 | 74.3 | 68.7 |
FRCN-Res(bs4) | 72.1 | 77.9 | 77.6 | 74.7 | 57.4 | 60.6 | 82.3 | 84.3 | 85.5 | 47.4 | 81.5 | 54.8 | 83.2 | 83.3 | 76.1 | 77.4 | 48.4 | 78.3 | 71.2 | 78.4 | 62.5 |

 
