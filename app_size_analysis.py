#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "小怡情ifelse"

import os
import sys
import time

"""

    分析APP安装包大小组成的脚本 支持Python3
    参数1: linkMap文件
    参数2: -m是否按照组件model输出分析结果， 可选 不传默认按照文件输出

"""

html_content = "<h2 align=center>App Size Analysis 数据</h2>" \
               "<table border='1px solid' " \
               "style='border-collapse:collapse;table-layout:fixed;word-break:break-all;width: 60%;margin: 0 auto;'>" \
               "<th>组件名称</th>" \
               "<th>组件大小</th>"


def usage():
    print('''
    --help      帮助
    param1      LinkMap文件路径
    param2      传参-m 按照组件modul输出
    ''')


class SymbolModel:
    """
    符号对象model，一个.o类生成一个symbol对象（文件、size）
    """
    file = ""
    size = 0


def get_all_symbol_map():
    """
    遍历linkmap文件，分析所有.o类信息生成symbol列表（.o = symbol）
    """
    symbol_map = {}
    arrive_files = False
    arrive_sections = False
    arrives_symbols = False
    with open(sys.argv[1], 'rb') as file:
        for line in file.readlines():
            # Python3 line此时是bytes类型，解码str便于后续操作
            line = line.decode("utf8", "ignore")
            if line.startswith('#'):
                if line.startswith('# Object files:'):
                    arrive_files = True
                elif line.startswith('# Sections:'):
                    arrive_sections = True
                elif line.startswith('# Symbols:'):
                    arrives_symbols = True
            else:
                if arrive_files == True and arrive_sections == False and arrives_symbols == False:
                    # 在# Object files:区域生成所有文件的Symbol对象,此时size为0
                    location = line.find(']')
                    if location != -1:
                        key = line[:location + 1]
                        if symbol_map.get(key) is not None:
                            continue
                        symbol = SymbolModel()
                        symbol.file = line[location + 1:]
                        symbol_map[key] = symbol
                elif arrive_files == True and arrive_sections == True and arrives_symbols == True:
                    # 当执行到# Symbols:区域后，开始统计每个文件的size
                    symbol_array = line.split('\t')
                    if len(symbol_array) == 3:
                        file_and_Name = symbol_array[2]
                        size = int(symbol_array[1], 16)
                        location = file_and_Name.find(']')
                        if location != -1:
                            key = file_and_Name[:location + 1]
                            symbol = symbol_map.get(key)
                            if symbol is not None:
                                symbol.size = symbol.size + size
    return symbol_map


def create_association_modul_results_data(symbol_array):
    """
    生成分析APP大小的结果 单位：modul组件
    """
    results = ["组件名称\t组件大小\r"]
    total_size = 0
    modul_map = {}
    for symbol in symbol_array:
        names = symbol.file.split('/')
        name = names[len(names) - 1].strip('\n')
        location = name.find("(")
        if name.endswith(")") and location != -1:
            # 工程的.a或者framework
            modul = name[:location]
            association_symbol = modul_map.get(modul)
            if association_symbol is None:
                association_symbol = SymbolModel()
                modul_map[modul] = association_symbol

            association_symbol.file = modul
            association_symbol.size = association_symbol.size + symbol.size
        else:
            # 系统的动态库
            modul_map[symbol.file] = symbol
    sorted_symbols = sorted(modul_map.values(), key=lambda s: s.size, reverse=True)

    for symbol in sorted_symbols:
        results.append(format_symbol(symbol))
        total_size += symbol.size
    results.append("总大小: %.2fM" % (total_size / 1024.0 / 1024.0))
    global html_content
    html_content += "<td colspan=2 style=text-align:center>" + "总大小: %.2fM" % (total_size / 1024.0 / 1024.0) + "</td>"
    return results


def create_file_results_data(symbol_array):
    """
    生成分析APP大小的结果 单位：file
    """
    results = ["类名称\t类大小\r"]
    total_size = 0
    for symbol in symbol_array:
        results.append(format_symbol(symbol))
        total_size += symbol.size
    results.append("总大小: %.2fM" % (total_size / 1024.0 / 1024.0))
    global html_content
    html_content += "<td colspan=2 style=text-align:center>" + "总大小: %.2fM" % (total_size / 1024.0 / 1024.0) + "</td>"
    return results


def format_symbol(symbol):
    """
    将symbol中的file、size格式为字符串
    """
    file_name = ""
    size = ""
    names = symbol.file.split('/')
    if len(names) > 0:
        temp = names[len(names) - 1]
        location = temp.find('(')
        file_name = temp[location + 1:-2]
    if symbol.size / 1024.0 / 1024.0 > 1:
        size = "%.2fM" % (symbol.size / 1024.0 / 1024.0)
    else:
        size = "%.1fK" % (symbol.size / 1024.0)
    symbol_info = "%s\t%s" % (file_name, size)
    global html_content
    html_content += "<td style=text-align:center>" + file_name + "</td>"
    html_content += "<td style=text-align:center>" + size + "</td>"
    html_content += "<tr>"
    return symbol_info


if __name__ == '__main__':
    """
    主入口, 参数 < 2 非法
    """
    if len(sys.argv) < 2:
        print('error - param invalid, need linkmap file path')
        exit(1)

    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print('error - param not file')
        exit(1)

    with open(file_path, 'rb') as file:
        data = file.read()
        value = str(data)
        if value.find('# Object files:') == -1:
            print('输入文件格式不正确')
            exit(1)
        if value.find('# Sections:') == -1:
            print('输入文件格式不正确')
            exit(1)
        if value.find('# Symbols:') == -1:
            print('输入文件格式不正确')
            exit(1)

    print("============ 开始处理linkMap文件 ==========")
    startTime = time.time()

    # 开始将所有类生成symbol列表
    symbol_map = get_all_symbol_map()

    # 针对所有的symbol列表按照size进行排序
    symbol_array = sorted(symbol_map.values(), key=lambda s: s.size, reverse=True)

    symbol_result_array = []
    # 对所有symbol对象进行格式化处理
    html_content += "<tr>"
    if len(sys.argv) >= 3 and sys.argv[2] == "-m":
        symbol_result_array = create_association_modul_results_data(symbol_array)
    else:
        symbol_result_array = create_file_results_data(symbol_array)

    # 分析结果以html报表形式输出
    desktop_path = os.path.expanduser("~") + "/Desktop"
    file_path = desktop_path + "/AppSizeAnalysis"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_path += "/AppSizeAnalysis.html"
    file_obj = open(file_path, "w")
    file_obj.write(html_content)
    file_obj.close()

    print("============ 处理结束html报表已生成 %s ============" % file_path)
    print('处理过程共花费%.2fs' % (time.time() - startTime))
