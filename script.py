from typing import Literal, Union
from database import Tables, Tasks, setting , task, table

#fix it with new things
def add(
    name:str,
    object:Union[Tables, Tasks] = task,
    table:str = setting.defult_table,
    mark:Literal['done','to_do','progress'] = "to_do",
    **kw
) -> None:
    """_summary_

    Args:
        name (str): _description_
        object (Tables | Tasks, optional): _description_. Defaults to Task.
        table (str, optional): the name of the table of id. Defaults to utils.defult_table.
    """
    if mark not in ['done','to_do','progress']:
        print("some error will write in future")
        mark = 'to_do'
    
    return object.add(
        name = name,
        mark = mark,
        inside = table,
        **kw
    )

def delete(
    id:str|int,
    object:Union[Tables, Tasks] = task,
    table:str = setting.defult_table,
    cleardata:bool = False,
    **kw
) -> None:
    """_summary_

    Args:
        id (str | int): _description_
        object (Union[Tables, Tasks], optional): _description_. Defaults to task.
        table (str, optional): _description_. Defaults to setting.defult_table.
        cleardata (bool, optional): _description_. Defaults to False.
    """
    return object.delete(
        id = id,
        table = table,
        cleardata = cleardata,
        **kw
    )

def show(
    id:str|int = None,
    object:Union[Tables, Tasks] = task,
    table:str = setting.defult_table,
    **kw
) -> None:
    """_summary_

    Args:
        id (_type_, optional): _description_. Defaults to id.
        object (Union[Tables, Tasks], optional): _description_. Defaults to task.
        table (str, optional): _description_. Defaults to setting.defult_table.
        cleardata (bool, optional): _description_. Defaults to False.
    """
    return object.show(
        id = id,
        table = table,
        **kw
    )

def update(
    id:str|int,
    name:str = None,
    description:str = None,
    object:Union[Tables, Tasks] = task,
    table:str = setting.defult_table,
    **kw
) -> None:
    """_summary_

    Args:
        id (str | int): _description_
        name (str, optional): _description_. Defaults to None.
        description (str, optional): _description_. Defaults to None.
        object (Union[Tables, Tasks], optional): _description_. Defaults to task.
        table (str, optional): _description_. Defaults to setting.defult_table.
    """
    object.update(
        id = id,
        name = name,
        description = description,
        table = table,
    )
    









if __name__ == '__main__':
    print(update('something',"something",description="hello world! :)",object=table))
    # ==========================================
    # print(delete(None,table,"something",True))
    #==========================
    # print('test-1-table-show',show(None,table),'\n')
    # print('test-2-table-show',show('something',table),'\n')
    # print('test-3-table-show',show('something1',table),'\n')
    # print(show(None,task))
    # print(show(None,task,"demo_table3"))
    # add('something',task, table='something',mark="to-do")
    # delete("5", task, 'demo_table4')
    # add(
    #     name = 'no table task',
    #     object = task,
    #     mark = 'progress'
    # )
    pass

