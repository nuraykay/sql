import psycopg2
import csv




conn = psycopg2.connect(host = 'localhost', database = 'Students', user = 'postgres', password='123', port = '5432')

cursor = conn.cursor()

cursor.execute('SELECT * FROM flights limit 10')

n = cursor.fetchall()
for i in n:
    print(i)

csvfile = open('output1.csv', 'w')
csvwriter = csv.writer(csvfile)

for row in n:
    csvwriter.writerow(row)
