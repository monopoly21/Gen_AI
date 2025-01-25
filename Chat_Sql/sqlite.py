import sqlite3

##Connect to sqllite
connection=sqlite3.connect('student.db')

#create a cursor to insert,delete,update,select data
cursor=connection.cursor()


table_info="""
    create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
    SECTION VARCHAR(26),MARKS INT)

"""
cursor.execute(table_info)

cursor.execute('''insert Into Student values('Raj','Data science','A',90)''')
cursor.execute('''insert Into Student values('Raja','Data ','B',80)''')
cursor.execute('''insert Into Student values('Rani','AI','C',40)''')
cursor.execute('''insert Into Student values('Rajesh','ML','D',70)''')

print("The inserted records are")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

connection.commit()
connection.close()