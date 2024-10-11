import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import patch, MagicMock
from database import Tables, database_error

@pytest.fixture
def mock_system():
    """Fixture to mock system functions"""
    with patch('database.system') as mock_system:
        yield mock_system

@pytest.fixture
def tables_instance(mock_system):
    """Fixture to return a Tables instance with mocked system"""
    mock_system.TABLE_PATH = "mocked_table_path"
    mock_system.DB_PATH = "mocked_db_path"
    
    # Mock load_data to return some default data
    mock_system.load_data.return_value = {
        'table1': {'table_id': '1'},
        'table2': {'table_id': '2'}
    }
    
    return Tables()

def test_load_data(mock_system, tables_instance):
    """Test that __load method correctly loads data"""
    tables_instance.__load()
    mock_system.load_data.assert_called_once_with(mock_system.TABLE_PATH)
    assert tables_instance.data == {'table1': {'table_id': '1'}, 'table2': {'table_id': '2'}}

def test_add_table(mock_system, tables_instance):
    """Test adding a new table successfully"""
    tables_instance.add(name="table3")
    
    # Check that data has been added
    assert 'table3' in tables_instance.data
    assert tables_instance.data['table3']['table_id'] == '3'
    
    # Ensure that system save_data was called to update the storage
    mock_system.save_data.assert_called_once_with(mock_system.TABLE_PATH, tables_instance.data)
    
    # Ensure that the system.add_file was called with the correct table id
    mock_system.add_fille.assert_called_once_with((mock_system.DB_PATH, '3'), {})

def test_add_existing_table_error(tables_instance):
    """Test error raised when adding an existing table"""
    with pytest.raises(database_error, match="name: table1 already exits"):
        tables_instance.add(name="table1")

def test_get_tableid_by_name(tables_instance):
    """Test getting a table ID by name"""
    table_id = tables_instance.get_tableid_by_name('table1')
    assert table_id == '1'

def test_get_tableid_by_name_error(tables_instance):
    """Test error raised when getting a table ID that doesn't exist"""
    with pytest.raises(database_error, match="some error"):
        tables_instance.get_tableid_by_name('non_existing_table')

def test_delete_table(mock_system, tables_instance):
    """Test deleting an existing table"""
    tables_instance.delete(id="table1")
    
    # Ensure that data was removed from the tables instance
    assert 'table1' not in tables_instance.data
    
    # Check that system.save_data was called
    mock_system.save_data.assert_called_once_with(mock_system.TABLE_PATH, tables_instance.data)
    
    # Ensure that the file associated with the table ID is deleted
    mock_system.delete_file.assert_called_once_with((mock_system.DB_PATH, '1'))

def test_delete_nonexistent_table(tables_instance):
    """Test error raised when deleting a non-existing table"""
    with pytest.raises(database_error, match="name: table3 not exits"):
        tables_instance.delete(id="table3")

def test_last_table_id(tables_instance):
    """Test fetching the last table ID"""
    last_id = tables_instance.last_table_id()
    assert last_id == '2'

def test_last_table_id_empty(mock_system):
    """Test fetching last table ID when no tables exist"""
    mock_system.load_data.return_value = {}
    tables_instance = Tables()
    last_id = tables_instance.last_table_id()
    assert last_id == "1"
