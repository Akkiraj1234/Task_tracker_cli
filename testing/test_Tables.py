from unittest.mock import patch, MagicMock

import sys, os, pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import Tables, database_error, system


@pytest.fixture
def mock_table():
    table = Tables()
    # Patch the _load method and _update method to prevent them from running
    with patch.object(table, "_load") as mock_load, patch.object(table, "_update") as mock_update:
        yield table, mock_load, mock_update


@pytest.mark.parametrize("table_data, table_name, expected_result", [
    ({"example_table": {"table_id": "1"}}, "example_table", "1"), 
    ({"example_table": {}}, "example_table", None), 
])
def test_get_table_id_by_name(mock_table, table_data, table_name, expected_result):
    mock_table, mock_load, mock_update = mock_table
    mock_table.data = table_data
    result = mock_table.get_tableid_by_name(table_name)
    assert result == expected_result
    
def test_get_table_id_by_name_invalid_structure(mock_table):
    mock_table, mock_load, mock_update = mock_table
    mock_table.data = {}
    
    with pytest.raises(database_error):
        mock_table.get_tableid_by_name("invalid_name")


#testing tablesdata
@pytest.mark.parametrize("table_data, table_name, expected_result", [
    (
        {
            "example_table": {
            "table_id": "1",
            "description": "a test description",
            "created_at": 1728649835.688255,
            "modified_at": 1728649835.688255 }
        },
        "example_table", 
        {
            "table_id": "1",
            "description": "a test description",
            "created_at": 1728649835.688255,
            "modified_at": 1728649835.688255 
        }
    ),
    ({}, "non_existent_table", None)
])
def test_get_tablesdata_by_name(mock_table, table_data, table_name, expected_result):
    mock_table, mock_load, mock_update = mock_table
    mock_table.data = table_data
    result = mock_table.get_tabledata_by_name(table_name)
    assert result == expected_result


@pytest.mark.parametrize("table_data, expected",[
    ({"table1":{"table_id":"3"}},"3"),
    (
        {"table1":{"table_id":"3"},"table2":{"table_id":"5"},
         "table4":{"table_id":"6"},"table6":{"table_id":"9"}},"9"
    ),
    ({},'1')
    
])
def test_last_table_id(mock_table, table_data, expected):
    mock_table, mock_load, mock_update = mock_table
    mock_table.data = table_data
    result = mock_table.last_table_id()
    assert result == expected

@pytest.mark.parametrize("table_data, table_name, expected",[
    ({"table1":{"table_id":"1"}},"table1",True),
    ({},'table1',False),
    ({"table1":{"table_id":"1"}},None, False),
    ({"table1":{"table_id":"1"}},123, False)
])
def test_is_tableexits(mock_table, table_data, table_name, expected):
    mock_table, mock_load, mock_update = mock_table
    mock_table.data = table_data
    result = mock_table.is_tableexists(table_name)
    assert result == expected
        
#testing add method -------------------------->
@pytest.mark.parametrize("table_data, new_tname, expected",[({"table1":{"table_id":"1"},"table2":{"table_id":"2"}},"table3","3")])
def test_add_unique_name(mock_table, table_data, new_tname, expected):
    mock_table, mock_load, mock_update = mock_table

    # Set initial data state
    mock_table.data = table_data

    # Patch the system.add_file to avoid writing to the file system
    with patch("database.system.add_file") as mock_add_file:
        # Call the add method
        mock_table.add(name=new_tname)

        # If data is None, _load should be called
        if table_data is None:
            mock_load.assert_called_once()
        else:
            mock_load.assert_not_called()

        # Check that the new table has been added to data
        assert new_tname in mock_table.data

        # Check the table ID of the newly added table
        table_id = mock_table.data[new_tname]["table_id"]
        assert table_id == expected

        # Ensure system.add_file was called with the correct arguments
        mock_add_file.assert_called_once_with((system.DB_PATH, f"{table_id}.json"), {})

def test_add_dublicate_name(mock_table):
    mock_table, mock_load, mock_update = mock_table
    mock_table.data = {"table1":{"table_id":"1"}}
    
    with patch("database.system.add_file") as mock_add_file:
        
        with pytest.raises(database_error):
            mock_table.add(name = "table1")
        
        mock_add_file.assert_not_called()
    
    mock_update.assert_not_called()


@pytest.mark.parametrize("name, error",[(None,database_error),(123,database_error)])
def test_add_diffent_value(mock_table, name, error):
    mock_table, mock_load, mock_update = mock_table
    mock_table.data = {"table1":{"table_id":'1'}}
    
    with patch("database.system.add_file") as mock_add_file:
        
        with pytest.raises(error):
            mock_table.add(name = name)
        
        mock_add_file.assert_not_called()

    mock_update.assert_not_called()
    

#writing for delete_method
pytest.mark.skip
def test_delete_existing_table(mock_table):
    mock_table, mock_load, mock_update = mock_table
    
    with patch("database.system.delete_file") as mock_delete_file:
        mock_table.delete(table="table1")
        
        # Check that table is deleted from data
        assert "table1" not in mock_table.data
        
        # Check that the delete_file was called with the correct arguments
        mock_delete_file.assert_called_once_with((system.DB_PATH, "1.json"))