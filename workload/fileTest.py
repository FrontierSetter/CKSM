import numpy as np
from struct import unpack
import torch
import torch.utils.data.dataset as Dataset
import torch.utils.data.dataloader as DataLoader
import sys

#创建子类
class subDataset(Dataset.Dataset):
    #初始化，定义数据内容和标签
    def __init__(self, Data):
        self.Data = Data
    #返回数据集大小
    def __len__(self):
        return len(self.Data)
    #得到数据内容和标签
    def __getitem__(self, index):
        data = torch.Tensor(self.Data[index])
        return data
 
if __name__ == '__main__':
    numProcess = int(sys.argv[1])

    curFile = open('./dataFile', 'rb')
    dataList = np.fromfile(curFile, dtype=np.uint8).reshape(1024*1024, 4)
    
    # print(dataList)
    Data = np.array(dataList)
    # Label = np.array(dataList)

    dataset = subDataset(Data)
    print(dataset)
    print('dataset大小为：', dataset.__len__())
    print(dataset.__getitem__(0))
    print(dataset[0])
 
    #创建DataLoader迭代器
    dataloader = DataLoader.DataLoader(dataset,batch_size= 2, shuffle = False, num_workers= numProcess)
    while True:
        for i, item in enumerate(dataloader):
            print('i:', i)
            data = item
            print('data:', data)
