import pymongo

class WKRoadGraph:
    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db = self.conn['武康路故居数据']
        self.col = self.db['14故居数据原版']
        # created为建筑始建时间、yname为建筑异名
        # 以下列出的是json中的所有键
        self.key_list = ['address','created','houseNumber','description',
                         'designer','uri','architecturalStyle','relation',
                         'road','name','architectureStructure','location'
                         ,'event','lane','architectural_photos','yname']

    # 清洗步骤只对需要清洗的键值进行修整
    # 需清洗的有 relation\road\yname\location\event\created 其中relation和event是重点对象
    def clean_data(self):
        count = 0
        for item in self.col.find():
            data = {}
            # road
            if 'road' in item:
                names = [road['name'] for road in item['road'] if isinstance(road, dict) and 'name' in road]
                data['road'] = names
            else:
                data['road'] = []

            # yname
            if 'yname' in item:
                labels = [yname['label'] for yname in item['yname'] if isinstance(yname, dict) and 'label' in yname]
                data['yname'] = labels
            else:
                data['yname'] = []

            # location
            if 'location' in item and isinstance(item['location'], list):
                for loca in item['location']:
                    if isinstance(loca, dict) and 'lat' in loca and 'long' in loca:
                        data['location'] = f"经度为{loca['long']}，纬度为{loca['lat']}"
            else:
                data['location'] = ''

            # created
            if 'created' in item:
                structure_start_time = item['created']
                structure_end_time = '2024'
                data['created'] = {'structure_start_time':structure_start_time, 'structure_end_time':structure_end_time}
            else:
                data['created'] = {}

            # event
            data['event'] = []
            if 'event' in item:
                for one_evet in item['event']:
                    event_dict = {}
                    if 'startedAtTime' in one_evet:
                        event_time = one_evet['startedAtTime']
                        if len(event_time) == 4:
                            event_start_time = f"{event_time}-12"
                            event_end_time = '2024-12'
                        elif len(event_time) == 7:
                            event_start_time = f"{event_time}"
                            event_end_time = '2024-12'
                        elif len(event_time) == 10:
                            event_start_time = event_time[:7]
                            event_end_time = '2024-12'
                        event_dict['event_start_time'] = event_start_time
                        event_dict['event_end_time'] = event_end_time
                    if 'description' in one_evet:
                        event_dict['description'] = one_evet['description']

                    if 'image' in one_evet and one_evet['image']:
                        event_dict['image'] = one_evet['image']

                    data['event'].append(event_dict)
            else:
                data['event'] = []

            # architectural_photos
            data['architectural_photos'] = []

            # relation
            # 先不做处理


            # 重组数据
            for key in self.key_list:
                if key not in data:
                    if key in item:
                        data[key] = item[key]
                    else:
                        data[key] =''

            # 加入mongodb
            try:
                self.db['14故居数据清洗版'].insert_one(data)
                count += 1
                print(count)
            except Exception as e:
                print(e)

        return

if __name__ == '__main__':
    handler = WKRoadGraph()
    handler.clean_data()