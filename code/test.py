from neo4j import GraphDatabase

def fetch_graph_from_neo4j(category, person_id):
    uri = "bolt://39.105.126.162:7687"  # 替换为你的远程Neo4j主机地址
    user = "neo4j"
    password = "_rong.5420"  # 替换为你的Neo4j密码

    driver = GraphDatabase.driver(uri, auth=(user, password))

    def query_graph(tx, category, person_id):
        if not category and not person_id:
            result = tx.run("""
                MATCH (p)-[r1]->(n1)
                RETURN p, r1, n1
            """)
        elif category == '人物栏' and person_id:
            result = tx.run("""
                MATCH (p:人物节点 {name: $personId})
                OPTIONAL MATCH (p)-[r1]->(n1)
                OPTIONAL MATCH (m)-[r2]->(n1)
                RETURN p, r1, n1, m, r2
            """, personId=person_id)
        elif category == '故居栏' and person_id:
            result = tx.run("""
                MATCH (p:故居节点 {name: $personId})
                OPTIONAL MATCH (p)-[r1]->(n1)
                OPTIONAL MATCH (m)-[r2]->(n1)
                RETURN p, r1, n1, m, r2
            """, personId=person_id)
        else:
            raise ValueError("Invalid category or person_id")

        nodes = {}
        links = []

        for record in result:
            # 处理 p 和 n1 节点
            for label in ['p', 'n1']:
                node = record.get(label)
                if node:
                    node_id = node.element_id
                    if node_id not in nodes:
                        type_ = next(iter(node.labels), 'unknown')
                        nodes[node_id] = {
                            'id': node_id,
                            'label': node.get('name'),
                            'type': type_,
                            'properties': dict(node),
                            **dict(node)
                        }

            # 处理关系 r1
            source = record.get('p')
            target = record.get('n1')
            relationship = record.get('r1')
            if source and target and relationship:
                links.append({
                    'source': source.element_id,
                    'target': target.element_id,
                    'type': relationship.type
                })

            # 处理 m 节点和关系 r2
            if category and person_id:
                m_node = record.get('m')
                m_relationship = record.get('r2')
                if m_node and m_relationship:
                    m_node_id = m_node.element_id
                    if m_node_id not in nodes:
                        type_ = next(iter(m_node.labels), 'unknown')
                        nodes[m_node_id] = {
                            'id': m_node_id,
                            'label': m_node.get('name'),
                            'type': type_,
                            'properties': dict(m_node),
                            **dict(m_node)
                        }
                    links.append({
                        'source': m_node_id,
                        'target': target.element_id,
                        'type': m_relationship.type
                    })

        return list(nodes.values()), links

    with driver.session(database="WKroadproject") as session:
        nodes, links = session.execute_read(query_graph, category, person_id)
        print('Fetched data:', {'nodes': nodes, 'links': links})
        return {'nodes': nodes, 'links': links}

# 示例调用
fetch_graph_from_neo4j('人物栏', '宋庆龄')