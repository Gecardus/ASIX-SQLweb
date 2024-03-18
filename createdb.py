import sqlite3
import hashlib
import uuid
from cryptography.fernet import Fernet
conn=sqlite3.connect("store.db")

cur=conn.cursor()
key=b'-J0EgKZvTK2JT44tLtaxg5t6T3j_O9KRyornUaxjJws='
cypher_suite=Fernet(key)
#tabla users
cur.execute("CREATE TABLE IF NOT EXISTS users (id TEXT, username TEXT, password TEXT,adress TEXT,rol INTEGER)")
conn.commit()
users=[
    (str(uuid.uuid4()),"admin",hashlib.sha256(b"asix2023").hexdigest(),cypher_suite.encrypt(b"Rambla Catalunya 82 bajos"),1),
    (str(uuid.uuid4()),"carlos",hashlib.sha256(b"12345").hexdigest(),cypher_suite.encrypt(b"Carretera de Sants 12 3o 1a"),2),
    (str(uuid.uuid4()),"julia", hashlib.sha256(b"pass6789").hexdigest(), cypher_suite.encrypt(b"Avenida Diagonal 401 2o 2a"),2),
    (str(uuid.uuid4()),"marc", hashlib.sha256(b"marc2024").hexdigest(), cypher_suite.encrypt(b"Gran Via 555 5o 3a"),2),
    (str(uuid.uuid4()),"lucia", hashlib.sha256(b"mypassword").hexdigest(), cypher_suite.encrypt(b"Passeig de Gracia 60 1o 1a"),2),
]
for e in users:
    cur.execute("INSERT INTO users (id,username,password,adress,rol) VALUES (?,?,?,?,?)",e)
conn.commit()

#tabla products
cur.execute("CREATE TABLE IF NOT EXISTS products (name TEXT,price REAL,image TEXT)")
conn.commit()
products=[
    ("ASUS E410MA",249,"https://m.media-amazon.com/images/I/51GYgS4f+GL._AC_UL640_FMwebp_QL65_.jpg"),
    ("WOZIFAN Ordenador Portátil Win11 14'' ",212.49,"https://m.media-amazon.com/images/I/71nCiLpqLqL._AC_UL640_FMwebp_QL65_.jpg"),
    ("HP 15-fd0000ns ",329.99,"https://m.media-amazon.com/images/I/91woduXUkRL._AC_UL640_FMwebp_QL65_.jpg"),
    ("ACEMAGIC Ordenador Portátil Intel 12th Alder Lake",322.92,"https://m.media-amazon.com/images/I/714vs7F41IL._AC_UL640_FMwebp_QL65_.jpg"),
    ("ASUS VivoBook 14 ",699,"https://m.media-amazon.com/images/I/71wTuQ2njfL._AC_UL640_FMwebp_QL65_.jpg"),
    ("Primux Ordenador Portátil Ioxbook 1406F ",149,"https://m.media-amazon.com/images/I/71YC3AEhJjL._AC_UL640_FMwebp_QL65_.jpg"),
    ("ASUS Chromebook CX1400CKA-EK0138 ",279,"https://m.media-amazon.com/images/I/61nfaSxWTLL._AC_UL640_FMwebp_QL65_.jpg"),
    ("HP ELITEBOOK 840 G3 INTEL CORE I5-6200U 6ª GEN 2.3GHZ",259,"https://m.media-amazon.com/images/I/71nVtdbtJiS._AC_UL640_FMwebp_QL65_.jpg"),
   
]
for e in products:
    cur.execute("INSERT INTO products (name,price,image) VALUES (?,?,?)",e)
conn.commit()


#tabla purchases
cur.execute("CREATE TABLE IF NOT EXISTS purchases (username_id INTEGER, product_id INTEGER,amount INTEGER)")
conn.commit()
users=[
    (1,5,1),
    (2,1,1),
    (2,2,1),
    (2,3,1),
    (2,4,1),
    (2,5,1),
    (3,1,1),
    (3,5,1),
    (4,4,1),
    (4,2,1),
    (5,8,2),
    (5,9,2),
    (5,3,2),
    (5,2,2),
    (5,1,2), 
]
for e in users:
    cur.execute("INSERT INTO purchases (username_id,product_id,amount) VALUES (?,?,?)",e)
conn.commit()

cur.close()
conn.close()

print("DB created")