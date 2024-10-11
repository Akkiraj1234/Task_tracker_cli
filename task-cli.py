from utils import *
from script import show

class formater:
    def json_format(self, data:dict):
        for table, values in data.items():
            print(f"---------{table}---------------")
            # Get the longest key for proper formatting alignment
            max_key_len = max(len(key) for key in values.keys())
            
            for key, value in values.items():
                print(f"{key.ljust(max_key_len)}: {value}")
            print()
    def another(self):
        pass



def call_syntax(script) -> None:
    pass


def main_loop():
    data = show(None,table)
    format.json_format(data)

if __name__ == "__main__":
    format = formater()
    main_loop()































# demo_data = [
#     'fnish the task number1',
#     'give gift to kavya say about ur feelings',
#     'think about ur works',
#     'finish the projects and ideas',
#     'finish something new',
#     'i guess thats enfugh',
#     'fnish the task number1',
#     'give gift to kavya say about ur feelings',
#     'think about ur works',
#     'finish the projects and ideas',
#     'finish something new',
#     'i guess thats enfugh',
#     'fnish the task number12',
#     'give gift to kavya say about ur feelings2',
#     'think about ur works2',
#     'finish the projects and ideas2',
#     'finish something new2',
#     'i guess thats enfugh2'
# ]

# class todo_table:
#     def __init__(self) -> None:
#         self.padx = 5
#         self.app_name = 'CLI app'
#         self.heading = None
#         self.header_data = None
#         self.table_data = None
        
#     def get_size(self) -> tuple[int,int]:
#         terminal_size = os.get_terminal_size()
#         width = terminal_size.columns
#         height = terminal_size.lines
#         return width, height
    
#     def add_data(self, heading = None, header_data = None, table_data = None):
#         if heading: self.heading = heading
#         if header_data: self.header_data = header_data
#         if table_data: self.table_data = table_data
    
#     def table(self) -> str:
#         w , h = self.get_size()
#         padding = 5
#         w -= padding*2
#         col1,col3,col4 = 5,15,15
        
#         return ''.join(
#             [
#                 f"{' '*padding}┌{'─'*(w-2)}┐\n",
#                 f"{' '*padding}│{' '*self.padx}{self.app_name}{'{:^{}}'.format(self.heading[0],w-len(self.heading[0])-len(self.heading[1])-(self.padx)*2)}{self.heading[1]}{' '*self.padx}│\n",
#                 f"{' '*padding}├{'─'*col1}┬{'─'*(w-5-col1-col3-col4)}┬{'─'*col3}┬{'─'*col4}┤\n",
#                 f"{' '*padding}│{'{:^{}}'.format(self.header_data[0],col1)}│  {'{:<{}}'.format(self.header_data[1],w-7-col1-col3-col4)}│{'{:^{}}'.format(self.header_data[2],col3)}│{'{:^{}}'.format(self.header_data[3],col4)}│\n{' '*padding}├{'─'*col1}┼{'─'*(w-5-col1-col3-col4)}┼{'─'*col3}┼{'─'*col4}┤\n" if self.header_data is not None else '',
#             ]+[
#                 f"{' '*padding}│{'{:^{}}'.format(table_data[0],col1)}│  {'{:<{}}'.format(table_data[1],w-7-col1-col3-col4)}│{'{:^{}}'.format(table_data[2],col3)}│{'{:^{}}'.format(table_data[3],col4)}│\n" for table_data in self.table_data
#             ]
#         )+ f"{' '*padding}└{'─'*col1}┴{'─'*(w-5-col1-col3-col4)}┴{'─'*col3}┴{'─'*col4}┘\n"



# def main():
#     parser = argparse.ArgumentParser(description="anything")
    
#     subparser = parser.add_subparsers(dest="command",required=True)
    
#     add_parser = subparser.add_parser("add", help="add a task or a table")
#     add_parser.add_argument('name',type=str,help = 'The name of the task or table to add.')
#     add_parser.add_argument('--object', choices=['Task', 'Table'], default='Task', help='Specify if adding a Task or Table.')
#     add_parser.add_argument('--inside', type=str, default=setting.defult_table, help='The table inside which to add the task.')
#     add_parser.add_argument('--mark', choices=['done', 'to-do', 'progress'], default='to-do', help='The mark status of the task.')
    
    
#     args = parser.parse_args()
    
#     if args.command.lower() == 'add':
#         object_ = task if args.object.lower() == 'task' else table
#         add(args.name, object=object_, table=args.inside, mark=args.mark)
    
    



# def demo_look():
#     color = CILcolor()
#     smart_input = SmartInput()
#     h = todo_table()
#     h.add_data(
#         heading = ('[table-1]','4/30'),
#         table_data = [
#             ['1','this is the first task', 'done', '23 may'],
#             ['2','kiss samar and tell her about ur feelings', 'nope', '23 may'],
#             ['3','become rich and marry a girl name samar (100000000)', 'nope', '29 may'],
#             ['4',"finsh some sexy projects",'none', 'none']
#         ],
#         header_data=["num","tasks","progress","date"]
#     )
#     print(h.table())
#     result = smart_input.input(color.color('cyan','          >>> '))
#     print(f'result info {result} + extra info width:')
    
# if __name__ == '__main__':
#     # demo_look()
#     main()