import os
import sys
import json
import argparse
import time

if os.name == 'nt':
    import msvcrt
    termios = None
    tty = None
else:
    import termios
    import tty
    

def load_data(path) -> dict:
    if isinstance(path, tuple):
        path = os.path.join(*path)
        
    try:
        with open(path,'r', encoding='utf-8') as data:
            return json.load(data)
        
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(path, data) -> None:
    if isinstance(path, tuple):
        path = os.path.join(*path)
        
    with open(path, 'w', encoding='utf-8') as json_data:
        json.dump(data, json_data, indent=4)

def delte_file(path) -> None:
    pass

def add_file(path, data) -> None:
    pass

class info:
    def __init__(self) -> None:
        self.setting = None
        self.current_account = None
        self.__group_data = None
        self.update_info()
    
    @property
    def group_list(self):
        if self.__group_data is not None:
            return 
        self.__group_data = self.__group_data.keys()
        return self.__group_data
    
    @property
    def current_data(self):
        if self.current_account:
            return self.current_account
        self.current_account = load_data(self.setting["study plan 1"])
        return self.current_account

    def update_info(self):
        self.group_data = load_data(TABLE_PATH)
        self.setting = load_data(SETTING_PATH)


class CILcolor:
    
    fg_color = {
        'black': '\x1b[30m',
        'red': '\x1b[31m',
        'green': '\x1b[32m',
        'yellow': '\x1b[33m',
        'blue': '\x1b[34m',
        'magenta': '\x1b[35m',
        'cyan': '\x1b[36m',
        'white': '\x1b[37m',         
        'none': '\x1b[39m',
        'b-black': '\x1b[90m',
        'b-red': '\x1b[91m',
        'b-green': '\x1b[92m',
        'b-yellow': '\x1b[93m',
        'b-blue': '\x1b[94m',
        'b-magenta': '\x1b[95m',
        'b-cyan': '\x1b[96m',
        'b-white': '\x1b[97m',
    }
    bg_color = {
        'black': '\x1b[40m',
        'red': '\x1b[41m',
        'green': '\x1b[42m',
        'yellow': '\x1b[43m',
        'blue': '\x1b[44m',
        'magenta': '\x1b[45m',
        'cyan': '\x1b[46m',
        'white': '\x1b[47m',         
        'none': '\x1b[49m',
        'b-black': '\x1b[100m',
        'b-red': '\x1b[101m',
        'b-green': '\x1b[102m',
        'b-yellow': '\x1b[103m',
        'b-blue': '\x1b[104m',
        'b-magenta': '\x1b[105m',
        'b-cyan': '\x1b[106m',
        'b-white': '\x1b[107m',
    }    
    
    def __init__(self) -> None:
        pass
    
    def color(self, string:str, color:str|tuple|list) -> str:
        return self.__check_color(string, color, self.fg_color, 38, 39) if color else string
    
    def style(self, string:str, color:str|tuple|list = None, background:str|tuple|list = None, bold:bool = False, italic:bool = False, underline:bool = False ) -> str:
        
        if color: string = self.__check_color(string, color, self.fg_color, 38, 39)
            
        if background: string = self.__check_color(string, background, self.bg_color, 48, 49)
        
        if bold: string = f"\x1b[1m{string}\x1b[0m"
        
        if italic: string = f"\x1b[3m{string}\x1b[0m"
        
        if underline: string = f"\x1b[4m{string}\x1b[0m"
            
        return string

    def __check_color(self,string, color:str, dict_:dict, code:int, code_end:int):
        
        if isinstance(color, tuple) or isinstance(color, list) and len(color) >= 2:
            ansi_code = f'\x1b[{code};2;{color[0]};{color[1]};{color[2]}m'
            string = f"{ansi_code}{string}\x1b[{code_end}m"
        
        elif isinstance(color, str):
            ansi_color_code = dict_.get(color, f"\x1b[{code_end}m")
            string = f"{ansi_color_code}{string}\x1b[{code_end}m"
            
        return string
    

class SmartInput:
    """
    A real-time character-based input handler class for capturing user input without needing Enter to finalize each key press.

    Features:
    ----------
    1. **Real-Time Input**: Instantly processes typed characters, including shift, caps lock, numbers, and symbols.
    2. **Backspace Support**: Allows deleting characters using the backspace key.
    3. **Color Support**: Colorizes text based on predefined word-color mappings using ANSI codes.
    4. **Terminal Control**: Dynamically updates the terminal, rewriting the current line with updated content.

    Limitations:
    ------------
    1. **Unsupported Keys**: Esc, Insert, Delete, Arrow Keys, Page Up, End not handled.
    2. **Ctrl+X**: Cutting isn't supported, but Ctrl+C and Ctrl+V work.
    
    Input Flow:
    ------------
    1. Shows a prompt.
    2. Updates input in real time, processes backspace and colorizes text.
    3. Returns the full input string on Enter.
    4. support all str methods
    
    Example:
    ------------
    >>> input_handler = SmartInput()
    
    >>> # Define a color dictionary where specific words are associated with colors
    >>> input_handler.color_dict = {
    >>>    "hello": "green",
    >>>    "world": "blue",
    >>>    "error": "red"
    >>> }

    >>> # Prompt the user for input and colorize specific words
    >>> user_input = input_handler.take_input("Say hello to the world: ")
    
    >>> # Output the result
    >>> print(f"Captured Input: {user_input}")
    """
    def __init__(self) -> None:
        self.input_buffer = ''
        self.char = ''
        self.color_dict:dict = None
        self.color = CILcolor()
        
    def __get_char_unix(self) -> bytes:
        """
        read a single character without waiting for enter on unix like system.
        """
        fd = sys.stdin.fileno()
        old_setting = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcseattr(fd, termios.TCSADRAIN, old_setting)
        
        return ch.encode()
        
    def _return(self, return_color:bool) -> str:
        return_value = self.input_buffer
        
        if return_color:
            return_value = self.color_the_string(return_value)
            
        self.input_buffer = ''
        self.char = ''
        return return_value
    
    def get_char(self) -> bytes:
        """
        Reads a single character without waiting for Enter (Windows only).
        """
        if os.name == 'nt':
            return msvcrt.getch() 
        else:
            return self.__get_char_unix()
    
    def add_color(self, color:dict) -> None:
        self.color_dict = color
    
    def input(self, prompt:str, return_color:bool = True) -> str:
        # sys.stdout.write(prompt)
        print(prompt, flush=True, end='')
        
        while True:
            self.char = self.get_char()
            
            if self.char == b'\x08':
                if not len(self.input_buffer):
                    continue
                
                self.input_buffer = self.input_buffer[:-1] #updating the main text
                sys.stdout.write('\b \b')
            
            elif self.char == b'\r':
                sys.stdout.write('\n')
                sys.stdout.flush()
                break
            
            else:
                char = self.char.decode('ansi', errors='ignore')
                if not char.isprintable(): continue
                self.input_buffer += char
                length = len(self.input_buffer)-1
                sys.stdout.write(f'\x1b[{length if length else -1}D')
                sys.stdout.write(self.color_the_string(self.input_buffer))
                
            sys.stdout.flush()
                
        return self._return(return_color)
    
    def color_the_string(self, string:str) -> str:
        if self.color_dict is None:
            return string
        
        words = string.split(' ')
        
        colord_word = [
            self.color.color(word, self.color_dict.get(word,'none')) 
            for word in words
        ]
        
        return ' '.join(colord_word)


class todo_table:
    def __init__(self) -> None:
        self.padx = 5
        self.app_name = 'CLI app'
        self.heading = None
        self.header_data = None
        self.table_data = None
        
    def get_size(self) -> tuple[int,int]:
        terminal_size = os.get_terminal_size()
        width = terminal_size.columns
        height = terminal_size.lines
        return width, height
    
    def add_data(self, heading = None, header_data = None, table_data = None):
        if heading: self.heading = heading
        if header_data: self.header_data = header_data
        if table_data: self.table_data = table_data
    
    def table(self) -> str:
        w , h = self.get_size()
        padding = 5
        w -= padding*2
        col1,col3,col4 = 5,15,15
        
        return ''.join(
            [
                f"{' '*padding}┌{'─'*(w-2)}┐\n",
                f"{' '*padding}│{' '*self.padx}{self.app_name}{'{:^{}}'.format(self.heading[0],w-len(self.heading[0])-len(self.heading[1])-(self.padx)*2)}{self.heading[1]}{' '*self.padx}│\n",
                f"{' '*padding}├{'─'*col1}┬{'─'*(w-5-col1-col3-col4)}┬{'─'*col3}┬{'─'*col4}┤\n",
                f"{' '*padding}│{'{:^{}}'.format(self.header_data[0],col1)}│  {'{:<{}}'.format(self.header_data[1],w-7-col1-col3-col4)}│{'{:^{}}'.format(self.header_data[2],col3)}│{'{:^{}}'.format(self.header_data[3],col4)}│\n{' '*padding}├{'─'*col1}┼{'─'*(w-5-col1-col3-col4)}┼{'─'*col3}┼{'─'*col4}┤\n" if self.header_data is not None else '',
            ]+[
                f"{' '*padding}│{'{:^{}}'.format(table_data[0],col1)}│  {'{:<{}}'.format(table_data[1],w-7-col1-col3-col4)}│{'{:^{}}'.format(table_data[2],col3)}│{'{:^{}}'.format(table_data[3],col4)}│\n" for table_data in self.table_data
            ]
        )+ f"{' '*padding}└{'─'*col1}┴{'─'*(w-5-col1-col3-col4)}┴{'─'*col3}┴{'─'*col4}┘\n"



FILE_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(FILE_PATH, 'database')
TABLE_PATH = os.path.join(DB_PATH,'tables.json')
SETTING_PATH = os.path.join(DB_PATH,'setting.json')

utils = info()


if __name__ == "__main__":
    new_input = SmartInput()
    new_input.add_color({'hello':'red','add':'yellow','remove':'yellow'})
    some = new_input.input("please type something :) ")
    print(some)