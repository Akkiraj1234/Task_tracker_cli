from utils import (
    os,
    GROUP_PATH, json, utils, load_data, save_data
)































































# def add_items(path, data, parent):
#     items = load_data(path)
    
#     if data['name'] in items.keys():
#         name = data['name']
#         print(f'FAILED : The {parent.name} name {name} already exist.')

#     items[data['name']] = data['data']
    
#     save_data(path, items)
    









# def list_accounts():
#     account = load_data(GROUP_PATH)
    
#     data = [(k, v.get('name',None)) for k,v in account.items()]
#     return data

# def create_account(data:dict):
#     account = load_data(GROUP_PATH)
    
#     #adding the data
#     id = len(account) + 1
#     account[id] = data
    
#     save_data(GROUP_PATH, account)
    
# def list_accounts():
#     pass

# # def open_database(name:str):
# #     if utils.current_account.name != name:
# #         pass #currently passing it but need to save data

    

# # print(list_accounts())
# # create_account({"name": "demo_user2",
# #         "language": "en",
# #         "path": "0012"})
# # print(list_accounts())