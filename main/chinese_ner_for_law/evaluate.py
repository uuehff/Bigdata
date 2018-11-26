"""
Main Evaluation Metrics: macro f1 score
http://rushdishams.blogspot.com/2011/08/micro-and-macro-average-of-precision.html
"""
import codecs
import sys

def loadResults(FileName) :
    ret = []
    lines = codecs.open(FileName, encoding='utf-8')

    ret_t = {'ALL':[], 'PER':[], 'LOC':[], 'ORG':[], 'TIME':[], 'ROLE':[], 'CRIME':[]}
    ___t = []
    num = 0
    for line in lines :
        num += 1
        if line.__contains__("\r"):
            line = line[:-2]
        else:
            line = line[:-1]
        if not line=='' :
            chr_t, label_all = line.split(' ')
            label_t = label_all[0]

        if len(___t) > 0 and (line=='' or label_t in ['B', 'O']):
            str_t = ''.join(___t[1:])
            ret_t['ALL'].append(str_t)
            ret_t[___t[0]].append(str_t)
            ___t = []
        if line == '' :
            ret.append(ret_t)
            ret_t = {'ALL':[], 'PER':[], 'LOC':[], 'ORG':[], 'TIME':[], 'ROLE':[], 'CRIME':[]}
        elif label_t == 'O' :
            pass
        elif label_t == 'I' :
            if len(___t) == 0:
                label_type = label_all.split('-')[1]
                ___t.append(label_type)
                ___t.append(chr_t)
            else:
                assert len(___t) > 0
                ___t.append(chr_t)
        elif label_t == 'B' :
            if len(___t) == 0:
                label_type = label_all.split('-')[1]
                ___t.append(label_type)
                ___t.append(chr_t)
            else:
                assert len(___t) > 0
                ___t.append(chr_t)

    return ret

def evaluate(predictedFile, goldenFile) :
    result_pre = loadResults(predictedFile)
    result_gld = loadResults(goldenFile)
    assert len(result_pre) == len(result_gld)

    typeList = ['ALL', 'PER', 'LOC', 'ORG', 'TIME', 'ROLE', 'CRIME' ]
    TPs   = {'ALL':0, 'PER':0, 'LOC':0, 'ORG':0, 'TIME':0, 'ROLE':0, 'CRIME':0}
    TPFPs = {'ALL':0, 'PER':0, 'LOC':0, 'ORG':0, 'TIME':0, 'ROLE':0, 'CRIME':0}
    TPFNs = {'ALL':0, 'PER':0, 'LOC':0, 'ORG':0, 'TIME':0, 'ROLE':0, 'CRIME':0}

    for i in range(len(result_pre)) :
        pre_i, gld_i = result_pre[i], result_gld[i]
        for tp in typeList :
            TPs[tp]   += sum([(1 if word in pre_i[tp] else 0) for word in gld_i[tp]])
            TPFPs[tp] += len(pre_i[tp])
            TPFNs[tp] += len(gld_i[tp])

    harmonic_mean = lambda x, y : 2 / (1 / x + 1 / y)
    precisions, recalls, f1_ss = {}, {}, {}
    for tp in typeList :
        precisions[tp] = 100. * TPs[tp] / TPFPs[tp] if not TPs[tp] == 0 else 0
        recalls[tp]    = 100. * TPs[tp] / TPFNs[tp] if not TPs[tp] == 0 else 0
        f1_ss[tp]      = harmonic_mean(precisions[tp], recalls[tp]) if not precisions[tp] * recalls[tp] == 0 else 0
        print '%s:\tprecision: %.2f  recall: %.2f  f1_score: %.2f'%(tp, precisions[tp], recalls[tp], f1_ss[tp])

    # macro_f1 = harmonic_mean(macro_precision, macro_recall)
    # print 'macro_precision: %.2f'%(macro_precision)
    # print 'nmacro_recall:   %.2f'%(macro_recall)
    # print 'nmacro_f1:       %.2f'%(macro_f1)

if __name__ == '__main__':
    # evaluate("ner_pre","ner_dev1")
    evaluate(predictedFile=sys.argv[1], goldenFile=sys.argv[2])

