from transport_generator import ts_generator as generate
from collections import deque
import time, random, csv, math

# Кузьмин Д.А.
# гр. ИБ-119


class Node:
    def __init__(self, id, neighborlist):
        self.id:int = id
        self.color:int = 0
        self.color_2:int = 0
        self.neighbors = tuple(neighborlist) # пара [(куда, значение)]
        self.min_way = math.inf
        self.min_from:int = -1
    def print_me(self):
        print(f"id: {self.id}, connects: {self.neighbors}")

def refactor(q, size):
    nodes = []
    for i in range(len(q)):
        nblist = []
        for j in range(len(q)):
            if int(q[i][j])!=0:
                nblist.append((j, q[i][j]))
        nodes.append(Node(i, nblist))
    return nodes # множество вершин и ведущих в них

def get_free(nodes):
    for this in nodes:
        if this.BFS_color==0: return this.id

def dijkstra(nodes, start):
    no_neg = True
    min_list = [-1]*len(nodes)
    def found_all():
        for z in nodes:
            if z.color!=1: return 0
        return 1
    queue = deque()
    queue.append(nodes[start].id)
    nodes[start].color = 1
    nodes[start].min_way = 0
    while not found_all():
        try:
            this = queue.popleft() # это id вершины
        except:
            for i in range(len(nodes)):
                if nodes[i].color==0:
                    this = i
                    break
        for i in nodes[this].neighbors:
            way, cost = i[0], i[1]
            if cost < 0:
                no_neg = False
            if nodes[this].min_way + cost < nodes[way].min_way:
                nodes[way].min_way = nodes[this].min_way + cost
                nodes[way].min_from = this
            if nodes[way].color==0: queue.append(nodes[way].id)
        nodes[this].color = 1

    for z in nodes:
        min_list[z.id] = z.min_way

    return (min_list, no_neg)

def check_negar(nodes, min_list, start):
    old_min_list = []
    for i in min_list:
        old_min_list.append(i)
    if len(nodes)>5: maxx=5
    else: maxx=len(nodes)
    x = -1
    for j in range(maxx):
        for this in range(0, len(nodes)):
            for i in nodes[this].neighbors:
                way, cost = i[0], i[1]
                if nodes[this].min_way + cost < nodes[way].min_way:
                    nodes[way].min_way = nodes[this].min_way + cost
                    nodes[way].min_from = this
        #print(f"Step {j} passed")
    new_min_list = [-1]*len(nodes)
    for z in nodes: new_min_list[z.id] = z.min_way
    res = True
    #for q in range(len(nodes)):
        #if old_min_list[q] == new_min_list[q]: pass
        #else: res = False
    #if res==True: return True
    if old_min_list[len(nodes)-1] == new_min_list[len(nodes)-1]: return True

    for this in range(len(nodes)):
        for i in nodes[this].neighbors:
            way, cost = i[0], i[1]
            if nodes[this].min_way + cost < nodes[way].min_way:
                #print(f"Updated {this} -> {way}: {nodes[way].min_way}")
                nodes[way].min_way = nodes[this].min_way + cost
                nodes[way].min_from = this
                #print(f"Updated {this} -> {way}: {nodes[way].min_way}")
                # метка обновилась way=x
                y = way
                for i in range(len(nodes)):
                    y = nodes[y].min_from
                    #print(f"Step {i} from {len(nodes)} passed, y = {y}")
                path = deque()
                path.append(y)
                cur = y
                while True:
                    cur = nodes[cur].min_from
                    path.append(cur)
                    #print(path, len(path), cur)
                    time.sleep(0.1)
                    if len(path)>1 and cur==y:
                        break
                print("Найден отрицательный цикл: ")
                for i in path: print(i, end=" -> ")
                print(" ... ")
                print(" Алгоритм не выполняется корректно ")
                return False
    return True

if __name__ == "__main__":
    if input("1 - открыть файл со списком смежности, 0 - сгенерировать новый список: ")=='0':
        q = generate(True)
    else:
        project_name = input("Название файла для открытия: ")
        with open(f"graphs\\{project_name}.csv", mode="r", newline='\r\n', encoding='utf-8') as file:
            fileread = csv.reader(file, delimiter=',')
            q=[]
            for str in file:
                f = str.split(',')
                f[-1] = f[-1].split('\r')[0]
                if not(len(f)==1): q.append(f)
    size = len(q)

    nodes = refactor(q, size)
    if input("Вывести соединения на экран? Y/N ")=='y':
        for i in range(len(q)): nodes[i].print_me()

    start = 0

    (min_list, no_neg) = dijkstra(nodes, start)
    #print(no_neg)

    if no_neg == False:
        res = check_negar(nodes, min_list, start)
    elif no_neg==True or res==True:
        for z in nodes:
            if z!=0:
                print(f"Длина пути из 0 в {z.id}: {z.min_way}. 'Родитель' пункта {z.id}: {z.min_from}")
