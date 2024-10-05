from utils import *

from database import *






















































































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


