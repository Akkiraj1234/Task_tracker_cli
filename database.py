from utils import (
    os, json, utils, load_data, save_data, delte_file, add_file, TABLE_PATH, DB_PATH, time
)
class id_error(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

class Tables:
    def __init__(self):
        self.__load()
        
    def __load(self):
        self.data:dict = load_data(TABLE_PATH)
        
    def __update(self):
        save_data(TABLE_PATH, self.data)

    def create_table(self, name_id):
        """
        create new table and save it in the database 
        and retrun the status by boolean and a message

        Args:
            name_id (str): the name or id of the table

        Returns:
            tuple[bool,str]: return a tuple containing boolen weather the prosee susseed or not with a str message
        """
        if name_id in self.data.keys():
            return False, f"name: {name_id} already exits, use another name"
        
        table_id = self.last_table_id()
        
        if not table_id:
            return False, f"there is some error can not create new table name {name_id} error: 112"
        
        data = {
            'table_id': str(int(table_id)+1)
        }
        
        #adding the data
        self.data[name_id] = data
        self.__update()
        add_file((DB_PATH,table_id),{})
        return True, f"name: {name_id} table has created"

    def remove_table(self, name_id):
        
        if name_id not in self.data.keys():
            return False, f"name: {name_id} does not exits, add valid name!"
        
        table_id = self.data.pop(name_id,{'table_id':None}).get('table_id',None)
        
        if not table_id:
            return False, f'cant delte the table {name_id} there is some error: 113'
        
        self.__update()
        delte_file((DB_PATH,table_id))
        return True, f'the table {name_id} has been deleted'
    
    def last_table_id(self) -> str|None:
        try:
            data = next(reversed(self.data))
            data = self.data[data]
            return data.get('table_id',None)
        
        except StopIteration:
            return "1"

    def add(self):
        pass
class Tasks:
    
    def __init__(self, table_id:str = None) -> None:
        self.oldt_id = table_id
        self.data = None
        self.__load('1')
    
    def __load(self, table_id = None):
        if table_id and self.oldt_id != table_id:
            self.oldt_id = table_id
            
        elif self.oldt_id is None:
            raise id_error('the id is none: id shuld be str (for dev there is way to solve it)')
        
        self.data = load_data((DB_PATH, f"{self.oldt_id}.json"))
    
    def __update(self, table_id = None):
        if table_id and self.oldt_id != table_id:
            self.oldt_id = table_id
            
        elif self.oldt_id is None:
            raise id_error('the id is none: id shuld be str (for dev there is way to solve it)')
        
        save_data((DB_PATH, f"{self.oldt_id}.json"), self.data)
    
    def add_task(self, task:str, date:str = time.time(), status:str = 'to-do')-> tuple[bool,str]:
        if self.data is None:
            self.__load()
        
        id_ = self.get_last_id()+1
        data = {
            'description': task,
            'status': status,
            'created_at': date,
            'updated_at':date,
        }
        
        self.data[str(id_)] = data
        self.__update()
        return True, f"the task: {task} added in the table {id_}"
        
    def remove_task(self, task_id:str) -> tuple[bool,str]:
        if self.data is None:
            self.__load()
        
        self.data.pop(task_id, None)
        self.__update()
        return True, f"the task: {task_id} has been deleted"

    def get_last_id(self):
        try:
            last_id = next(reversed(self.data))
        except StopIteration:
            last_id = 0
        return int(last_id)

    def add(self, name:str, **args) -> None:
        self.add_task(
            task=name
        )
    

def test_1():
    hello = Tables()
    print(hello.last_table_id())
    print(hello.create_table('demo_table4'))
    print(hello.last_table_id())
    _ = input()
    print(hello.remove_table('demo_table4'))
    print(hello.last_table_id())

def test_2():
    h = Tasks()
    print(h.add_task('added a first task in list'))
    print(h.remove_task("3"))

if __name__ == '__main__':
    # test_1()
    test_2()
    
    
        

# use it for the task 
# def create_data(self):
        
#         try:
#             last_id = last_key = next(reversed(self.data))
#         except StopIteration:
#             last_id = 1
    
#         data = {
#             'name'
#         }
    
#         #adding the data
#         self.data[int(last_id)+1] = data




# def get_id_by_name(self, name):
#         if self.data is None or not bool(self.data):
#             self.__load()
        
#         for id, data in self.data.items():
#             if data.get('name',None) == name:
#                return id






















































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