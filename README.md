# XLAppSizeAnalysis

# 用法：
分析APP安装包大小组成的脚本 支持Python3

参数1: linkMap文件

参数2: -m是否按照组件modul输出分析结果， 可选 不传默认按照文件输出


# 示例
python app_size_analysis.py 参数1 参数2

============ 开始处理linkMap文件 ==========

============ 处理结束html报表已生成 /Users/xiaoqiyingifelse/Desktop/AppSizeAnalysis/AppSizeAnalysis.html ============

处理过程共花费5.60s

[Tips:处理结束之后，结果以html报表形式展示，查看路径是/Users/xiaoqiyingifelse/Desktop/AppSizeAnalysis/AppSizeAnalysis.html]

# 如何获取LinkMap文件
针对主工程配置打开LinkMap开关：Xcode->Project->Build Settings-> Search map -> 设置 Write Link Map Files 选项为YES（release、debug区分配置）
编译工程之后会在指定路径生成LinkMap文件产物，默认是在/Users/xiaoyiqingifelse/Library/Developer/Xcode/DerivedData/xxx-cnwlggeskzjwiyejtomaplxmpnbd/Build/Intermediates.noindex/xxx.build/Debug-iphonesimulator/xxx.build/xxx-LinkMap-normal-x86_64.txt
