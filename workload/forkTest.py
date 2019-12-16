import numpy as np
from struct import unpack
import torch
import torch.utils.data.dataset as Dataset
import torch.utils.data.dataloader as DataLoader
import sys
 
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
    pageNum = int(sys.argv[2])
    
    dataList = []
    labelList = []

    for i in range(pageNum*1024):
        dataList.append([666, 666])
        labelList.append([666])

    # Data = np.asarray([[1, 2], [3, 4],[5, 6], [7, 8]])
    # Label = np.asarray([[0], [1], [0], [2]])
    # print(dataList)
    Data = np.array(dataList)
    Label = np.array(labelList)

    dataset = subDataset(Data, Label)
    print(dataset)
    print('dataset大小为：', dataset.__len__())
    print(dataset.__getitem__(0))
    print(dataset[0])
 
    #创建DataLoader迭代器
    dataloader = DataLoader.DataLoader(dataset,batch_size= 2, shuffle = False, num_workers= numProcess)
    while True:
        for i, item in enumerate(dataloader):
            # print('i:', i)
            data, label = item
            print('data:', data)
            print('label:', label)