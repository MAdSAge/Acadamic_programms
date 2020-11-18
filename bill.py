
# testing code block
import sqlite3 as dblite
import matplotlib


def show_table_columns(database:str,table:str):
    conn = dblite.connect(database)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info("+table+")")
    list=cur.fetchall()
    column=[]
    for i in list:
        column.append(i[1])
    return column

# adding tasks function
def add_a_task(dbname:str,are_you_cretaing_table=False):
    conn = dblite.connect(dbname)
    cur= conn.cursor()
    # creat a new table if first time
    if(are_you_cretaing_table==True):
        creta_tabele=input("enter the table creation statement")
        cur.execute(creta_tabele)
    # select a table from given list
    cur.execute("SELECT * FROM sqlite_master where type='table';")
    tables = cur.fetchall()
    for i in tables:
        print(i[1])
    selected_table = input("enter name of a table")
    columns = show_table_columns(dbname,selected_table)
    #building the input query dor sql
    number_of_q= 0
    for i in columns:
        number_of_q = number_of_q+1
    string1=""
    for i in columns:
        string1=string1+"(?),"
    string1 = string1[:-1]
    print(string1)
    while True:
        columns = show_table_columns(dbname,selected_table)
        iterman=[]
        empty="["
        for i in columns:
            wow = input("enter "+i)
            iterman.append(wow)
            empty=empty+"'', "
        empty=empty[:-2]
        empty=empty+"]"
        print(str(iterman))      
        if (str(iterman) != empty):     
            cur.execute("INSERT INTO "+selected_table+" VALUES ("+string1+")",iterman)
            conn.commit()
            iterman.clear()
        else:
            break
    cur.close()    
    conn.close()
    print("added vales")

# to see all tasks in table
def see_tasks(dbname:str,table_name=None,condition=None,mode="print"):
    
    conn = dblite.connect(dbname)
    cur = conn.cursor()    
    tables_list = cur.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
    for table in tables_list:
        print(table[0])
    if(table_name == None):
        table_name = input("enter name of a table")
    # x= show_table_columns(dbname,table_name)
    # print(x)        
    if(condition != None):
        cur.execute("select * from "+table_name+" where "+condition)
    else:
        cur.execute("select * from "+table_name)
    table = cur.fetchall()
    cur.close()
    conn.close()
    if(mode=="print"):
        print("Tasks in {} are :".format(table_name))
        print()
        for i in table:
            print("Start date: \t{}\tTarget Date:\t{}".format(i[0],i[3]))
            print("task: \t\t{}".format(i[1]))
            print("Description: \t{}".format(i[2]))
            print("Status:\t\t{}".format(i[4]))
            print()

    else:
        return table

# to deleted unwanted tasks
def del_unwanted_tasks(dbname:str,all:bool):
    conn = dblite.connect(dbname)
    cur = conn.cursor()
    tables_list = cur.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
    for table in tables_list:
        print(table)
    selected_table = input("enter name of a table")
    if(all==True):
        c = show_table_columns(dbname,selected_table)
        criteria = input("select from following :\n "+str(c))
        cur.execute("DELETE from "+selected_table+" WHERE "+criteria+" is not null")
        conn.commit()
    else:
        c = show_table_columns(dbname,selected_table)
        criteria = input("select from following :\n "+str(c)+" ")
        cur.execute("DELETE from "+selected_table+" where "+criteria)
        conn.commit()
    cur.close()
    conn.close()
    
# to update the details in tasks
def update_a_task(dbname:str,table_name=None,condition=None,variable="status"):
    see_tasks(dbname=dbname,table_name=table_name,condition=condition)
    conn = dblite.connect(dbname)
    cur = conn.cursor()
    if(table_name == None):
        table_name = input("enter name of a table")
    if(variable==None):
        variable=input("Select a task: \n"+str(show_table_columns(dbname,table_name)))
    while True:
        row_id=input("task stats supdate : ")
        u_col=input("enter the update: ")
        if(row_id==''):
            break
        cur.execute("UPDATE {} SET {}='{}' WHERE task_name='{}'".format(table_name,variable,u_col,row_id))
        conn.commit()
        print("updated "+row_id+"staus to "+u_col)
    cur.close()
    conn.close()

# plot progress of the achivements in a graph
def plot_progress(dbname,table_name=None,condition=None):
    scores={"NO":1,"YES":0,"FAIL":-1}
    tabel=see_tasks(dbname,table_name,condition,mode="god")
    data=[]
    for row in tabel:
        data.append(row[4])
    print(data)



