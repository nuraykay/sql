import psycopg2
from psycopg2 import sql

connection = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="123",
    port = '5432'
)
cursor = connection.cursor()

create_table_query = '''
    CREATE TABLE Graph (
        StartVertex VARCHAR(50),
        EndVertex VARCHAR(50),
        Weight DECIMAL(10, 2)
    );
'''
cursor.execute('''
    CREATE TABLE Graph (
        StartVertex VARCHAR(50),
        EndVertex VARCHAR(50),
        Weight DECIMAL(10, 2)
    );
''')
connection.commit()

insert_data_query = sql.SQL('''
    INSERT INTO Graph (StartVertex, EndVertex, Weight) VALUES
        {}, {}, {},
        {}, {}, {},
        {}, {}, {},
        {}, {}, {};
''').format(
    sql.SQL("('A', 'B', 1)"),
    sql.SQL("('A', 'C', 4)"),
    sql.SQL("('B', 'A', 1)"),
    sql.SQL("('B', 'C', 2)"),
    sql.SQL("('B', 'D', 5)"),
    sql.SQL("('C', 'A', 4)"),
    sql.SQL("('C', 'B', 2)"),
    sql.SQL("('C', 'D', 1)"),
    sql.SQL("('D', 'B', 5)"),
    sql.SQL("('D', 'C', 1)")
)
cursor.execute(insert_data_query)
connection.commit()

cursor.close()
connection.close()

import heapq

def dijkstra_pg(graph_table, start):
    distances = {vertex: float('infinity') for vertex in graph_table}
    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        cursor.execute('''
            SELECT "EndVertex", "Weight"
            FROM "Graph"
            WHERE "StartVertex" = %s
        ''', (current_vertex,))
        neighbors = cursor.fetchall()

        for neighbor, weight in neighbors:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="123"
)
cursor = connection.cursor()

graph_table = {'A': {}, 'B': {}, 'C': {}, 'D': {}}
result = dijkstra_pg(graph_table, 'A')
print(f"Shortest distances from A: {result}")

cursor.close()
connection.close()

