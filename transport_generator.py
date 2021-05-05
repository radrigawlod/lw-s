# Кузьмин Д.А.
# гр. ИБ-119

def ts_generator(return_it):
    import random
    import time
    import csv
    import numpy

    def account_medium(a, n):
        sum = 0
        for i in a:
            for j in i:
                if j != 0: sum += 1
        return sum / n

    def account_sum(z):
        count = 0
        for i in z:
            if i!=0: count+=1
        return count

    def count_medium(a, n, heaps):
        for i in range(len(a)):
            (heaps[account_sum(a[i])]).append(i)
        return heaps

    def print_medium(a, n, heaps):
        print(account_medium(a, n))
        for i in range(len(heaps)):
            if heaps[i] != []: print("{} связи: {} вершин".format(i, len(heaps[i])))

    def track(a, n):
        r1, r2_i, r2_j, r3, r3_id, ms = -1, -1, -1, 100000, -1, -1
        aa = numpy.array(a).T.tolist()
        for i in range(len(a)):
            if sum(a[i]) == 0: r1 = i
            if sum(a[i]) > ms: ms = sum(a[i])
            if sum(aa[i]) == 0:
                r3 = sum(aa[i])
                r3_id = i
        if r1 == -1 and r3 > 0: return [r1, r2_i, r2_j, r3, r3_id]
        excepts = []
        excepts.append(ms)
        while True:
            ms2 = -1
            for i in range(len(a)):
                if sum(a[i]) > ms2 and sum(a[i]) not in excepts: ms2 = sum(a[i])
            for i in range(len(a)):
                if sum(a[i]) == ms:
                    for j in range(len(a)-1):
                        if sum(a[j]) == ms2:
                            if a[i][j] != 0:
                                r2_i, r2_j = i, j
                                return [r1, r2_i, r2_j, r3, r3_id]
            excepts.append(ms2)
        return [r1, r2_i, r2_j, r3, r3_id]

    def heaps_enum(n):
        heaps = []
        for i in range(n):
            heaps.append([])
        return heaps

    def write_this(a, project_name, project_name2):
        with open(f"graphs\\{project_name}.csv", mode="w", encoding='utf-8') as w:
            fw = csv.writer(w, delimiter=',')
            for i in a:
                fw.writerow(i)
        print(f"Сохранено в файл {project_name} подпапки graphs")
        with open(f"graphs\\{project_name2}.csv",  mode="w", encoding='utf-8') as ww:
            fww = csv.writer(ww, delimiter=',')
            fww.writerow(("Source","Target","Label"))
            for i in range(len(a)):
                for j in range(len(a)):
                    if a[i][j]!=0: fww.writerow((i, j, a[i][j]))
        print(f"Сохранено в файл {project_name2} подпапки graphs")

    type_1 = 1 # ориентированный граф, всегда
    n = int(input("Количество пунктов в сети: "))
    medium = int(input("0, если значение среднего веса произвольно, иначе - требуемый вес: "))
    project_name = input("Если матрицу смежности сети нужно сохранить в файл, название файла: ")
    min_, max_ = map(int, input("Минимальное и максимальное значение веса ребра (пути): ").split())

    if medium == 0: medium = random.randrange(round(n / 10), round(n * 4 / 10))

    a = [[0] * n for i in range(n // 1)]
    q = 0
    vertices = 0
    this = 0
    heaps = heaps_enum(n)

    while q < medium:
        z = random.randrange(this, n)
        c = random.randrange(this, n)
        if z==0 and z!=c and a[z][c]==0 and a[c][z]==0:
            a[z][c] = random.randrange(min_, max_)
            if a[z][c]!=0:
                #print(f"[1] New edge {z} -> {c}")
                vertices +=1
                #print(f"[1] {a[c][z]}, {a[z][c]}")
        elif c==n-1 and z!=c and a[z][c]==0 and a[c][z]==0:
            a[z][c] = random.randrange(min_, max_)
            if a[z][c] != 0:
                #print(f"[2] New edge {z} -> {c}")
                vertices += 1
                #print(f"[2] {a[c][z]}, {a[z][c]}")
        elif z!=c and a[z][c]==0 and a[c][z]==0 and c!=0 and z!=n-1:
            a[z][c] = random.randrange(min_, max_)
            if a[z][c]!=0:
                #print(f"[3] New edge {z} -> {c}")
                vertices +=1
                #print(f"[3] {a[c][z]}, {a[z][c]}")
        elif z!=c and a[z][c] == 0 and a[c][z]!=0 and c!=0 and z!=n-1:
            a[z][c] = a[c][z]
            vertices += 1
            #print(f"[4] {a[c][z]}, {a[z][c]}")

            #print(f"[4] New edge {z} -> {c}")
        q = vertices / n
        #print(q)

    heaps = count_medium(a, n, heaps)
    print("Граф сгенерирован")

    #print(heaps)

    # if heaps[0] != 0:
    #     s_ = [-2, -2, -2, -2, -2]
    #     while True:
    #         t = track(a, n)
    #         for i in t: print(i)
    #         print(t)
    #         #break
    #         if t[0] != -1:
    #             if t[0] != n-1 and t[2] != 0:
    #                 a[t[1]][t[2]] = 0
    #                 a[t[0]][t[2]] = random.randrange(min_, max_)
    #                 print(f"[5] New edge {z} -> {c}")
    #             heaps = heaps_enum(n)
    #             heaps = count_medium(a, n, heaps)
    #             s_ = t
    #         elif s_[2] == t[4] and s_[4] == t[2]:
    #             print("!")
    #             break
    #         else:
    #             break

    if return_it == False:
        print_medium(a, n, heaps)

    if project_name != "":
        project_name2 = project_name+"_edges"
        write_this(a, project_name, project_name2)

    if return_it == True:
        return a

    return


if __name__ == "__main__":
    ts_generator(False)