# -*- coding: utf-8 -*-

def t(x):
    t = [['B-TIME',"1"],['B-TIME',"2"],['I-TIME',"3"],['B-ORG',"4"],['B-ROLE',"5"],['B-LOC',"7"]]
    l2 = []
    l3 = []
    l22 = []
    l23 = []
    c = 0
    ttl = ""
    for i in t:
        if i[0].startswith('B') and c == 0:
            l2.append(i[0])
            l3.append(i[1].decode("utf-8"))
            ttl = i[0].replace('B', 'I')
            c = c + 1

        elif i[0] == ttl:
            l2.append(i[0])
            l3.append(i[1].decode("utf-8"))
        elif i[0].startswith('B') and c != 0:
            l22.append(l2)
            l23.append("".join(l3))
            l2 = []
            l3 = []
            l2.append(i[0])
            l3.append(i[1].decode("utf-8"))
            ttl = i[0].replace('B', 'I')
    l22.append(l2)
    l23.append("".join(l3))

    # taglist = ['B_ROLE','I_ROLE','B_PER','I_PER','B_CRIME','I_CRIME','B_TIME','I_TIME','B_ORG','I_ORG','B_LOC','I_LOC']
    ret_t = {'PER': [], 'LOC': [], 'ORG': [], 'TIME': [], 'ROLE': [], 'CRIME': []}
    # index_tag {0: 'PAD', 1: 'O', 2: 'B-ROLE', 3: 'I-ROLE', 4: 'B-PER', 5: 'I-PER', 6: 'B-CRIME', 7: 'I-CRIME', 8: 'B-TIME',
    #  9: 'I-TIME', 10: 'B-ORG', 11: 'I-ORG', 12: 'B-LOC', 13: 'I-LOC'}
    id = 0
    for i in l22:
        ret_t[i[0].split("-")[1]].append(l23[id])
        id += 1

    t2 = []
    for i in ret_t.keys():
        tmp = ("rowkey", ["rowkey", "d", i, ",".join(ret_t[i])])
        t2.append(tmp)
    for i in t2:
        print i[1][2],i[1][3]
    #
    # return t2
    #     # return "-"


if __name__ == "__main__":

    # t = []
    # for i in range(14):
    #     t.app
    t("x")