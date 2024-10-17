import pytest
import sys, os, pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from syntax import Lexer

# Create a fixture to initialize the Lexer class before each test
@pytest.fixture
def lexer():
    return Lexer()

# Test tokenize method
def test_tokenize_valid(lexer):
    # Valid cases
    command = 'Add Task "This is a valid string"'
    expected_tokens = ['Add', 'Task', '"This is a valid string"']
    assert lexer.tokenize(command) == expected_tokens

    command = 'Update "This is another string"'
    expected_tokens = ['Update', 'Task', '"This is another string"']
    assert lexer.tokenize(command) == expected_tokens

def test_tokenize_invalid(lexer):
    # Invalid operation
    with pytest.raises(SyntaxError):
        lexer.tokenize('invalidOperation Task "This is a string"')

    # Unclosed string
    with pytest.raises(SyntaxError):
        lexer.tokenize('Add Task "This is an unclosed string')

    # Exceeding string length
    with pytest.raises(SyntaxError):
        long_string = '"{}"'.format("a" * 251)
        lexer.tokenize(f'Add Task {long_string}')

    # Two consecutive strings
    with pytest.raises(SyntaxError):
        lexer.tokenize('Add Task "First string" "Second string"')

# Test split method
def test_split(lexer):
    # Simple split cases
    command = 'Add Task "A string with spaces"'
    expected_split = ['Add', 'Task', '"A string with spaces"']
    assert lexer.spilt(command) == expected_split

    command = 'Add "Another test"'
    expected_split = ['Add', '"Another test"']
    assert lexer.spilt(command) == expected_split

def test_split_edge_cases(lexer):
    # Handle empty string
    assert lexer.spilt('') == []

    # Handle no quoted string
    command = 'Add Task'
    expected_split = ['Add', 'Task']
    assert lexer.spilt(command) == expected_split

    # Handle single quoted string
    command = '"Only one string"'
    expected_split = ['"Only one string"']
    assert lexer.spilt(command) == expected_split

# Test syntax_checker method
def test_syntax_checker_valid(lexer):
    # Valid cases
    tokens = ['Add', 'Task', '"A valid string"', 'inside', 'table1']
    expected_tokens = ['Add', 'Task', '"A valid string"', 'inside', 'table1']
    assert lexer.syntax_checker(tokens) == expected_tokens

    tokens = ['Update', '"Another valid string"']
    expected_tokens = ['Update', 'Task', '"Another valid string"']
    assert lexer.syntax_checker(tokens) == expected_tokens

def test_syntax_checker_invalid(lexer):
    # Invalid operation size
    tokens = ['Addddddddddddddddddddddd', 'Task', '"Too long operation"']
    with pytest.raises(SyntaxError):
        lexer.syntax_checker(tokens)

    # Invalid object format
    tokens = ['Add', 'taskNameThatIsTooLong', '"A string"']
    with pytest.raises(SyntaxError):
        lexer.syntax_checker(tokens)

    # Invalid string length
    long_string = '"{}"'.format("a" * 251)
    tokens = ['Add', 'Task', long_string]
    with pytest.raises(SyntaxError):
        lexer.syntax_checker(tokens)

    # Two consecutive clauses
    tokens = ['Add', 'Task', 'inside', 'inside']
    with pytest.raises(SyntaxError):
        lexer.syntax_checker(tokens)

    # Two consecutive strings
    tokens = ['Add', 'Task', '"First string"', '"Second string"']
    with pytest.raises(SyntaxError):
        lexer.syntax_checker(tokens)

