#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from china_region.constants import (
    CITY_DF
)

__all__ = ['search', 'search_all', 'sample']


def search(province=None, city=None, county=None):
    """
    只获取匹配的第一个数据。

    >>> import china_region
    >>> china_region.search('辽宁 铁岭')
    {'province': '辽宁省', 'city': '铁岭市', 'county': '铁岭市', 'longitude': 123.83, 'latitude': 42.28, 'zipCode': '112000'}

    :param province: str, 省份
    :param city: str, 市
    :param county: str, 县
    :return: dcit
    """
    all_data = search_all(province, city, county)
    if all_data:
        return all_data[0]
    return {}


def search_all(province=None, city=None, county=None):
    """
    获取匹配到的所有数据
    >>> import china_region
    >>> china_region.search_all(county='华安')
    [{'province': '福建省', 'city': '漳州市', 'county': '华安县', 'longitude': 117.53, 'latitude': 25.02, 'zipCode': '363800'}]
    >>> china_region.search_all(province='福建省',city='华安')
    [{'province': '福建省', 'city': '漳州市', 'county': '华安县', 'longitude': 117.53, 'latitude': 25.02, 'zipCode': '363800'}]
    >>> china_region.search_all(province='贵州',city='贵阳',county='白云')
    [{'province': '贵州省', 'city': '贵阳市', 'county': '白云区', 'longitude': 106.65, 'latitude': 26.68, 'zipCode': '550014'}]

    :param province: str, 省份
    :param city: str, 市
    :param county: str, 县
    :return: list item dict
    """

    # 如果是 "山东 济南"主动分割
    if province and re.findall(r'\s+', province.strip()) and city is None and county is None:
        ss = re.split(r'\s+', province)
        if len(ss) == 2:
            province, city = ss
        elif len(ss) > 2:
            province, city, county = ss[:3]

    my_df = CITY_DF
    cur_len = 0
    if province:
        province = re.sub(r'[省]{1}$', '', province)
        df_s = my_df[my_df['province'].str.contains(province)]
        cur_len = df_s.shape[0]
        if cur_len > 0:
            my_df = df_s

    # 如果搜索省份没有结果，而city，county为空，则把省份名赋值给城市名
    if cur_len == 0 and city is None and county is None:
        city = province

    if city:
        sc = my_df['city'].str.contains(city)
        my_df_temp = my_df[sc]

        # 这一步的作用是为了怕写错了城市，如：内蒙古兴安盟，写成兴安县。当搜索没有结果时，清除最后一个字，重新再搜索一次
        if my_df_temp.shape[0] == 0 and len(city) > 2 and city[-1] in '市盟州区县台':
            n_city = re.sub(r'[市盟州区县台]{1}$', '', city)
            sc = my_df['city'].str.contains(n_city)
            my_df_temp = my_df[sc]

        cur_len = my_df_temp.shape[0]
        if cur_len > 0:
            my_df = my_df_temp

    # 如果搜索城市名没有结果，而county为空，则把城市名赋值给县城名
    if cur_len == 0 and county is None:
        county = city

    if county:
        scc = my_df['county'].str.contains(county)
        my_df_temp = my_df[scc]

        # 像是蓟县只有两个字，就不用做处理。
        if my_df_temp.shape[0] == 0 and len(county) > 2 and county[-1] in '市区县旗盟州区港门台尔':
            n_county = re.sub(r'[市区县旗盟州区港门台尔]{1}$', '', county)
            scc = my_df['county'].str.contains(n_county)
            my_df_temp = my_df[scc]

        cur_len = my_df_temp.shape[0]
        if cur_len > 0:
            my_df = my_df_temp

    if cur_len > 0:
        return my_df.to_dict('records')
    else:
        return []


def sample():
    """
    获取一个随机的地址
    :return: dict ，例如：{'province': '山西省', 'city': '临汾市', 'county': '洪洞县', 'longitude': 111.67, 'latitude': 36.25, 'zipCode': '041600'}
    """
    yy = CITY_DF.sample()
    cc = yy.to_dict('records')[0]
    return cc


# if __name__ == '__main__':
    # ret = search_all(province='贵州',city='贵阳', county='白云区')
    # ret = search_all(county='华安')
    # ret = search_all("山东 济南 历下")
    #
    # ret = search('辽宁 铁岭')
    # yy = CITY_DF.sample()
    # cc = yy.to_dict('records')[0]
    # print(cc)
