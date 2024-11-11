import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
import os

load_dotenv()

ssh_host1 = os.getenv('SSH_HOST1')
ssh_port1 = int(os.getenv('SSH_PORT1'))
ssh_user1 = os.getenv('SSH_USER1')
ssh_key1 = os.getenv('SSH_KEY1')

db_host1 = os.getenv('DB_HOST1')
db_port1 = int(os.getenv('DB_PORT1'))
db_name1 = os.getenv('DB_NAME1')
db_user1 = os.getenv('DB_USER1')
db_password1 = os.getenv('DB_PASSWORD1')

ssh_host2 = os.getenv('SSH_HOST2')
ssh_port2 = int(os.getenv('SSH_PORT2'))
ssh_user2 = os.getenv('SSH_USER2')
ssh_key2 = os.getenv('SSH_KEY2')

db_host2 = os.getenv('DB_HOST2')
db_port2 = int(os.getenv('DB_PORT2'))
db_name2 = os.getenv('DB_NAME2')
db_user2 = os.getenv('DB_USER2')
db_password2 = os.getenv('DB_PASSWORD2')

def create_db_connection(connection_details):
    ssh_host, ssh_port, ssh_user, ssh_key, db_host, db_port, db_name, db_user, db_password = connection_details
    
    tunnel = SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_pkey=ssh_key,
        remote_bind_address=(db_host, db_port),
        local_bind_address=('localhost', 6543)
    )
    
    tunnel.start()
    
    conn = psycopg2.connect(
        host='localhost',
        port=tunnel.local_bind_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    
    return tunnel, conn

def close_db_connection(tunnel, conn):
    if conn:
        conn.close()
    if tunnel:
        tunnel.stop()

def get_connection_details(db_number):
    if db_number == 1:
        return (ssh_host1, ssh_port1, ssh_user1, ssh_key1, db_host1, db_port1, db_name1, db_user1, db_password1)
    elif db_number == 2:
        return (ssh_host2, ssh_port2, ssh_user2, ssh_key2, db_host2, db_port2, db_name2, db_user2, db_password2)
    else:
        raise ValueError("Invalid database number")
