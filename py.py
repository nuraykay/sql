import psycopg2


connection = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="123",
            port="5432"
)
        
       

def teachers_table(connection):
 
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                subject VARCHAR(100)
            )
        """)
        connection.commit()
    
def teacher_insert(connection, name, subject):
 
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO teachers (name, subject)
            VALUES (%s, %s)
        """, (name, subject))
        connection.commit()
     
  
def teachers_subject(connection, name):
   
        cursor = connection.cursor()
        cursor.execute("SELECT subject FROM teachers WHERE name = %s", (name,))
        # WHERE name = %s: Эта часть определяет условие для фильтрации строк. 
        # Мы выбираем только те строки, где значение в столбце name равно значению,
        #  которое мы передаем через параметр %s. %s является заполнителем, который будет заменен реальным значением при выполнении запроса.
        subject = cursor.fetchone()
        if subject:
            return subject[0] # если уже были предметы созданы ранее - обнуляем его данные в массиве 
        else:
            return None #если нет то ничего не делаем


def get_teacher_graph(connection):
    
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM teachers")
        teachers = [row[0] for row in cursor.fetchall()]
#teachers = [row[0] for row in cursor.fetchall()]: Создается список teachers,
#  содержащий имена всех преподавателей, полученные из результата предыдущего SQL-запроса.
        
        graph = {}
# graph = {}: Создается пустой словарь graph,
#  который будет представлять собой граф отношений между преподавателями.

        for teacher in teachers:
            graph[teacher] = set()
            cursor.execute("SELECT name FROM teachers WHERE name != %s", (teacher,))
            neighbors = [row[0] for row in cursor.fetchall()]
            graph[teacher].update(neighbors)
        
        return graph
# for teacher in teachers:: Запускается цикл по всем преподавателям из списка teachers.

# graph[teacher] = set(): Для каждого преподавателя создается пустое множество, 
# которое будет представлять собой множество соседей (преподавателей, с которыми у текущего преподавателя есть отношение).

# cursor.execute("SELECT name FROM teachers WHERE name != %s", (teacher,)): Выполняется вложенный SQL-запрос,
#  который выбирает имена всех преподавателей, кроме текущего, с использованием условия name != %s.
#  Здесь %s - это заполнитель для параметра, который будет заменен конкретным значением (именем преподавателя) при выполнении запроса.

# neighbors = [row[0] for row in cursor.fetchall()]: Полученные результаты запроса сохраняются в списке neighbors, 
# содержащем имена преподавателей, являющихся соседями текущего преподавателя.

# graph[teacher].update(neighbors): Метод update добавляет все элементы из списка neighbors 
# в множество соседей текущего преподавателя.

# return graph: В конце функции возвращается словарь graph, представляющий граф отношений между преподавателями,
#  где каждый преподаватель связан с множеством своих соседей.








def dijkstra_algorithm(graph, start_node):
    visited = set()
    queue = [start_node]

    while queue:
        current_node = queue.pop(0)
        if current_node not in visited:
            visited.add(current_node)
            queue.extend(graph[current_node] - visited)

    return start_node in visited


#visited = set(): Создается множество visited для отслеживания посещенных узлов.

# queue = [start_node]: Создается очередь queue с начальным узлом start_node.

# while queue:: Начинается цикл, который будет выполняться, пока очередь не пуста.

# current_node = queue.pop(0): Извлекается первый элемент из очереди. В данном случае, это реализация
#  "обхода в ширину" (BFS), где используется очередь.

# if current_node not in visited:: Проверяется, был ли текущий узел уже посещен. Если нет, то выполняются следующие шаги.

# visited.add(current_node): Текущий узел помечается как посещенный и добавляется в множество visited.

# queue.extend(graph[current_node] - visited): Добавляются все соседи текущего узла, которые еще не были посещены, в конец очереди.

# return start_node in visited: После завершения цикла, возвращается булево значение, 
# показывающее, был ли стартовый узел start_node посещен в результате выполнения алгоритма.

if __name__ == "__main__":
    if connection:
        teachers_table(connection)

        teacher_insert(connection, "Комрон", "subd")
        teacher_insert(connection, "Алмас", "py")
        teacher_insert(connection, "Айжан", "ikt")
        teacher_insert(connection, "Комрон1", "subdd")
        teacher_insert(connection, "Комрон2", "subddd")


        teacher_name = input("Введите имя преподавателя: ")
        graph = get_teacher_graph(connection)
        exists = dijkstra_algorithm(graph, teacher_name)

        if exists:
            subject = teachers_subject(connection, teacher_name)
            print(f"Преподаватель {teacher_name} преподает предмет: {subject}")
        else:
            print(f"Преподаватель {teacher_name} не найден.")

        connection.close()
