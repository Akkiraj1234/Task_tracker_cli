import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import patch, MagicMock, mock_open,call
import json
from database import System, database_error, Tables, Tasks, Setting

@pytest.fixture
def system():
    return System()

@pytest.fixture
def mock_table_data():
    return {"table1": {"table_id": "1"}}

@pytest.fixture
def mock_task_data():
    return {
        "1": {
            "description": "Task 1",
            "status": "to-do",
            "created_at": 1609459200,
            "updated_at": 1609459200,
        }
    }

### Test Cases for System Class

def test_name(system):
    """Test System name property."""
    assert system.name in ["nt", "posix"]  # based on the platform

@patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"key": "value"}))
def test_load_data_file_exists(mock_file, system):
    """Test load_data when the file exists."""
    result = system.load_data("some_path.json")
    assert result == {"key": "value"}

@patch("builtins.open", side_effect=FileNotFoundError)
def test_load_data_file_not_found(mock_file, system):
    """Test load_data when the file does not exist."""
    result = system.load_data("some_path.json")
    assert result == {}

@patch("builtins.open", side_effect=json.JSONDecodeError("error", "doc", 0))
def test_load_data_invalid_json(mock_file, system):
    """Test load_data when the file contains invalid JSON."""
    result = system.load_data("some_path.json")
    assert result == {}

@patch("builtins.open", new_callable=mock_open)
def test_save_data(mock_file, system):
    """Test save_data with valid data."""
    system.save_data("some_path.json", {"key": "value"})
    mock_file.assert_called_once_with("some_path.json", "w", encoding="utf-8")

    # Get the actual write calls and compare them to the expected parts
    write_calls = [
        call('{'),
        call('\n    '),
        call('"key"'),
        call(': '),
        call('"value"'),
        call('\n'),
        call('}')
    ]
    mock_file().write.assert_has_calls(write_calls, any_order=False)
### Test Cases for Tables Class

@patch("database.System.load_data")
def test_get_tableid_by_name(mock_load_data, mock_table_data):
    """Test get_tableid_by_name when table exists."""
    mock_load_data.return_value = mock_table_data
    table = Tables()
    result = table.get_tableid_by_name("table1")
    assert result == "1"

def test_is_tableexists(mock_table_data):
    """Test is_tableexists method when table exists."""
    table = Tables()
    table.data = mock_table_data
    assert table.is_tableexists("table1") is True

def test_last_table_id(mock_table_data):
    """Test last_table_id returns the last table ID."""
    table = Tables()
    table.data = mock_table_data
    assert table.last_table_id() == "1"

def test_add_table_already_exists(mock_table_data):
    """Test adding a table that already exists."""
    table = Tables()
    table.data = mock_table_data
    with pytest.raises(database_error):
        table.add(name="table1")

@patch("database.System.add_fille")
def test_add_new_table(mock_add_file):
    """Test adding a new table successfully."""
    table = Tables()
    table.data = {}
    table.add(name="new_table")
    assert "new_table" in table.data
    mock_add_file.assert_called_once()

@patch("database.System.delete_file")
def test_delete_table(mock_delete_file):
    """Test deleting a table successfully."""
    table = Tables()
    table.data = {"table1": {"table_id": "1"}}
    table.delete(id="table1")
    assert "table1" not in table.data
    mock_delete_file.assert_called_once()

### Test Cases for Tasks Class

@patch("database.Tables.get_tableid_by_name", return_value="1")
@patch("database.System.load_data", return_value={"1": {}})
def test_add_task(mock_load_data, mock_get_table_id, mock_task_data):
    """Test adding a task successfully."""
    task = Tasks()
    task.add(name="Task 2", mark="done", inside="table1")
    assert "2" in task.data

def test_get_last_id(mock_task_data):
    """Test getting the last task ID."""
    task = Tasks()
    task.data = mock_task_data
    assert task.get_last_id() == 1

@patch("database.System.save_data")
def test_remove_task(mock_save_data, mock_task_data):
    """Test removing a task."""
    task = Tasks()
    task.data = mock_task_data
    task.remove_task(task_id="1")
    assert "1" not in task.data

@patch("database.System.save_data")
def test_delete_task(mock_save_data, mock_task_data):
    """Test deleting a task."""
    task = Tasks()
    task.data = mock_task_data
    task.delete(id="1", inside="table1")
    assert "1" not in task.data
    mock_save_data.assert_called_once()