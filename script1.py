# Исходные данные для заполнения таблиц
import csv
import psycopg2

#cur.execute("SET search_path TO student_schema_name;")

with open('customers_data.csv', newline='') as file:
    customers_data = [row for row in csv.reader(file) if 'customer_id' not in row]

with open('employees_data.csv', newline='') as file:
    employees_data = [row for row in csv.reader(file) if 'first_name' not in row]

with open('orders_data.csv', newline='') as file:
    orders_data = [row for row in csv.reader(file) if 'order_id' not in row]

# Импортируйте библиотеку psycopg2

# Создайте подключение к базе данных
conn = psycopg2.connect(host="localhost", port=5432, database='analysis', user='postgres', password='12345')

# Открытие курсора
cur = conn.cursor()

# Не меняйте и не удаляйте эти строки - они нужны для проверки
cur.execute("create schema if not exists itresume17832;")
cur.execute("SET search_path TO itresume17832;")
cur.execute("DROP TABLE IF EXISTS orders")
cur.execute("DROP TABLE IF EXISTS customers")
cur.execute("DROP TABLE IF EXISTS employees")

# Ниже напишите код запросов для создания таблиц
cur.execute("CREATE TABLE customers("
            "customer_id varchar(5) primary key, "
            "company_name varchar(100) not null, "
            "contact_name varchar(100) not null"
            ")")
cur.execute("CREATE TABLE employees("
            "employee_id int primary key, "
            "first_name varchar(25) not null, "
            "last_name varchar(35) not null, "
            "title varchar(100) not null, "
            "birth_date date not null, "
            "notes text)")
cur.execute("create table orders("
            "order_id int primary key, "
            "customer_id varchar(5) references customers(customer_id) not null, "
            "employee_id int references employees(employee_id) not null, "
            "order_date date not null, "
            "ship_city varchar(100) not null)")

# Зафиксируйте изменения в базе данных
conn.commit()

# Теперь приступаем к операциям вставок данных
# Запустите цикл по списку customers_data и выполните запрос формата
# INSERT INTO itresume3270.table (column1, column2, ...) VALUES (%s, %s, ...) returning ", data)
# В конце каждого INSERT-запроса обязательно должен быть оператор returning
title = "customer_id, company_name, contact_name"
for item in customers_data:
    query = f"insert into customers ({title}) values ({', '.join(['%s'] * len(item))})"
    cur.execute(query, item)
cur.execute("SELECT * FROM customers ORDER BY customer_id DESC LIMIT 1")

# Не меняйте и не удаляйте эти строки - они нужны для проверки
conn.commit()
res_customers = cur.fetchall()

    # Запустите цикл по списку employees_data и выполните запрос формата
    # INSERT INTO table (column1, column2, ...) VALUES (%s, %s, ...) returning *", data)
    # В конце каждого INSERT-запроса обязательно должен быть оператор returning *
title = "employee_id, first_name, last_name, title, birth_date, notes"
index_ = 1
for item in employees_data:
    query = f"insert into employees ({title}) values ({index_}, {', '.join(['%s'] * len(item))})"
    cur.execute(query, item)
    index_ += 1
cur.execute("SELECT * FROM employees ORDER BY employee_id DESC LIMIT 1")
# Не меняйте и не удаляйте эти строки - они нужны для проверки
conn.commit()
res_employees = cur.fetchall()

    # Запустите цикл по списку orders_data и выполните запрос формата
    # INSERT INTO table (column1, column2, ...) VALUES (%s, %s, ...) returning *", data)
    # В конце каждого INSERT-запроса обязательно должен быть оператор returning *
title = "order_id, customer_id, employee_id, order_date, ship_city"
for item in orders_data:
    query = f"insert into orders ({title}) values ({', '.join(['%s'] * len(item))})"
    cur.execute(query, item)

cur.execute("SELECT * FROM orders ORDER BY order_id DESC LIMIT 1")
# Не меняйте и не удаляйте эти строки - они нужны для проверки
conn.commit()
res_orders = cur.fetchall()

# Закрытие курсора
cur.close()

# Закрытие соединения
conn.close()
