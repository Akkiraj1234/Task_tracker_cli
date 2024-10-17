from typing import Literal, Union, Any


# fix it with new things database management language
def add(
    name: str = None,
    inside: str = None,           #setting.defult_table,
    mark:str = None,              #Literal["done", "to_do", "progress"] = "to_do",
    object =  None,               #Union[Tables, Tasks] = task,
    **kw
) -> Any:
    """_summary_

    Args:
        name (str): _description_
        object (Tables | Tasks, optional): _description_. Defaults to Task.
        table (str, optional): the name of the table of id. Defaults to utils.defult_table.
    """
    return object.add(
        name=name, 
        mark=mark,
        inside=inside,
        **kw
    )

def delete(
    id: str = None,
    table: str = None,      #setting.defult_table,
    cleardata: bool = None, #False,
    object = None,          #Union[Tables, Tasks] = task,
    **kw
) -> Any:
    """_summary_

    Args:
        id (str | int): _description_
        object (Union[Tables, Tasks], optional): _description_. Defaults to task.
        table (str, optional): _description_. Defaults to setting.defult_table.
        cleardata (bool, optional): _description_. Defaults to False.
    """
    return object.delete(
        id=id,
        table=table,
        cleardata=cleardata,
        **kw
    )

def show(
    id: str | int = None,
    table: str = None,    #setting.defult_table,
    object = None,        #Union[Tables, Tasks] = task,
    **kw
) -> Any:
    """_summary_

    Args:
        id (_type_, optional): _description_. Defaults to id.
        object (Union[Tables, Tasks], optional): _description_. Defaults to task.
        table (str, optional): _description_. Defaults to setting.defult_table.
        cleardata (bool, optional): _description_. Defaults to False.
    """
    return object.show(
        id=id,
        table=table,
        **kw
    )

def update(
    id: str | int = None,
    name: str = None,
    status:str = None,
    description: str = None,
    table: str = None, #setting.defult_table,
    object = None, #Union[Tables, Tasks] = task,
    **kw
) -> Any:
    """_summary_

    Args:
        id (str | int): _description_
        name (str, optional): _description_. Defaults to None.
        description (str, optional): _description_. Defaults to None.
        object (Union[Tables, Tasks], optional): _description_. Defaults to task.
        table (str, optional): _description_. Defaults to setting.defult_table.
    """
    return object.update(
        id = id,
        name = name,
        description = description,
        table = table,
        status = status
    )




class DatabaseManagmentLanguage:
    def __init__(self, command:str):
        
        for i in command:
            print(i)


if __name__ == "__main__":
    print(DatabaseManagmentLanguage("hello world"))
