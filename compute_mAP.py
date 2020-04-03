# using python 2.x
from voc_eval import voc_eval
#import _pickle as cPickle
import matplotlib.pyplot as plt
rec,prec,ap = voc_eval('/home/aulaywang/darknet/results/ship.txt', '/home/aulaywang/darknet/VOCdevkit/Annotations/{}.xml', '/home/aulaywang/darknet/VOCdevkit/ImageSets/Main/test.txt', 'ship', '.')



plt.figure()
plt.xlabel('recall')
plt.ylabel('precision')
plt.title('Precision-Recall')
plt.plot(rec,prec,label='mAP = {:.4f}'''.format(ap))
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.legend(loc="lower left")
plt.grid(True)
plt.show()
print('rec',sum(rec)/len(rec))
print('prec',sum(prec)/len(prec))
print('ap',ap)

