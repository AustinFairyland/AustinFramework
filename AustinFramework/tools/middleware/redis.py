# coding: utf8
""" 
@File: redis.py
@Editor: PyCharm
@Author: Austin (From Chengdu.China) https://fairy.host
@HomePage: https://github.com/AustinFairyland
@OperatingSystem: Windows 11 Professional Workstation 23H2 Canary Channel
@CreatedTime: 2023-10-12
"""
from __future__ import annotations

import os
import sys
import warnings
import platform
import asyncio

sys.dont_write_bytecode = True
warnings.filterwarnings('ignore')
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import time
import random

from redis import ConnectionPool
from redis import Redis
from rediscluster import RedisCluster
from rediscluster.connection import ClusterConnectionPool

# from modules.journals import JournalsModuleClass
from conf import ConfigClass


class RedisStandaloneToolsClass:
    """ Redis 单节点工具类"""

    def __init__(self):
        # JournalsModuleClass.debug('初始化类：{}'.format(self.__class__.__name__))
        try:
            self.__redis_config: dict = ConfigClass.config.get('middleware').get('redis').get('standalone')
        except Exception as error:
            # JournalsModuleClass.exception(error)
            sys.exit(1)

    @property
    def __redis_connect(self):
        """
        Redis 连接
        :return: Redis Connect Object Redis 连接对象
        """
        try:
            __host = self.__redis_config.get('host')
            __port = self.__redis_config.get('port')
            __password = self.__redis_config.get('password')
            __db = self.__redis_config.get('db')
            # JournalsModuleClass.debug('Redis 数据源：Redis Standalone')
            # JournalsModuleClass.debug('Redis IP：{}'.format(__host))
            # JournalsModuleClass.debug('Redis 端口：{}'.format(__port))
            # JournalsModuleClass.debug('Redis 数据库：{}'.format(__db))
            pool = ConnectionPool(
                host=__host,
                port=__port,
                password=__password,
                db=__db,
                decode_responses=True,
                max_connections=10
            )
            conn = Redis(connection_pool=pool)
            # JournalsModuleClass.debug('Redis 服务器连接成功')
            return conn
        except Exception as error:
            # JournalsModuleClass.error('Redis 服务器连接失败')
            # JournalsModuleClass.exception(error)
            sys.exit(1)

    def redis_set(self, k, v):
        """
        Redis 写入数据
        :param k: 键
        :param v: 值
        :return: Boolean
        """
        try:
            conn = self.__redis_connect
            conn.set(k, v)
            # JournalsModuleClass.debug('Redis 写入数据： key：{}， value：{}'.format(k, v))
            return True
        except Exception as error:
            # JournalsModuleClass.exception(error)
            pass
        finally:
            conn.connection_pool.disconnect()

    def redis_get(self, k):
        """
        Redis 根据键获取值
        :param k: key
        :return: 值
        """
        try:
            conn = self.__redis_connect
            v = conn.get(k)
            # JournalsModuleClass.debug('Redis 获取数据成功： key：{}， value：{}'.format(k, v))
            return v
        except Exception as error:
            # JournalsModuleClass.debug('Redis 获取数据失败： key：{}'.format(k))
            # JournalsModuleClass.exception(error)
            pass
        finally:
            conn.connection_pool.disconnect()


class RedisClusterToolsClass:
    """ Redis 集群工具类 """

    def __init__(self):
        # JournalsModuleClass.debug('初始化类：{}'.format(self.__class__.__name__))
        try:
            self.__redis_config: list = ConfigClass.config.get('middleware').get('redis').get('cluster')
        except Exception as error:
            # JournalsModuleClass.exception(error)
            pass

    @property
    def __redis_cluster_connect(self):
        try:
            redis_cluster_confg = ConfigClass.config.get('middleware').get('redis').get('cluster')
            startup_nodes = []
            __password_map = {}
            for standalone_confg in redis_cluster_confg:
                standalone_confg: dict
                __host = standalone_confg.get('host')
                __port = standalone_confg.get('port')
                __password = standalone_confg.get('password')
                startup_nodes.append({'host': __host, 'port': __port})
                __password_map['{}:{}'.format(__host, __port)] = __password
            # JournalsModuleClass.debug('Redis 连接池数据源：{}'.format(startup_nodes))
            pool = ClusterConnectionPool(
                startup_nodes=startup_nodes,
                password_map=__password_map,
                max_connections=10,
                decode_responses=True
            )
            conn = RedisCluster(connection_pool=pool)
            # JournalsModuleClass.debug('Redis Cluster 连接成功')
            return conn
        except Exception as error:
            # JournalsModuleClass.error('Redis Cluster 连接失败')
            # JournalsModuleClass.exception(error)
            pass
            
    def redis_get(self, k):
        try:
            conn = self.__redis_cluster_connect
            value = conn.get(k)
            # JournalsModuleClass.debug('Redis 获取数据成功：key：{}，value：{}'.format(k, value))
            return value
        except Exception as error:
            # JournalsModuleClass.exception(error)
            pass
        finally:
            conn.connection_pool.disconnect()