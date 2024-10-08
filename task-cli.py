from utils import *
from database import *

demo_data = [
    'fnish the task number1',
    'give gift to kavya say about ur feelings',
    'think about ur works',
    'finish the projects and ideas',
    'finish something new',
    'i guess thats enfugh',
    'fnish the task number1',
    'give gift to kavya say about ur feelings',
    'think about ur works',
    'finish the projects and ideas',
    'finish something new',
    'i guess thats enfugh',
    'fnish the task number12',
    'give gift to kavya say about ur feelings2',
    'think about ur works2',
    'finish the projects and ideas2',
    'finish something new2',
    'i guess thats enfugh2'
]

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

def demo_look():
    color = CILcolor()
    smart_input = SmartInput()
    h = todo_table()
    h.add_data(
        heading = ('[table-1]','4/30'),
        table_data = [
            ['1','this is the first task', 'done', '23 may'],
            ['2','kiss samar and tell her about ur feelings', 'nope', '23 may'],
            ['3','become rich and marry a girl name samar (100000000)', 'nope', '29 may'],
            ['4',"finsh some sexy projects",'none', 'none']
        ]
    )
    print(h.table())
    result = smart_input.input(color.color('cyan','          >>> '))
    print(f'result info {result} + extra info width:')
    




if __name__ == '__main__':
    pass




















































































# tasks = ['hello world task no task']

# def add_task(task_desription):
#     tasks.append(task_desription)
#     print('task added to list: ',task_desription)
    
# def remove_task(index):
#     try :
#         task = tasks.pop(index)
#     except:
#         task = 'error to remove'
    
#     print('task removed status : ', task)

# def list_all_task():
#     for num , task in enumerate(tasks):
#         print(f'[{num}]: {task}')
        
# def show(event):
#     pass
        

# def start():
#     while True:
#         system('cls')
#         print('-----------welcome to demo verstion--------------')
#         list_all_task()
#         print("-------------------------------------------------")
#         print('here are the command (add_task, remove_task)')
#         someh = input("enter ur quary: ").split(' ')
#         try:
#             if someh[0] == 'add_task':
#                 add_task(someh[1])
#             elif someh[0] == 'remove_task':
#                 remove_task(int(someh[1]))
#             elif someh[0] == 'end':
#                 break
#         except:
#             print('there is some error')
#         _ = input('tap enter to continue.............')
        

# def main():
#     parser = argparse.ArgumentParser(description='task manager')
#     subparsee = parser.add_subparsers(dest="command",required=True)
    
#     parser_add = subparsee.add_parser('add_task', help="add a new task")
#     parser_add.add_argument('description', type=str, help= 'task description')
    
#     parese_remove = subparsee.add_parser("remove_task", help="remove a tasl by its number")
#     parese_remove.add_argument("task_number", type=int, help = "the number of the task to remove")
    
#     parse_list= subparsee.add_parser("list_tasks", help="list all current tasks")
#     parser_begin = subparsee.add_parser("start", help="start the cml application")
    
#     args = parser.parse_args()
    
#     if args.command == 'add_task':
#         add_task(args.description)
        
#     elif args.command == 'remove_task':
#         remove_task(args.task_number)
    
#     elif args.command == 'list_tasks':
#         list_all_task()
        
#     elif args.command == 'start':
#         start()
    
#     else:
#         parser.print_help()

# if __name__ == "__main__":
#     main()


