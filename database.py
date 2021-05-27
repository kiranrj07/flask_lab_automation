import sqlite3
conn = None
def connection_open():
    return sqlite3.connect('lab_database.db')

def connection_close():
    conn.close()

def login_data():
    conn = connection_open()
    connection_close()


def server_detail(server_list):
    server_detais={}
    conn = connection_open()
    for server in server_list:
        cursor = conn.execute("select * from server_details where name =?",(server,))
        i=0
        server_data = []
        for row in cursor:
            server_data.append(row[0])
            server_data.append(row[1])
            server_data.append(row[2])
            server_data.append(row[3])
            #i += 1
        server_detais[server]=server_data

    conn.close()
    return server_detais