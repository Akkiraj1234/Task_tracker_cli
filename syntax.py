from utils import List, Tuple, Color
import re
from database import system,table,task,setting
from script import add, delete, show, update

class SyntaxError(Exception):
    def __init__(self, text = None, data_list = None, index:int = 0):
        error_message = ''
        
        if text:
            error_message+=f"{Color.color(text, 'red')}\n"
        
        if data_list:
            data_list[index] = Color.color(data_list[index], 'b-red')
            error_message += f"{Color.color('>>>', 'cyan')} {' '.join(data_list)}\n"
        
        len_ = lambda value: len(value) + 1
        lenght = sum(map(len_, data_list[:index])) if data_list else len(text) if text else 0
        error_message += f"{Color.color('>>>','cyan')} {'-'*lenght}^"
        
        super().__init__(error_message)


class Command:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.inteprator = Inteprator()
    
    def add_synatx(self):
        pass
    
    def execute(self, command:str) -> None:
        tokenize = self.lexer.tokenize(command)


class Lexer:
    """
    The `Lexer` class is responsible for tokenizing and validating commands in the `task_cli` application, version 1.0.
    
    This class breaks down command strings into structured tokens and ensures they adhere to specific syntax rules. It supports the parsing of operations, objects, clauses, strings, and numbers based on well-defined patterns. If the syntax of the command string is invalid, the class raises appropriate errors.

    ### Patterns Supported:
    - **Operation:** Starts with a capital letter followed by up to 18 letters (either lowercase or uppercase). Maximum length: 20 characters.
    - **Objects:** Starts with a capital letter followed by up to 13 lowercase letters. Maximum length: 15 characters.
    - **Clauses:** Lowercase letters with underscores, up to 19 characters.
    - **Strings:** Enclosed in double quotes, up to 250 characters.
    - **Numbers:** Integers between 1 and 99.
    
    ### Default Behavior:
    - If an object is missing or invalid, a default object `"Task"` will be used.
    
    ### Error Handling:
    - Raises `SyntaxError` when a token does not match the expected pattern.
    
    Attributes:
        operation_pattern (str): Regex pattern for matching valid operation tokens.
        objects_pattern (str): Regex pattern for matching valid object tokens.
        clause_pattern (str): Regex pattern for matching valid clause tokens.
        defult_object (str): The default object to use if no valid object is provided.
        operation_size (int): Maximum allowed length for operation tokens.
        string_size (int): Maximum allowed length for string tokens.
    """
    def __init__(self) -> None:
        """
        Initializes the Lexer with predefined regular expression patterns for operations, objects, and clauses.
        
        Attributes:
            - `operation_pattern`: Pattern that matches operation strings (capitalized words up to 20 characters).
            - `objects_pattern`: Pattern for objects (capitalized word up to 15 characters).
            - `clause_pattern`: Pattern for clauses (lowercase with underscores, up to 20 characters).
            - `defult_object`: Default object value ("Task") used if no valid object is found.
            - `operation_size`: Maximum size for operations (20 characters).
            - `string_size`: Maximum length for string literals (250 characters).
        """
        self.operation_pattern = r"^[A-Z][a-zA-Z]{0,18}$"
        self.objects_pattern = r"^[A-Z][a-z]{0,13}$"
        self.clause_pattern = r"^[a-z_]{0,19}$"
        # self.string_pattern = r'^"[^"]*"{0,249}$'
        # self.digit_pattern = r"^[0-9][0-9]$"
        
        self.defult_object = 'Task'
        self.operation_size = 20
        self.string_size = 250
    
    def tokenize(self, command:str) -> List[str]:
        """
        Tokenizes and validates a command string.

        This method splits the input command into tokens and checks whether they conform to the defined syntax. 
        If valid, returns the structured tokens, else raises a `SyntaxError`.

        Args:
            command (str): The command string to be tokenized and validated.

        Returns:
            dict[str]: A dictionary of valid tokens that adhere to the CLI syntax.

        Raises:
            SyntaxError: If the command does not follow the expected syntax.
        """
        row_token = self.spilt(command)
        valid_token = self.syntax_checker(row_token)
        
        return valid_token
    
    def spilt(self, string: str) -> List[str]:
        """
        Splits the input string into tokens, allowing spaces inside quoted strings.

        This method divides the command string into components, respecting spaces within quotes and splitting other text by whitespace. It handles the correct formation of quoted strings.

        Args:
            string (str): The command string to be split into tokens.

        Returns:
            List[str]: A list of tokens derived from the command string.

        Example:
            >>> some_text = 'Add Task "Some text here"'
            >>> split(some_text)
            ['Add', 'Task', '"Some text here"']
        """
        result = []
        current_text = []
        in_quotes = False
        
        for char in string:
            if char == '"':
                in_quotes = not in_quotes
                current_text.append(char) #remove this line to remove double quotes from text 
                if not in_quotes:
                    result.append(''.join(current_text))
                    current_text = []
                continue
            
            if not in_quotes and char.isspace():
                if current_text:
                    result.append(''.join(current_text))
                    current_text = []
                continue
                
            current_text.append(char)
        
        if current_text: result.append(''.join(current_text))
        return result
    
    def syntax_checker(self, tokens:List[str]) -> List[str]:
        """
        Validate the syntax of commands according to version 1.0 of the `task_cli` application.

        This method checks whether the provided command string adheres to the expected syntax structure.
        If the command is valid, the method returns a structured command list. Otherwise, it raises a `SyntaxError`.

        The supported syntax is as follows:

        Syntax Structure:
            operation [object] ("text" or option "text") option text ...

        Where the components are defined as:

        ### 1. Operators:
            - Should contain only letters (a-z).
            - The first character must be capitalized, and the rest can be either lowercase or uppercase.
            - Maximum length: 20 characters.
            - **Raises:** `SyntaxError` for invalid operator formats.

        ### 2. Objects:
            - Should contain only letters (a-z).
            - The first character must be capitalized, and the remaining characters should be lowercase.
            - Maximum length: 15 characters.
            - **Default Handling:** If no valid object is found, default data will be used. No error is raised.

        ### 3. Clauses:
            - Should contain only lowercase letters (a-z) and underscores (_).
            - Maximum length: 20 characters.
            - Only one clause is allowed. No subsequent clauses after the first one.
            - **Raises:** `SyntaxError` if the clause is not valid (unrecognized clause).

        ### 4. Strings:
            - Must be enclosed in double quotes ("").
            - Can contain any characters inside the quotes.
            - Maximum length: 250 characters.
            - Only one string is allowed. No subsequent strings after the first one.
            - **Raises:** `SyntaxError` in the following cases:
                - If the string is not properly enclosed in double quotes.
                - If the string exceeds the 250-character limit.
                - If the string is unrecognized or malformed.

        ### 5. Numbers (Num):
            - Must be an integer between 1 and 99.
            - Only one number is allowed. No subsequent numbers after the first one.
            - **Raises:** `SyntaxError` if the number is invalid (unrecognized or out of range).

        ### 6. Other Rules:
            - Each token must be separated by whitespace.
            - Any entity that does not match the expected syntax will raise an error (unrecognized entity error).

        ### Examples of supported commands:
            >>> Add "hello world"
            >>> Add Task "hello world" inside "table1"

        Args:
            tokens (List[str]): A list of tokens representing the parts of a command.

        Returns:
            List[str]: A structured list of tokens if the command matches the expected syntax.

        Raises:
            SyntaxError: If the command does not conform to the expected syntax.
        """

        modified_token = []
        before , index = None , 0
        
        # if tokens are less than 1, return as view management language
        if len(tokens) <= 1:
            return tokens
        
        # NUMBER1: Operation (required)
        if not len(tokens[index]) <= self.operation_size:
            raise SyntaxError(f"Size Limit Exceeded: The operation '{tokens[index]}' should be at most {self.operation_size} characters long.", tokens, index)
        if re.match(self.operation_pattern, tokens[index]):
            modified_token.append(tokens[index])
            index += 1
        else: raise SyntaxError(f"Invalid Operation: '{tokens[index]}' must be an alphabetic string with the first character capitalized.", tokens, index)
        
        # NUMBER2: Objects (optional)
        if re.match(self.objects_pattern, tokens[index]):
            modified_token.append(tokens[index])
            index += 1
        else: modified_token.append(self.defult_object)
        
        # NUMBER3: Allowed text and number and clause (one required)
        while index < len(tokens):
            start = index
            if tokens[index].startswith('"'):
                if before == 'string':
                    raise SyntaxError(f"Invalid Syntax: Two consecutive strings are not allowed. Found: '{tokens[index]}'", tokens, index)
                if not tokens[index].endswith('"'):
                    raise SyntaxError(f"String Error: The string starting with '{tokens[index][:10]}...' was not properly closed with a double quote.", tokens, index)
                if not len(tokens[index]) < 250:
                    raise SyntaxError(f"String Length Exceeded: The string '{tokens[index][:10]}...' exceeds the 250-character limit.", tokens, index)
                
                modified_token.append(tokens[index])
                index, before = index + 1, 'string'
            
            elif tokens[index].isdigit() and len(tokens[index]) < self.string_size:
                if before == 'digit': 
                    raise SyntaxError(f"Invalid Syntax: Two consecutive numbers are not allowed. Found: '{tokens[index]}'", tokens, index)
                modified_token.append(tokens[index])
                index, before = index + 1, 'digit'
            
            elif re.match(self.clause_pattern, tokens[index]):
                if before == 'clause': 
                    raise SyntaxError(f"Invalid Syntax: Two consecutive clauses are not allowed. Found: '{tokens[index]}'", tokens, index)
                modified_token.append(tokens[index])
                index, before = index + 1, 'clause'

            if start == index:
                raise SyntaxError(f"Unrecognized Token: '{tokens[index]}' is not a valid operation, object, string, number, or clause.", tokens, index)
        
        return modified_token


class Parser:
    def __init__(self):
        self.valid_operations = {'Add':add}
        self.valid_objects = {'Task':task, 'Table':table}
    
    def parse(self, tokens:list[str]) -> dict[str:str]:
        oood = self.create_OOOD_data(tokens)
    
    def check_syantax(token:List[str]) -> dict[str:str]:
        pass
    
    def create_OOOD_data(self, tokens:List[str]) -> dict[str:str]:
        """
        the OOO Data is base of task_cli syntax analysing the OOO
        (operation, objects, options) tells which operastion to perfom,
        in which objects to perform and what are there options and data
        by fillding defult data where for objects its task: data structure >
        >>> data = {
        >>>    'operation': None,
        >>>    'objects': task,
        >>>    'options': []
        >>> }

        Raises:
            SyntaxError: if operation is not given or invalid raise

        Returns:
            dict[str:str]: dict containing info 
        """
        num = 0
        data = {
            'operation': None,
            'objects': task,
            'options': []
        }
        if tokens[0].lower() in self.valid_operations.keys():
            data['operation'] = self.valid_operations[tokens[0].lower()]
            num += 1
        else: raise SyntaxError(f"invalid operation: ({tokens[0]}) should be {self.valid_operations.keys()}")
        
        if tokens[1].lower() in self.valid_objects.keys():
            data["objects"] = self.valid_objects[tokens[1].lower()]
            num += 1
        else: pass
    
        data['options'] = tokens[num:]
        return data


class Inteprator:
    pass



command = Command()
def test_3():
    lexer = Lexer()
    commands = [
        'Add "some tasks"',
        'Add "some tasks"',
        'Add "some text inside table1',
        'Add "some tasks" inside "table1" mark "done"',
        'Add Task "some tasks" inside "table1" mark "done"',
        'Add Table "some table"',
        'Delete 1',
        'Delete task 1',
        'Delete 1 inside "table1"',
        'Delete task 1 inside "table1"',
        'Delete table "table1"',
        'Delete table "table1" cleardata',
        'Update 1 "hello world"',
        'Update Task 1 name "hello world"',
        'Update Task id 1 status "to_do"',
        'Update Task 1 name "hello_world" inside "table2"',
        'Update Table "table1" "table2"',
        'Update Table "table1" name "table2"',
        'Update Table "table1" description "hello world"',
        'Show table',
        'Show table "name"',
        'Show task',
        'Show task inside "name"',
        #exception
        'Add "Hello" "World"',
        'add "hello" "world"',
        'AddSomeLargeTextERROR Table "hello world"',
        'Add task "Hello World" inside "table1" "table2"',
        'TooLongTextThatExceedsTwentyChars task "some task here"',
        'Add tableNameThatIsLonge "valid text" inside "some text here"'
    ]
    
    for command in commands:
        try:
            print('---------------------------------')
            print(h:= lexer.spilt(command))
            print(lexer.syntax_checker(h))
        except SyntaxError as e:
            print(e)

def test_4():
    lexer = Lexer()
    commands = [
        'Add "some tasks"',
        'Add "some tasks" inside "table1" mark "done"',
        'Add Task "some tasks" inside "table1" mark "done"',
        'Add Table "some table"',
        'Delete 1',
        'Delete Task 1',
        'Delete 1 inside "table1"',
        'Delete Task 1 inside "table1"',
        'Delete Table "table1"',
        'Delete Table "table1" cleardata',
        'Update 1 "hello world"',
        'Update Task 1 name "hello world"',
        'Update Task id 1 status "to_do"',
        'Update Task 1 name "hello_world" inside "table2"',
        'Update Table "table1" name "table2"',
        'Update Table "table1" description "hello world"',
        'Show Table', #its should pass tho
        'Show Table "table1"',
        'Show Task',
        'Show Task inside "table2"',
        #exception
        'Add "Hello" "World"',
        'Update Table 1 1',
        'Update Table clause clasue',
        'update Table Clasue',
        'TooLongTextThatExceedsTwentyChars task "some task here"',
        'Add tableNameThatIsLonge "valid text" inside "some text here"',
        'Add "some text inside table1',
        'Add Table "hello world here is some text that is gonaa exceed 240 words ts have to be so i am just gonna write till it reaches 250 maybe i should try using ajhhdsjhjahdjahjadjahdjahdajhdjahdjahdjahdjahdjahdjahdjahdjahdjadjahdjadhjadhjahdjahdjahdjahdjahdjahdjahdjahdjadhjadhjahdjahdjahdad"',
        'Add Task # and & and 1'
    ]
    
    for command in commands:
        try:
            print('---------------------------------')
            print("command >_ :",command)
            print(lexer.tokenize(command))
        except SyntaxError as e:
            print(e)

if __name__ == "__main__":
    test_4()
    pass