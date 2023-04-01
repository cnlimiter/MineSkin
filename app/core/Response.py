#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Response.py
# @Time      :2023/4/1 16:23
# @Author    :Cnlimiter
# @Des       :简介
from typing import List

from starlette.responses import JSONResponse


def res_antd(data: List = None, total: int = 0, code: bool = True):
    """
    支持ant-design-table 返回的格式
    :param code:
    :param data:
    :param total:
    :return:
    """
    if data is None:
        data = []
    result = {
        "success": code,
        "data": data,
        "total": total
    }
    return result


def base_response(code, msg, data=None):
    """基础返回格式"""
    if data is None:
        data = []
    result = {
        "code": code,
        "message": msg,
        "data": data
    }
    return result


def fail(data=None):
    """失败返回格式"""
    return JSONResponse(
        status_code=-1,
        content=data
    )


def noContent():
    return JSONResponse(
        status_code=204,
        content=""
    )


def success(data):
    return JSONResponse(
        status_code=200,
        content=data
    )
