from torch.utils.data import Dataset
import numpy as np

from util.data_util import DataUtil


class DatasetUtil(Dataset):
    def __init__(self, conf):
        self.data_util = DataUtil(conf)
        self.input_list, self.target_list, self.intent_list = self.data_util.get_train_data()

    def __getitem__(self, index):
        return np.array(self.input_list[index]), np.array(self.target_list[index]), np.array(self.intent_list[index])

    def __len__(self):
        return len(self.input_list)
