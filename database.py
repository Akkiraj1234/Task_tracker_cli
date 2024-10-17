import os
import json
import time


class database_error(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class System:
    """
    This class handles the loading, saving, and managing of JSON data files
    and provides utility methods for file path operations.
    """

    def __init__(self):
        """
        Initializes paths to the main directories and files in the system.
        """
        self.FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.DB_PATH = os.path.join(self.FILE_PATH, "database")
        self.TABLE_PATH = os.path.join(self.DB_PATH, "tables.json")
        self.SETTING_PATH = os.path.join(self.DB_PATH, "setting.json")

    @property
    def name(self) -> str:
        """
        Returns the name of the OS.
        :return: str representing the OS name.
        """
        return os.name

    def _path(self, path: str | tuple | list) -> str:
        """
        Joins a tuple or list of strings into a file path if needed.
        :param path: A string, tuple, or list representing the file path.
        :return: The constructed file path as a string.
        """
        if isinstance(path, tuple):
            path = os.path.join(*path)
        elif isinstance(path, list):
            path = os.path.join(*path)
        return path

    def load_data(self, path: str | tuple | list) -> dict:
        """
        Loads JSON data from a specified file path.
        :param path: A string, tuple, or list representing the file path.
        :return: A dictionary with the loaded data or an empty dict if an error occurs.
        """
        path = self._path(path)

        try:
            with open(path, "r", encoding="utf-8") as data_file:
                return json.load(data_file)

        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_data(self, path: str | tuple | list, data: dict) -> None:
        """
        Saves a dictionary as JSON data to a specified file path.
        :param path: A string, tuple, or list representing the file path.
        :param data: A dictionary to save as JSON.
        :raise database_error: If the file cannot be saved due to the file not existing.
        """
        path = self._path(path)

        try:
            with open(path, "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=4)
        except FileNotFoundError:
            raise database_error(
                f"Error: Cannot save to file. '{path}' does not exist."
            )
        except Exception as e:
            print(
                f"Failed: Unexpected error occurred while saving data to '{path}': {str(e)}"
            )

    def delete_file(self, path: str | tuple | list) -> None:
        """
        Deletes a file at a specified path.
        :param path: A string, tuple, or list representing the file path.
        :raise database_error: If the file cannot be deleted due to it not existing.
        """
        path = self._path(path)

        try:
            os.remove(path)
            print(f"File '{path}' successfully deleted.")
        except FileNotFoundError:
            raise database_error(f"Error: File '{path}' not found, cannot delete.")
        except Exception as e:
            print(f"Unexpected error occurred while deleting file '{path}': {str(e)}")

    def add_file(self, path: str | tuple | list, data: dict) -> None:
        """
        Adds new data to a file. Creates a new file if it doesn't exist.
        :param path: A string, tuple, or list representing the file path.
        :param data: A dictionary containing the data to be added.
        """
        path = self._path(path)

        if not os.path.exists(path):
            # If the file does not exist, create it by saving the data
            self.save_data(path, data)
        else:
            try:
                # Load the existing data and update it with the new data
                existing_data = self.load_data(path)
                existing_data.update(data)

                # Save the updated data back to the file
                self.save_data(path, existing_data)
            except Exception as e:
                print(
                    f"Unexpected error occurred while adding data to '{path}': {str(e)}"
                )


class Setting:
    """
    A class to manage application settings by loading them from a JSON configuration file.
    """

    def __init__(self):
        """
        Initializes the Setting class and prepares to load settings from the system.

        :param system: An instance of the System class for loading configuration data.
        """
        self.setting = None

    @property
    def defult_table(self) -> str | None:
        """
        Retrieves the default table from the settings. Loads settings if not already loaded.

        :return: The name of the default table or None if not found.
        """
        if self.setting is None:
            self._load()

        data = self.setting.get("table", None)

        if data is None or not bool(data):
            print(f"devloper: the data is none or empty need to set new defult")

        return data

    def update_data(self, key: str, value: str) -> None:
        """
        Updates a specific setting with the provided key and value.

        :param key: The key of the setting to update.
        :param value: The new value for the setting.
        :raise ValueError: If the key is not valid or if value is None or empty.
        """
        if not key or value is None or value == "":
            raise ValueError("Key cannot be empty and value cannot be None or empty.")

        # Update the setting with the new value
        if self.setting is None:
            self._load()  # Load settings if not already loaded

        self.setting[key] = value  # Update the setting with the new value
        self._update()  # Save the updated settings

    def _load(self) -> None:
        """
        Loads the settings from the specified settings file.
        """
        self.setting = system.load_data(system.SETTING_PATH)

    def _update(self) -> None:
        """
        Saves the current settings to the specified settings file.
        """
        system.save_data(system.SETTING_PATH, self.setting)


class Tables:
    def __init__(self) -> None:
        self.data = None
        self._load()

    def _load(self) -> None:
        self.data = system.load_data(system.TABLE_PATH)

    def _update(self) -> None:
        system.save_data(system.TABLE_PATH, self.data)

    def get_tableid_by_name(self, nameid: str) -> dict | None:
        if self.data is None:
            self._load()

        data = self.data.get(nameid, None)

        if data is None:
            raise database_error(
                f"some error becouse data is : {data} and the name id is invalid : {nameid}"
            )

        return data.get("table_id", None)

    def get_tabledata_by_name(self, nameid: str) -> dict | None:
        if self.data is None:
            self._load()

        return self.data.get(nameid, None)

    def is_tableexists(self, nameid: str) -> bool:
        if self.data is None:
            self._load()

        return nameid in self.data.keys()

    def last_table_id(self) -> str:
        if self.data is None:
            self._load()

        try:
            data = next(reversed(self.data))
            data = self.data[data]
            return data.get("table_id", None)

        except StopIteration:
            return "1"

    def valid_argument(self) -> dict:
        return {"name": str}

    def add(self, **kw) -> None:
        """
        create new table and save it in the database
        and retrun the status by boolean and a message

        Args:
            name_id (str): the name or id of the table

        Returns:
            tuple[bool,str]: return a tuple containing boolen weather the prosee susseed or not with a str message
        """
        name = kw.get("name", None)
        
        if not isinstance(name, str) or not name.strip():
            raise database_error("Invalid table name. Must be a non-empty string.")

        if self.is_tableexists(name):
            raise database_error(f"name: {name} already exits, use another name")

        table_id = str(int(self.last_table_id()) + 1)
        # apply something that if its return string insted of something then it will fix it
        # add a feature to get unique id which should be the best
        data = {
            "table_id": table_id,
            "description": "add the table description",
            "created_at": time.time(),
            "modified_at": time.time(),
        }

        # adding the data
        self.data[name] = data
        self._update()
        system.add_file((system.DB_PATH, f"{table_id}.json"), {})

    def delete(self, **kw) -> None:
        name_id = kw.get("table", None)
        cleardata = kw.get("cleardata", False)

        if not self.is_tableexists(name_id):
            raise database_error(f"name: {id} not exits, use valid name")

        table_id = self.data.get(name_id, {}).get("table_id", None)
        if not table_id:
            raise database_error(
                f"cant delete the {id} table is spasified with this name"
            )

        if cleardata:
            system.save_data((system.DB_PATH, f"{table_id}.json"), {})
            return

        self.data.pop(name_id, {})
        self._update()
        system.delete_file((system.DB_PATH, f"{table_id}.json"))

    def show(self, **kw) -> None:
        if self.data or self.data is None:
            self._load()

        table_id = kw.get("id", None)

        if table_id is not None and not self.is_tableexists(table_id):
            print(f"FAILED: there is no table exists with the name {table_id}")

        return self.data.get(table_id, self.data)

    def update(self, **kw) -> None:
        name_id = kw.get("id", None)
        name = kw.get("name", None)
        description = kw.get("description", None)

        if self.data or self.data is None:
            self._load()

        if not self.is_tableexists(name_id):
            raise database_error(f"the table Not exists name : {name_id} ")

        # gathering the previous data -modifying info
        defult_desc = self.data.get("description", "add the table description")

        # modifying the info
        self.data[name_id]["description"] = description if description else defult_desc

        # modifying name_id if exits
        if name and self.is_tableexists(name):
            self._update()
            raise database_error(
                f"cant change the name of table {name_id} to {name} table already exits with the name."
            )

        if name:
            self.data[name] = self.data.get(name_id)
            self.data.pop(name_id)

        self._update()


class Tasks:
    def __init__(self, table_id:str|None = None) -> None:
        self._old_id = None
        self.data = None
        if table_id is not None:
            self._load(table_id)

    def _load(self, table_id:str|None = None) -> None:
        if table_id == self._old_id:
            return
        
        try:
            self.data = system.load_data((system.DB_PATH, f"{table_id}.json"))
            self._old_id = table_id
        except FileNotFoundError:
            raise database_error("there is a probleam with the database")

    def _update(self, table_id:str|None = None) -> str:
        try:
            system.save_data((system.DB_PATH, f"{table_id}.json"), self.data)
        except Exception as e:
            raise database_error(f"some error: {e}")

    def get_last_id(self) -> None:
        if self.data is None:
            raise database_error("the data is none please load the table")
        
        try:
            last_id = next(reversed(self.data))
        except StopIteration:
            last_id = 0
            
        return last_id

    def unique_id(self) -> str:
        # needa fix to see if genrated id exist or not..
        return str(int(self.get_last_id()) + 1)

    def valid_argument(self):
        return {"name": str, "mark": str, "inside": str}
    
    def add(self, **kw) -> None:
        name = kw.get("name", "")
        status = kw.get("mark", "to-do")
        table_name = kw.get("inside", None)
        #if table_name exits then its gonna load
        #if table_name not exists or None its gonna raise databse_error
        
        if not (isinstance(table_name, str) and table.is_tableexists(table_name)):
            raise database_error(f"table name is invalid -> {None}")
        
        #if table data is okay its gonna retuen table_id -------------check under (_load(id))
        #if table data is not okay its gonna raise databse_error -------^
        table_id = table.get_tableid_by_name(table_name)
        self._load(table_id)
        date = time.time()

        data = {
            "description": name,
            "status": status,
            "created_at": date,
            "updated_at": date,
        }

        # if update method have some issue gonna raise error
        self.data[self.unique_id()] = data
        self._update(table_id)

    def delete(self, **kw) -> None:
        id = kw.get("id", "")
        table_name = kw.get("table", None)
        
        #if table name is invalid type and does not exist raise database error
        if not (isinstance(table_name, str) and table.is_tableexists(table_name)):
            raise database_error(f"table name is invalid -> {None}")
        
        #if table id is cant be assesed return None handel by _load
        table_id = table.get_tableid_by_name(table_name)
        self._load(table_id)

        #if id is invalid or not in dict its gonna raise database_error
        try: self.data.pop(id)
        except KeyError: raise database_error("invalid id: make sure task id is valid")
        self._update(table_id)

    def show(self, **kw) -> None:
        table_name = kw.get("table", None)
        # if table name is invalid raise databse error
        if not (isinstance(table_name, str) and table.is_tableexists(table_name)):
            raise database_error(f"table name is invalid -> {None}")
        
        # if table struture not good handele by get_tableid_by_name if error -> None
        #if table id is not given handele by _load if error -> {}
        table_id = table.get_tableid_by_name(table_name)
        self._load(table_id)

        return self.data

    def update(self, **kw) -> None:
        id = kw.get("id","")
        name = kw.get("name", None)
        status = kw.get("status", None)
        table_name = kw.get("table", None)
        
        # if table name does not exist or invalid raise database error
        if not (isinstance(table_name, str) and table.is_tableexists(table_name)):
            raise database_error(f"table name is invalid -> {None}")
        
        table_id = table.get_tableid_by_name(table_name)
        self._load(table_id)
        # if any error in data get {} empty dict and if id not in data.keys() raise error
        
        if not id in self.data.keys():
            raise database_error("the id is invalid ")
        
        try :
            self.data[id]['description'] = name if bool(name) else self.data[id]['description']
            self.data[id]['status'] = status if bool(status) else self.data[id]['status']
            self._update(table_id)
        except KeyError:
            raise database_error("there is some issue with the task cant be updated")


system = System()
setting = Setting()
table = Tables()
task = Tasks()