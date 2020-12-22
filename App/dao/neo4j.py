from py2neo import Node, Relationship, Graph, NodeMatcher
import time


def get_all_triplets():
    graph = Graph("http://10.147.17.138:7474", auth=("neo4j","qbneo4j"))
    cyber = 'MATCH (a)-[b]->(c) RETURN a.name as source, c.name as target, type(b) as rela'
    relationships = graph.run(cyber)

    rs = []
    start_time = time.time()
    for relation in relationships:
        # print(type(relation), relation.items(), dict(relation.items()))
        rs.append(dict(relation.items()))

    # print(rs[:10])
    end_time = time.time()
    print('Time consumption:', end_time - start_time, 's')
    print('Total relationships:', len(rs))
    return rs

if __name__ == '__main__':
    get_all_triplets()