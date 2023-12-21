# coding: utf8
"""
@ File: tools.py
@ Editor: PyCharm
@ Author: Austin (From Chengdu.China) https://fairy.host
@ HomePage: https://github.com/AustinFairyland
@ OS: Linux Ubunut 22.04.4 Kernel 6.2.0-36-generic 
@ CreatedTime: 2023/12/21
"""
from __future__ import annotations

import sys
import warnings
import platform
import asyncio

sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from typing import Union


class SQLStatement:
    @staticmethod
    def select_clause(
        field_iterable: Union[str, list[str], tuple[str], set[str], None] = None
    ) -> str:
        if not field_iterable:
            results = "select *"
        else:
            if not isinstance(field_iterable, (list, tuple, set)):
                results = "select {}".format(field_iterable)
            else:
                if not isinstance(field_iterable, str):
                    raise TypeError
                field_str = " ".join(field_iterable)
                results = " ".join(("select", field_str))
        return results

    @staticmethod
    def from_clause(
        table: str, database: Union[str, None] = None, schema: Union[str, None] = None
    ) -> str:
        if not database and not schema:
            raise ValueError
        if database and schema:
            raise ValueError
        if not table:
            raise ValueError
        if not isinstance(table, str):
            raise TypeError
        if database:
            if not isinstance(database, str):
                raise TypeError
            else:
                results = "from {}.{}".format(database, table)
        elif schema:
            if not isinstance(schema, str):
                raise TypeError
            else:
                results = "from {}.{}".format(schema, table)
        return results

    @staticmethod
    def filter_join(
        filter_name: str,
        field_name: str,
        field_value: Union[int, str, tuple[str, int, float]],
        field_operation: str,
    ) -> str:
        if not isinstance(field_name, str):
            raise TypeError
        if isinstance(field_value, str):
            if field_operation in ("like", "ilike"):
                results = "{} {} {} '%{}%'".format(
                    filter_name, field_name, field_operation, field_value
                )
            else:
                results = "{} {} {} '{}'".format(
                    filter_name, field_name, field_operation, field_value
                )
        else:
            if field_operation in ("like", "ilike"):
                raise SyntaxError
            else:
                results = "{} {} {} {}".format(
                    filter_name, field_name, field_operation, field_value
                )
        return results

    @staticmethod
    def where_clause(
        filter_iterable: Union[str, list[str], tuple[str], set[str], None] = None
    ) -> str:
        if not filter_iterable:
            return str()
        if not isinstance(filter_iterable, (list, tuple, set)):
            if not isinstance(filter_iterable, str):
                raise TypeError
            else:
                results = "where {}".format(filter_iterable)
        else:
            results = " ".join(filter_iterable)
        return results