from typing import Literal, Union
from database import Tables, Tasks, setting , task, table


def add(
    name:str,
    object:Union[Tables, Tasks] = task,
    table:str = setting.defult_table,
    mark:Literal['done','to-do','progress'] = "to_do",
    **kw
) -> None:
    """_summary_

    Args:
        name (str): _description_
        object (Tables | Tasks, optional): _description_. Defaults to Task.
        table (str, optional): the name of the table of id. Defaults to utils.defult_table.
    """
    if mark not in ['done','to-do','progress']:
        print("some error will write in future")
        mark = 'to-do'
    
    object.add(
        name = name,
        mark = mark,
        inside = table,
        **kw
    )

def delete(
    id:str|int,
    object:Union[Tables, Tasks] = task,
    table:str = setting.defult_table,
    cleardata:bool = False
) -> None:
    """_summary_

    Args:
        id (str | int): _description_
        object (Union[Tables, Tasks], optional): _description_. Defaults to task.
        table (str, optional): _description_. Defaults to setting.defult_table.
        cleardata (bool, optional): _description_. Defaults to False.
    """
    object.delete(
        id = id,
        inside = table,
        cleardata = cleardata
    )

def show(
    id:str|int = None,
    object:Union[Tables, Tasks] = task,
    table:str = setting.defult_table,
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
        table = table
    )

def update(
    id:str|int,
    new_name:str|int,
    object:Union[Tables, Tasks] = task,
    table:str = setting.defult_table,
) -> None:
    """_summary_

    Args:
        id (str | int): _description_
        new_name (str | int): _description_
        object (Union[Tables, Tasks], optional): _description_. Defaults to task.
        table (str, optional): _description_. Defaults to setting.defult_table.
    """
    









if __name__ == '__main__':
    pass
    add('something',task, table='something',mark="to-do")
    # delete("5", task, 'demo_table4')
    # add(
    #     name = 'no table task',
    #     object = task,
    #     mark = 'progress'
    # )

