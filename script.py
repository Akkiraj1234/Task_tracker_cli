from database import Tables, Tasks


def add(
    object:Tables|Tasks,
    name:str
) -> None:
    object.add(name)
    

































































# class show:
#     def __init__(self) -> None:
#         pass
    
#     def show(self, item:dict = None, id:str = None, under:str = None, detail:bool = False):
#         if not item: return
#         item = item()
#         print(load_data(item['path']))
        
        
        
        
        
    
        
    
# class add:
    
#     def __init__(self) -> None:
#         pass
    
#     def add(self, item:dict, name:str, under:str) -> None:
#         pass
    







# ADD = add()
# SHOW = show()

# GROUP = lambda: {'name':'group', 'path':GROUP_PATH}
# # TASK = lambda: {'name':'task', 'path':utils.current_task}

# print('command : ','show GROUP')
# SHOW.show(GROUP)
