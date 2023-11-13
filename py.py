import psycopg2




def binarySearch(unames, x, low, high):

    while low <= high:
        mid = low + (high - low)//2

        if unames[mid] == x:
            return mid

        elif unames[mid] < x:
            low = mid + 1

        else:
            high = mid - 1

    return -1

conn = psycopg2.connect(
    host='localhost',
    database='SUBD',
    user='postgres',
    password='123',
    port='5432'
)

cur = conn.cursor()
cur.execute("SELECT name FROM fruits LIMIT 5;")
unames = [r[0] for r in cur.fetchall()]

uname = input("Enter your login (name of the fruit): ")
found = binarySearch(unames, uname)

if found:
    print("You have it in the list.")
else:
    print("You do not have it in the list.")

cur.close()
conn.close()
