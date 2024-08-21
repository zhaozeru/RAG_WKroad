import json

def remove_contributorOf(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if key != 'contributorOf':
                new_data[key] = remove_contributorOf(value)
        return new_data
    elif isinstance(data, list):
        return [remove_contributorOf(item) for item in data]
    else:
        return data

def process_json(json_data):
    data = json.loads(json_data)
    processed_data = remove_contributorOf(data)
    return json.dumps(processed_data, ensure_ascii=False)

# 本地文件路径
file_path = r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【数据获取和清洗】\data\武康路故居数据.14故居数据清洗版.json'

# 读取本地文件内容
with open(file_path, 'r', encoding='utf-8') as file:
    json_data = file.read()

# 处理JSON数据
processed_json = process_json(json_data)

# 保存处理后的JSON数据到新文件
output_file_path = r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【LangChain-JSON】\test.json'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(processed_json)

print(f"Processed JSON data has been saved to {output_file_path}")