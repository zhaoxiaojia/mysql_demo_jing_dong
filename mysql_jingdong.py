#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time    :2020/4/27 21:01
# @Author  :Coco
# @FileName: mysql_jingdong.py

# @Software: PyCharm
"""
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓ ┏┓
            ┏┛┻━┛┻━┓
            ┃   ☃  ┃
            ┃ ┳┛ ┗┳ ┃
            ┃   ┻   ┃
            ┗━┓   ┏━┛
               ┃     ┗━━┓
               ┃        ┣┓
               ┃　      ┏┛
               ┗┓┓━━┳┓━┛
                 ┃┫  ┃┫
                 ┗┛  ┗┛
"""
from pymysql import connect
import csv

'''
class JD
完成数据库，表，内容等业务

mysql> show tables;
+---------------------+
| Tables_in_jing_dong |
+---------------------+
| customers           |
| goods               |
| goods_brands        |
| goods_cates         |
| order_detial        |
| orders              |
+---------------------+
6 rows in set (0.00 sec)

mysql> desc goods;
+------------+---------------+------+-----+---------+----------------+
| Field      | Type          | Null | Key | Default | Extra          |
+------------+---------------+------+-----+---------+----------------+
| id         | int unsigned  | NO   | PRI | NULL    | auto_increment |
| name       | varchar(140)  | NO   |     | NULL    |                |
| cate_id    | int unsigned  | NO   |     | NULL    |                |
| brand_id   | int unsigned  | NO   |     | NULL    |                |
| price      | decimal(10,3) | NO   |     | 0.000   |                |
| is_show    | bit(1)        | NO   |     | b'1'    |                |
| is_saleoff | bit(1)        | NO   |     | b'0'    |                |
+------------+---------------+------+-----+---------+----------------+
7 rows in set (0.00 sec)

mysql> desc goods_cates;
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int unsigned | NO   | PRI | NULL    | auto_increment |
| name  | varchar(40)  | NO   |     | NULL    |                |
+-------+--------------+------+-----+---------+----------------+
2 rows in set (0.00 sec)

mysql> desc goods_brands;
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int unsigned | NO   | PRI | NULL    | auto_increment |
| name  | varchar(40)  | NO   |     | NULL    |                |
+-------+--------------+------+-----+---------+----------------+
2 rows in set (0.00 sec)

mysql> desc orders;
+-----------------+--------------+------+-----+---------+----------------+
| Field           | Type         | Null | Key | Default | Extra          |
+-----------------+--------------+------+-----+---------+----------------+
| id              | int unsigned | NO   | PRI | NULL    | auto_increment |
| order_date_time | varchar(40)  | YES  |     | NULL    |                |
| customer_id     | int          | NO   |     | NULL    |                |
+-----------------+--------------+------+-----+---------+----------------+
3 rows in set (0.00 sec)

mysql> desc customers;
+---------+--------------+------+-----+---------+----------------+
| Field   | Type         | Null | Key | Default | Extra          |
+---------+--------------+------+-----+---------+----------------+
| id      | int unsigned | NO   | PRI | NULL    | auto_increment |
| name    | varchar(150) | NO   |     | NULL    |                |
| address | varchar(150) | NO   |     | NULL    |                |
| tel     | varchar(11)  | NO   |     | NULL    |                |
| passwd  | varchar(40)  | NO   |     | NULL    |                |
+---------+--------------+------+-----+---------+----------------+

mysql> desc order_detial;
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| id       | int unsigned | NO   | PRI | NULL    | auto_increment |
| order_id | int          | NO   |     | NULL    |                |
| good_id  | int          | NO   |     | NULL    |                |
| quantity | int          | NO   |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+
4 rows in set (0.00 sec)

'''

create_table_goods_sql = '''
    create table if not exists goods(
    id int unsigned primary key auto_increment,
    name varchar(140) not null,
    cate_id int unsigned not null,
    brand_id int unsigned not null,
    price decimal(10,3) not null default 0,
    is_show bit not null default 1,
    is_saleoff bit not null default 0
    )
'''

create_table_goods_cates_sql = '''
    create table if not exists goods_cates(
    id int unsigned primary key auto_increment,
    name varchar(40) not null
    )
'''
create_table_goods_brands_sql = '''
    create table if not exists goods_brands(
    id int unsigned primary key auto_increment,
    name varchar(40) not null
    )
'''
create_table_orders_sql = '''
    create table if not exists orders(
    id int unsigned primary key auto_increment,
    order_date_time varchar(40) not null,
    customer_id int not null
    );
'''
create_table_customers_sql = '''
    create table if not exists customers(
    id int unsigned primary key auto_increment,
    name varchar(150) not null,
    address varchar(150) not null,
    tel int not null,
    passwd varchar(40) not null
    );
'''
create_table_order_detial_sql = '''
    create table if not exists order_detial(
    id int unsigned primary key auto_increment,
    order_id int not null,
    good_id int not null,
    quantity int not null
    );
'''


class JD:

    def __init__(self):
        # 创立数据库连接
        self.conn = connect(host='localhost', port=3306, user='root', password='123', database='jing_dong',
                            charset='utf8')
        # 获取cursor洗对象
        self.cursor = self.conn.cursor()
        # 创立表(如果表不存在)
        self.excuext_sql(create_table_goods_sql)
        self.excuext_sql(create_table_goods_cates_sql)
        self.excuext_sql(create_table_goods_brands_sql)
        self.excuext_sql(create_table_orders_sql)
        self.excuext_sql(create_table_customers_sql)
        self.excuext_sql(create_table_order_detial_sql)
        print('创建完成')
        # 添加数据(如果数据不存在)
        # 判断goods表中是否有数据
        select_goods_sql = '''select * from goods'''
        goods_number = self.cursor.execute(select_goods_sql)
        if goods_number == 0:
            # 添加数据
            self.add_goods_info()
        goods_cates_number = self.cursor.execute('''select * from goods_cates''')
        if goods_cates_number == 0:
            pass
        goods_brands_number = self.cursor.execute('''select * from goods_brands''')
        if goods_brands_number == 0:
            self.excuext_sql(
                '''insert into goods_brands (name) values("华硕"),("联想"),("雷神"),("索尼"),("苹果"),("戴尔"),("宏基"),("惠普"),("ibm")''')
        self.conn.commit()

    def show_goods_info(self):
        '''
        显示所有商品信息
        :return:
        '''
        sql = '''select * from goods'''
        self.cursor.execute(sql)
        for temp in self.cursor.fetchall():
            print(temp)

    def excuext_sql(self, sql):
        self.cursor.execute(sql)

    def __del__(self):
        # 关闭cursor 以及conn
        self.cursor.close()
        self.conn.close()

    def add_goods_info(self):
        # 读取goods_data.csv中的数据并写入数据库
        with open('goods_data.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in list(reader)[1:]:
                print(
                    '''insert into goods value(
                    0,{},{},{},{},default,default
                    )'''.format(row[1].strip(), row[2].strip(),
                                row[3].strip(), row[4].strip()))
                self.excuext_sql(
                    '''insert into goods value(
                    0,{},{},{},{},default,default
                    )'''.format('"' + row[1].strip() + '"',
                                row[2].strip(), row[3].strip(),
                                row[4].strip()))
