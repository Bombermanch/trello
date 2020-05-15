import requests
import sys
import json

  
# Данные авторизации в API Trello

def autorization():
	fp = open("auth_params.json")
	# загружаем JSON документ с помощью функции load
	user_data = json.load(fp)	
	return user_data 
auth_params = autorization()
  
# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.  
base_url = "https://api.trello.com/1/{}"  

board_id = "Y40v3An1"

def read():      
    # Получим данные всех колонок на доске:  
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()  
  
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:  
    for column in column_data:
        
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()  
        print(column['name'] + " - ({})".format(len(task_data)))  
  
        if not task_data:  
            print('\t' + 'Нет задач!')  
            continue  
        for task in task_data:  
            print('\t' + task['name'])
             
def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

      
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:      
    	if column['name'] == column_name:      
            # Создадим задачу с именем _name_ в найденной колонке      
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            print("Создано задание '{}' в колонке: {}".format(name, column['name'])) 
            break   
def create_column(column_name):
    return requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': board_id, **auth_params}).json()
    print("Создана новая колонка: {}".format(column_name))

def move(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_id = None    
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name:    
                task_id = task['id']                   
                break    
        if task_id:    
            break    
       
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params}) 
            print("Задание '{}' перемещено в колонку: {}".format(task['name'], column_name))    
            break



if __name__ == "__main__":
	try:
		if len(sys.argv) <= 2:
			read()
		elif sys.argv[1] == 'create':
			create(sys.argv[2], sys.argv[3])
		elif sys.argv[1] == 'create_column':
			create_column(sys.argv[2])
		elif sys.argv[1] == 'move':
			move(sys.argv[2], sys.argv[3])
	except ValueError:
		print("\n\n\tНеверный ключ или токен.\n")