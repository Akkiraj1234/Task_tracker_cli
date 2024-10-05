import os
from shutil import *
import json
import argparse

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(FILE_PATH, 'database')
GROUP_PATH = os.path.join(DB_PATH,'account.json')
SETTING_PATH = os.path.join(DB_PATH,'setting.json')


def load_data(path) -> dict:
    try:
        with open(path,'r', encoding='utf-8') as data:
            return json.load(data)
        
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(path, data) -> None:
    with open(path, 'w', encoding='utf-8') as json_data:
        json.dump(data, json_data, indent=4)

class info:
    def __init__(self) -> None:
        self.setting = None
        self.current_account = None
        self.__group_data = None
        self.update_info()
    
    @property
    def group_list(self):
        if self.__group_data is not None:
            return 
        self.__group_data = self.__group_data.keys()
        return self.__group_data
    
    @property
    def current_data(self):
        if self.current_account:
            return self.current_account
        self.current_account = load_data(self.setting["study plan 1"])
        return self.current_account

    def update_info(self):
        self.group_data = load_data(GROUP_PATH)
        self.setting = load_data(SETTING_PATH)

utils = info()