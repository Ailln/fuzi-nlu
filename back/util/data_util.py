from torch.utils.data import Dataset

from util.convert_util import ConvertUtil


class DataUtil(Dataset):
    def __init__(self, config):
        self.run_type = config["run_type"]
        self.dataset_size = config["dataset_size"]

        self.convert_util = ConvertUtil(config)
        self.convert_util.json2iob()

        if self.run_type == "train":
            self.train_data_list, self.validate_data_list, self.vacab_data_list = self.convert_util.gen_train_data()

    def __getitem__(self, index):
        if self.run_type == "train":
            return self.train_data_list[0][index], self.train_data_list[1][index], self.train_data_list[2][index]
        elif self.run_type == "validate":
            return self.validate_data_list[0][index], self.validate_data_list[1][index], self.validate_data_list[2][index]
        else:
            raise ValueError(f"error run type: {self.run_type} !")

    def __len__(self):
        return self.dataset_size

    def get_vocab(self):
        return self.vacab_data_list
