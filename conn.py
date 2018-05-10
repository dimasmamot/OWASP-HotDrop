import pymysql.cursors

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='9L1reyib',
    db='hotdrop',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)