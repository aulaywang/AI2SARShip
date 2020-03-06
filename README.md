# AI2SARShip
这个repo是我做2020年本科毕业设计的记录，我的研究课题是：高分辨率SAR影像舰船检测模型设计与优化。  
本repo于2020/03/06开源，每隔一周更新一次，直到5月底验收。  
## 2020/03/06进度
由于之前调研了AI目标检测的相关文献（如Faster RCNN、SSD、YOLO等），于是本周主要工作是完成对这些基础算法的复现。    
本周贡献：**实现了SSD算法在VOC2007数据集上的预测。**   
参考代码：https://github.com/amdegroot/ssd.pytorch  
### 调试步骤：  
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

 Average | Aeroplane | Bicycle | Bird | Boat | Bottle | Bus | Car | Cat | Chair | Cow | Diningtable | Dog | Horse | Motorbike | Person | Pottedplant | Sheep | Sofa | Train | Tvmonitor |
-- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
77.5 | 82.1 | 85.7 | 75.5 | 69.5 | 50.2 | 84.8 | 85.8 | 87.3 | 61.4 | 82.4 | 79.1 | 85.7 | 87.1 | 84.0 | 79.0 | 50.7 | 77.7 | 78.9 | 86.2 | 76.7 |

 
