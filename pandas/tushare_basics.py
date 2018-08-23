#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tushare as ts
from sqlite3 import dbapi2 as sqlite
from sqlalchemy import create_engine, Column, String, Integer, BigInteger, Float
from sqlalchemy import and_, or_

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# 数据库连接规范参加：http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html
# engine = create_engine('mysql://user:passwd@127.0.0.1/db_name?charset=utf8')
engine = create_engine('sqlite+pysqlite:///d:/stockA.db', module=sqlite)

# # A股基本面信息
# df = ts.get_stock_basics()

# #存入数据库
# df.to_sql('SA_basics',engine)

#追加数据到现有表
#df.to_sql('tick_data',engine,if_exists='append')


# 创建对象的基类:
Base = declarative_base()


# 定义SA_Basics对象:
# code,代码
# name,名称
# industry,所属行业
# area,地区
# pe,市盈率
# outstanding,流通股本(亿)
# totals,总股本(亿)
# totalAssets,总资产(万)
# liquidAssets,流动资产
# fixedAssets,固定资产
# reserved,公积金
# reservedPerShare,每股公积金
# esp,每股收益
# bvps,每股净资
# pb,市净率
# timeToMarket,上市日期
# undp,未分利润
# perundp, 每股未分配
# rev,收入同比(%)
# profit,利润同比(%)
# gpr,毛利率(%)
# npr,净利润率(%)
# holders,股东人数
class Basics(Base):
    # 表的名字:
    __tablename__ = 'SA_basics'

    # 表的结构:
    code = Column(String(10), primary_key=True)
    name = Column(String(10))
    industry = Column(String(10))
    area = Column(String(10))
    pe = Column(Float)
    outstanding = Column(Float)
    totals = Column(Float)
    totalAssets = Column(Float)
    liquidAssets = Column(Float)
    fixedAssets = Column(Float)
    reserved = Column(Float)
    reservedPerShare = Column(Float)
    esp = Column(Float)
    bvps = Column(Float)
    pb = Column(Float)
    timeToMarket = Column(BigInteger)
    undp = Column(Float)
    perundp = Column(Float)
    rev = Column(Float)
    profit = Column(Float)
    gpr = Column(Float)
    npr = Column(Float)
    holders = Column(Integer)

    def __str__(self):
    	return "%s %s:\t gpr=%.2f%%\t npr=%.2f%%" % (self.code, self.name, self.gpr, self.npr)


def query_basics_by_indudsty(intype):
	# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
	session = DBSession()
	sas = session.query(Basics).filter(Basics.industry==intype).all()
	session.close()

	print('count: %d' % len(sas))
	for sa in sas:
		print(sa)




# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

query_basics_by_indudsty("白酒")