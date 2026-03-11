import json
from py2neo import Graph, Node

class WKRoadGraph:
    def __init__(self):
        cur_dir = r'D:\my_document\pycharm\project\【竞赛项目：上图开放数据】\【数据获取和清洗】\data\武康路故居数据.14故居数据清洗版.json'
        self.data_path = cur_dir
        self.g = Graph("http://localhost:7474", auth=("neo4j", "_rong.5420"), name='WKroadproject')

    def create_center_node(self, center_node=None): #创建中心节点
        if center_node is None:
            center_node = ['武康路']
            center_node_info = {
                'name': "武康路",
                '起点': '华山路',
                '终点': '淮海中路',
                '简介': '武康路（Wukang Road），是中国上海市徐汇区境内南北向道路，位于徐汇区北部，连接了华山路和淮海中路，也是中国历史文化名街之一 。武康路北起华山路，南至淮海中路，全长1182.7米，宽12米至15.5米 。',
                '历史变迁': '武康路于清光绪三十三年（1907年）修筑，时名福开森路 ；于民国三年（1914年）拆分 ；于民国三十二年（1943年）更名为武康路 。',
                '文化特色': '武康路的沿线建筑代表了上海20世纪二三十年代重要建筑设计机构和建筑师的作品，展现了当时的顶尖设计水平。初期由外国设计师主导，\
                    后来逐渐转为中国建筑师主导，涵盖了诸如公和洋行、责安洋行、思九生洋行等重要建筑设计机构和设计师。在林荫大道两旁，高级花园别墅汇集了不同\
                    风格的建筑，包括英国乡村式、法国文艺复兴式、西班牙式、地中海式、装饰艺术派、现代派以及混合式建筑等。这些建筑集聚了不同历史时期、国家\
                    建筑风格的代表作品，展示了上海独特的海派文化，并成为宝贵的文化遗产，见证了东西方文化的交融和发展 。',
            }

        count = 0
        for i in center_node:
            node = Node('中心节点',
                        name=i,
                        起点=center_node_info.get('起点'),
                        终点=center_node_info.get('终点'),
                        简介=center_node_info.get('简介'),
                        历史变迁=center_node_info.get('历史变迁'),
                        文化特色=center_node_info.get('文化特色')
            )
            self.g.create(node)
            count += 1
        print(f"创建中心节点 {count}")
        print("中心节点创建完成！！")
        return

    def read_nodes(self): #捕捉节点信息
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data_json = json.load(f)







        center_node = ['武康路']
        center_road = center_node[0]
############################################################################
        constructs = []
        construct_peoples = []
        construct_photos = []
        construct_events = []
        people_events = []
        people_photos = []
        people_ynames = []
        people_works = []
        people_organizaitons = []

        construct_info = {}
        construct_people_info = {}
        construct_event_info = {}
        construct_photo_info = {}
        people_photo_info = {}
        people_event_info = {}
        people_work_info = {}
        people_yname_info = {}

        rels_construct = []
        rels_people = []
        rels_photo = []
        rels_event = []
        rels_people_event = []
        rels_people_photo = []
        rels_people_yname = []
        rels_people_work = []
        rels_people_organizaiton = []

############################################################################
        for item in data_json:
            construct_name = item.get('name')
            if construct_name: # 处理故居节点
                constructs.append(construct_name)
                rels_construct.append([center_road, construct_name])
                construct_info[construct_name] = {
                    'yname': item.get('yname'),
                    'created': item.get('created'),
                    'address': item.get('address'),
                    'uri': item.get('uri'),
                    'description': item.get('description'),
                    'architecturalStyle': item.get('architecturalStyle'),
                    'architectureStructure': item.get('architectureStructure'),
                    'designer': item.get('designer'),
                    'houseNumber': item.get('houseNumber'),
                    'location': item.get('location'),
                    'road': item.get('road'),
                    'lane': item.get('lane'),
                    'architectural_photos': item.get('architectural_photos')
                }

            for i, event in enumerate(item.get('event', [])): #处理故居事件节点
                event_name = f"相关事件{i + 1}-{construct_name}"
                construct_events.append(event_name)
                construct_event_info[event_name] = {
                    'event_start_time': event.get('event_start_time'),
                    'event_end_time': event.get('event_end_time'),
                    'description': event.get('description'),
                    'image': event.get("image", {}).get("path")
                }
                rels_event.append([construct_name, event_name])

            for i, photo in enumerate(item.get('architectural_photos', [])): #处理故居图片节点
                photo_name = f"建筑图片{i + 1}-{construct_name}"
                construct_photos.append(photo_name)
                construct_photo_info[photo_name] = {
                    'description': photo
                }
                rels_photo.append([construct_name, photo_name])

            relation = item.get('relation')
            for person in relation: # 处理故居人物节点
                people_uri = person.get('uri')
                people_name = person['name']
                construct_peoples.append(people_name)
                rels_people.append([construct_name, people_name])
                construct_people_info[people_name] = {
                    'courtesyName': people_uri.get('courtesyName'),
                    'pseudonym': people_uri.get('pseudonym'),
                    'id': person.get('id'),
                    'birthday': people_uri.get('birthday'),
                    'deathday': people_uri.get('deathday'),
                    'birthPlace': people_uri.get('birthPlace'),
                    'ethnicity': people_uri.get('ethnicity'),
                    'nationality': people_uri.get('nationality'),
                    'speciality': people_uri.get('speciality'),
                    'officialEvent': people_uri.get('officialEvent'),
                    'spouseOf': people_uri.get('spouseOf'),
                    'childOf': people_uri.get('childOf'),
                    'friendOf': people_uri.get('friendOf'),
                    'parentOf': people_uri.get('parentOf'),
                    'gender': people_uri.get('gender'),
                    'familyName': people_uri.get('familyName'),
                    'nativePlace': people_uri.get('nativePlace'),
                    'temporal': people_uri.get('temporal'),
                    'noteOfSource': people_uri.get('noteOfSource'),
                    'relatedOrganization': people_uri.get('relatedOrganization'),
                    'person_photos': people_uri.get('img')
                }


                brief_biography = people_uri.get('briefBiography', []) # 处理人物相关事件节点
                if isinstance(brief_biography, str):
                    brief_num = f"相关事件-{people_name}"
                    people_events.append(brief_num)
                    people_event_info[brief_num] = {
                        'description': brief_biography
                    }
                    rels_people_event.append([people_name, brief_num])
                elif isinstance(brief_biography, list):
                    for i, brief in enumerate(brief_biography):
                        brief_num = f"相关事件{i + 1}-{people_name}"
                        people_events.append(brief_num)
                        people_event_info[brief_num] = {
                            'description': brief
                        }
                        rels_people_event.append([people_name, brief_num])

                for i, org in enumerate(people_uri.get('relatedOrganization', [])): #处理人物中相关机构节点
                    people_organizaitons.append(org)
                    rels_people_organizaiton.append([people_name, org])

                photos = people_uri.get('img', []) # 处理人物图片节点
                if isinstance(photos, str):
                    photo_num = f"相关图片-{people_name}"
                    people_photos.append(photo_num)
                    people_photo_info[photo_num] = {
                        'img': photos
                    }
                    rels_people_photo.append([people_name, photo_num])
                elif isinstance(photos, list):
                    for i, photo in enumerate(photos):
                        photo_num = f"相关图片{i + 1}-{people_name}"
                        people_photos.append(photo_num)
                        people_photo_info[photo_num] = {
                            'img': photo
                        }
                        rels_people_photo.append([people_name, photo_num])

                for i, yname in enumerate(people_uri.get('name', [])): #处理人物别名节点
                    people_yname = yname.get('label')
                    people_ynames.append(people_yname)
                    people_yname_info[people_yname] = {
                        'nameType': yname.get('nameType'),
                        'noteOfSource': yname.get('noteOfSource')
                    }
                    rels_people_yname.append([people_name, people_yname])

                for work1 in people_uri.get('contributorOf', []): #处理人物作品节点
                    if 'title' in work1:
                        work_name = work1['title']
                        people_works.append(work_name)
                        people_work_info[work_name] = {
                            'time': work1.get('time'),
                            'type': work1.get('type'),
                            'theme': work1.get('theme'),
                            'description': work1.get('description'),
                            'id': work1.get('uri')
                        }
                        rels_people_work.append([people_name, work_name])
                for work2 in people_uri.get('creatorOf', []):
                    work_name = work2.get('title')

                    people_works.append(work_name)
                    people_work_info[work_name] = {
                        'time': work2.get('time'),
                        'type': work2.get('type'),
                        'theme': work2.get('theme'),
                        'description':work2.get('description'),
                        'id': work2.get('uri')
                    }
                    rels_people_work.append([people_name, work_name])

                created_work = people_uri.get('createdWork', [])
                # 确保 created_work 是一个列表
                if isinstance(created_work, str):
                    created_work = [created_work]
                # 处理 created_work 列表
                for work_name in created_work:
                    people_works.append(work_name)
                    rels_people_work.append([people_name, work_name])

        return set(constructs), set(construct_peoples), set(construct_photos), set(construct_events), set(people_events), set(people_photos), set(people_ynames), set(people_works), set(people_organizaitons), \
            construct_info, construct_people_info, construct_event_info, construct_photo_info, people_photo_info, people_event_info,people_work_info, people_yname_info, \
            rels_construct, rels_people, rels_photo, rels_event, rels_people_event, rels_people_photo, rels_people_yname, rels_people_work, rels_people_organizaiton

    def create_construct_nodes(self, constructs, construct_info):  # 创建故居节点
        count = 0
        for construct_name in constructs:
            info = construct_info.get(construct_name, {})
            # 打印属性值以进行调试
            # print(f"Creating node for {construct_name} with properties: {info}")
            designer_label = [item.get('label') for item in info.get('designer', []) if item.get('label')]
            road_str = ', '.join(info.get('road', []))
            lane_label = info.get('lane')[0].get('label') if info.get('lane') else None
            architectural_photos = ', '.join(info.get('architectural_photos', []))
            node = Node("故居节点",
                        name = construct_name,
                        建筑异名=info.get('yname'),
                        建筑开始时间=info.get('created').get('structure_start_time'),
                        建筑完工时间=info.get('created').get('structure_end_time'),
                        建筑所在地址=info.get('address'),
                        建筑ID=info.get('uri'),
                        建筑简介=info.get('description'),
                        建筑风格=info.get('architecturalStyle'),
                        建筑结构=info.get('architectureStructure'),
                        设计者=designer_label,
                        门牌号=info.get('houseNumber'),
                        位置坐标=info.get('location'),
                        所在相关道路=road_str,
                        里弄=lane_label,
                        故居图片=architectural_photos
                        )
            self.g.create(node)
            count += 1
        print(f"故居节点{count}")
        print('故居节点创建完成！！')
        return
    def create_person_nodes(self, construct_peoples, construct_people_info): #创建人物节点
        count = 0
        for person_name in construct_peoples:
            # print(person_name)
            info = construct_people_info.get(person_name, {})
            # print(info)
            person_photos = info.get('person_photos', [])
            person_photos_str = ', '.join(person_photos if person_photos is not None else [])
            # print(person_photos)
            node = Node("人物节点",
                        name = person_name,
                        人物字名=info.get('courtesyName'),
                        人物号名=info.get('pseudonym'),
                        人物ID=info.get('id'),
                        出生日期=info.get('birthday'),
                        死亡日期=info.get('deathday'),
                        出生地=info.get('birthPlace'),
                        民族=info.get('ethnicity'),
                        国籍=info.get('nationality'),
                        职业=info.get('speciality'),
                        任职经历=info.get('officialEvent'),
                        相关机构=info.get('relatedOrganization'),
                        配偶=info.get('spouseOf'),
                        父亲=info.get('childOf'),
                        友人=info.get('friendOf'),
                        儿女=info.get('parentOf'),
                        性别=info.get('gender'),
                        姓氏=info.get('familyName'),
                        籍贯=info.get('nativePlace'),
                        朝代=info.get('temporal'),
                        数据来源=info.get('noteOfSource'),
                        人物图片=person_photos_str
                        )
            self.g.create(node)
            count += 1
        print(f"人物节点{count}")
        print('人物节点创建完成！！')
        return
    def create_photo_nodes(self, construct_photos, construct_photo_info): #创建故居图片节点
        count = 0
        for photo in construct_photos:
            info = construct_photo_info.get(photo, {})
            node = Node("图片节点",
                        name = photo,
                        故居图片描述=info.get('description')
                        )
            self.g.create(node)
            count += 1
        print(f"图片节点{count}")
        print('图片节点创建完成！！')
        return
    def create_event_nodes(self, construct_events, construct_event_info): #创建故居事件节点
        count = 0
        for event in construct_events:
            info = construct_event_info.get(event, {})
            node = Node("事件节点",
                        name=event,
                        事件开始时间=info.get('event_start_time'),
                        事件结束时间=info.get('event_end_time'),
                        描述=info.get('description'),
                        图片= info.get('image')
                        )
            self.g.create(node)
            count += 1
        print(f"事件节点{count}")
        print('事件节点创建完成！！')
        return

    def create_people_event_nodes(self, people_events,people_event_info): #创建人物中的事件节点
        count = 0
        for event in people_events:
            info = people_event_info.get(event, {})
            node = Node("人物简介节点",
                        name=event,
                        描述=info.get('description')
                        )
            self.g.create(node)
            count += 1
        print(f"人物简介节点{count}")
        print('人物简介节点创建完成！！')
        return
    def create_people_organization_nodes(self, people_organizaitons): #创建人物中的相关机构节点
        count = 0
        for org in people_organizaitons:
            node = Node("人物相关机构节点",name=org)
            self.g.create(node)
            count += 1
        print(f"人物相关机构节点{count}")
        print('人物相关机构节点创建完成！！')
        return
    def create_people_photo_nodes(self, people_photos,people_photo_info): #创建人物图片节点
        count = 0
        for pic in people_photos:
            info = people_photo_info.get(pic, {})
            node = Node("人物图片节点",
                        name=pic,
                        人物图片描述=info.get('img')
                        )
            self.g.create(node)
            count += 1
        print(f"人物图片节点{count}")
        print('人物图片节点创建完成！！')
        return
    def create_people_yname_nodes(self, people_ynames,people_yname_info): #创建人物别名节点
        count = 0
        for yname in people_ynames:
            info = people_yname_info.get(yname, {})
            node = Node("人物别名节点",
                        name=yname,
                        别名类型=info.get('nameType'),
                        别名来源=info.get('noteOfSource')
                        )
            self.g.create(node)
            count += 1
        print(f"人物别名节点{count}")
        print('人物别名节点创建完成！！')
        return
    def create_people_work_nodes(self, people_works,people_work_info): #创建人物作品节点
        count = 0
        for work in people_works:
            info = people_work_info.get(work, {})
            node = Node("人物作品节点",
                        name=work,
                        创作时间=info.get('time'),
                        作品类型=info.get('type'),
                        作品主题=info.get('theme'),
                        作品描述=info.get('description'),
                        作品ID=info.get('id')
                        )
            self.g.create(node)
            count += 1
        print(f"人物作品节点{count}")
        print('人物作品节点创建完成！！')
        return


    def create_graphnodes(self):
        constructs, construct_peoples, construct_photos, construct_events, people_events, people_photos, people_ynames, people_works, people_organizaitons, \
            construct_info, construct_people_info, construct_event_info, construct_photo_info, people_photo_info, people_event_info, people_work_info, people_yname_info, \
            rels_construct, rels_people, rels_photo, rels_event, rels_people_event, rels_people_photo, rels_people_yname, rels_people_work, rels_people_organizaiton = self.read_nodes()

        self.create_construct_nodes(constructs, construct_info)
        self.create_person_nodes(construct_peoples, construct_people_info)
        self.create_photo_nodes(construct_photos, construct_photo_info)
        self.create_event_nodes(construct_events, construct_event_info)
        self.create_people_event_nodes(people_events,people_event_info)
        self.create_people_organization_nodes(people_organizaitons)
        self.create_people_photo_nodes(people_photos,people_photo_info)
        self.create_people_yname_nodes(people_ynames,people_yname_info)
        self.create_people_work_nodes(people_works,people_work_info)




    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        all = len(edges)
        for edge in edges:
            p, q = edge
            query = f"MATCH (p:{start_node}), (q:{end_node}) WHERE p.name='{p}' AND q.name='{q}' CREATE (p)-[:{rel_type} {{name: '{rel_name}'}}]->(q)"
            try:
                self.g.run(query)
                count += 1
            except Exception as e:
                print(e)
        print(f"{rel_type} {count}/{all}")
        return

    def create_graphrels(self):
        constructs, construct_peoples, construct_photos, construct_events, people_events, people_photos, people_ynames, people_works, people_organizaitons, \
            construct_info, construct_people_info, construct_event_info, construct_photo_info, people_photo_info, people_event_info, people_work_info, people_yname_info, \
            rels_construct, rels_people, rels_photo, rels_event, rels_people_event, rels_people_photo, rels_people_yname, rels_people_work, rels_people_organizaiton = self.read_nodes()

        self.create_relationship('中心节点', '故居节点', rels_construct, '武康路and故居', '故居建筑')
        self.create_relationship('故居节点', '人物节点', rels_people, '故居and相关人物', '故居人物')
        self.create_relationship('故居节点', '事件节点', rels_event, '故居and相关事件', '故居事件')
        self.create_relationship('故居节点', '图片节点', rels_photo, '故居and相关图片', '故居图片')

        self.create_relationship('人物节点', '人物简介节点', rels_people_event, '人物and相关简介', '人物简介')
        self.create_relationship('人物节点', '人物相关机构节点', rels_people_organizaiton, '人物and相关机构', '人物相关机构')
        self.create_relationship('人物节点', '人物图片节点', rels_people_photo, '人物and相关照片', '人物图片')
        self.create_relationship('人物节点', '人物别名节点', rels_people_yname, '人物and别名', '人物别名')
        self.create_relationship('人物节点', '人物作品节点', rels_people_work, '人物and相关作品', '人物作品')



if __name__ == "__main__":
    wk_graph = WKRoadGraph()
    wk_graph.create_center_node()
    wk_graph.create_graphnodes()
    wk_graph.create_graphrels()