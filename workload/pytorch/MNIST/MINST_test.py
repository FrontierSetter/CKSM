import numpy as np
from struct import unpack
import torch
import torch.utils.data.dataset as Dataset
import torch.utils.data.dataloader as DataLoader
import sys
import time

def __read_image(path):
    with open(path, 'rb') as f:
        magic, num, rows, cols = unpack('>4I', f.read(16))
        print(magic)
        # print(np.fromfile(f, dtype=np.uint8))
        img = np.fromfile(f, dtype=np.uint8).reshape(num, 784)
    return img

def __read_label(path):
    with open(path, 'rb') as f:
        magic, num = unpack('>2I', f.read(8))
        lab = np.fromfile(f, dtype=np.uint8)
    return lab
    
def __normalize_image(image):
    img = image.astype(np.float32) / 255.0
    return img

def __one_hot_label(label):
    lab = np.zeros((label.size, 10))
    for i, row in enumerate(lab):
        row[label[i]] = 1
    return lab

def load_mnist(train_image_path, train_label_path, test_image_path, test_label_path, normalize=True, one_hot=True):
    '''读入MNIST数据集
    Parameters
    ----------
    normalize : 将图像的像素值正规化为0.0~1.0
    one_hot_label : 
        one_hot为True的情况下，标签作为one-hot数组返回
        one-hot数组是指[0,0,1,0,0,0,0,0,0,0]这样的数组
    Returns
    ----------
    (训练图像, 训练标签), (测试图像, 测试标签)
    '''
    image = {
        'train' : __read_image(train_image_path),
        'test'  : __read_image(test_image_path)
    }

    label = {
        'train' : __read_label(train_label_path),
        'test'  : __read_label(test_label_path)
    }
    
    if normalize:
        for key in ('train', 'test'):
            image[key] = __normalize_image(image[key])

    if one_hot:
        for key in ('train', 'test'):
            label[key] = __one_hot_label(label[key])

    return (image['train'], label['train']), (image['test'], label['test'])



 

#创建子类
class subDataset(Dataset.Dataset):
    #初始化，定义数据内容和标签
    def __init__(self, Data, Label):
        self.Data = Data
        self.Label = Label
    #返回数据集大小
    def __len__(self):
        return len(self.Data)
    #得到数据内容和标签
    def __getitem__(self, index):
        data = torch.Tensor(self.Data[index])
        label = torch.IntTensor(self.Label[index])
        return data, label
 
if __name__ == '__main__':
    numProcess = int(sys.argv[1])

    image_path = '../data/train-images.idx3-ubyte'
    label_path = '../data/train-labels.idx1-ubyte'
    # image_path = './train-images.idx3-ubyte'
    # label_path = './train-labels.idx1-ubyte'

    (image1, label1), (image2, label2) = load_mnist(image_path, label_path, image_path, label_path)

    # Data = np.asarray([[1, 2], [3, 4],[5, 6], [7, 8]])
    # Label = np.asarray([[0], [1], [0], [2]])
    Data = np.array(image1)
    Label = np.array(label1)

    dataset = subDataset(Data, Label)
    # print(dataset)
    # print('dataset大小为：', dataset.__len__())
    # print(dataset.__getitem__(0))
    # print(dataset[0])
 
    # #创建DataLoader迭代器
    dataloader = DataLoader.DataLoader(dataset,batch_size= 2, shuffle = False, num_workers= numProcess)
    print (int(time.time()))
    while True:
        for i, item in enumerate(dataloader):
            # print('i:', i)
            data, label = item
            # print('data:', data)
            # print('label:', label)