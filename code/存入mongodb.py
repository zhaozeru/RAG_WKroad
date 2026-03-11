import json
from pymongo import MongoClient

# 连接到 MongoDB 服务器
client = MongoClient()

# 选择数据库和集合
db = client['武康路故居数据']
collection = db['14故居数据原版']

# 读取包含 JSON 数据的文本文件
paths = [
    r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【数据获取和清洗】\data\周作民旧居.txt',
    r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【数据获取和清洗】\data\唐绍仪旧居.txt',
    r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【数据获取和清洗】\data\宋庆龄故居.txt',
    r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【数据获取和清洗】\data\巴金故居.txt',
    r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【数据获取和清洗】\data\张乐平故居.txt',
    r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【数据获取和清洗】\data\柯灵故居.txt',
    r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【数据获取和清洗】\data\武康庭故居.txt',
    r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【数据获取和清洗】\data\王元化故居.txt',
    r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【数据获取和清洗】\data\莫觞清旧居.txt',
    r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【数据获取和清洗】\data\陈果夫旧居.txt',
    r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【数据获取和清洗】\data\陈立夫旧居.txt',
    r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【数据获取和清洗】\data\颜福庆旧居.txt',
    r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【数据获取和清洗】\data\马步芳故居.txt',
    r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【数据获取和清洗】\data\黄兴故居.txt'
]

for path in paths:
    with open(path, 'r', encoding='utf-8') as file:  # 确保文件编码为 utf-8
        data = json.load(file)

    # 将 JSON 数据插入到 MongoDB 集合中
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)

    print(f"数据已成功插入到 MongoDB 中: {path}")