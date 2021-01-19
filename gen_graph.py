# -*- coding:utf-8 -*-
from py2neo import Node, Relationship, Graph
import pandas as pd
import json
import sys


def create_nodes(graph):
    data = pd.read_csv('corp_info.csv')

    persons = set()
    dict = {'Person': set(), 'Industry': set(), 'Type': set(), 'Admin_div': set()}
    for i, row in data.iterrows():
        node = Node('Corporation', name=row['name'])
        node['code'] = row['code']
        node['regist_capital'] = row['regist_capital']
        node['establish_date'] = row['establish_date']
        node['business_scope'] = row['business_scope']

        graph.create(node)

        dict['Industry'].add(row['industry'])
        dict['Type'].add(row['type'])
        dict['Admin_div'].add(row['admin_div'])

        dict['Person'].add(row['legal_person'])
        for name in row['member'].split(','):
            name = name.strip()
            dict['Person'].add(name)

    for key, values in dict.items():
        for value in values:
            node = Node(key, name=value)
            graph.create(node)


def create_edges(graph):
    data = pd.read_csv('corp_info.csv')

    for i, row in data.iterrows():

        # link legal_person to corporation
        cyber = "MATCH (a:Person {name:'" + row['legal_person'] + "'}), (b:Corporation {name:'" + row[
            'name'] + "'}) MERGE (a)-[:legal_person]->(b)"
        graph.run(cyber)
        # link industry to corporation
        cyber = "MATCH (a:Industry {name:'" + row['industry'] + "'}), (b:Corporation {name:'" + row[
            'name'] + "'}) MERGE (a)-[:industry]->(b)"
        graph.run(cyber)
        # link type to corporation
        cyber = "MATCH (a:Type {name:'" + row['type'] + "'}), (b:Corporation {name:'" + row[
            'name'] + "'}) MERGE (a)-[:type]->(b)"
        graph.run(cyber)
        # link admin_div to corporation
        cyber = "MATCH (a:Admin_div {name:'" + row['admin_div'] + "'}), (b:Corporation {name:'" + row[
            'name'] + "'}) MERGE (a)-[:admin_div]->(b)"
        graph.run(cyber)

        for name in row['member'].split(','):
            name = name.strip()
            # link member to corporation
            cyber = "MATCH (a:Person {name:'" + name + "'}), (b:Corporation {name:'" + row[
                'name'] + "'}) MERGE (a)-[:member]->(b)"
            graph.run(cyber)


if __name__ == "__main__":
    if len(sys.argv) == 5:
        print('知识图谱正在生成...')
        url = 'http://{}:{}'.format(sys.argv[1], sys.argv[2])
        user = sys.argv[3]
        password = sys.argv[4]
        graph = Graph(url, auth=(user, password))
        create_nodes(graph)
        create_edges(graph)
        print('知识图谱已生成...')
    else:
        print('参数不正确')
