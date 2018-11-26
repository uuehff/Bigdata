# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import pymysql
import time



def common_elements(list1, list2):
    """判断两个list中的共同元素"""
    return [element for element in list1 if element in list2]


def art_select():
    print 'call function'
    conn = pymysql.connect(db="civil", user="hzj", password="123456", host="192.168.12.35",port = 3306,charset ='utf8mb4')
    print 'conn done!'
    cur = conn.cursor()
    batch_amount = 1
    total_amount = 17000000#2824916
    for start in range(6999998,total_amount,batch_amount):
        if start % 1000 == 0:
            print start
            time.sleep(1)

        sql = "SELECT uuid,id,trial_request,casedate_origin,judge_type FROM judgment WHERE id = %d"  % start
        #print start

        cur.execute(sql)

        for row in cur:
            uuid = row[0]

            dbid = row[1]

            trial_request = row[2]
            casedate = row[3]
            judge_type = row[4]
            if judge_type == '判决' and trial_request:
                #print start

                dft_idx = [] # defendent
                dft_no_idx = []
                qst_idx = [] # question

                plt =[]
                dft =[]
                qst =[]

                trial_lst = trial_request.split('。')#split by '\n' or '。'
                for idx,cnt in enumerate(trial_lst):

                    if ('答辩' in cnt or '辩称' in cnt):
                        dft_idx.append(idx)

                    if ('未' in cnt or '没' in cnt):
                        dft_no_idx.append(idx)

                    if ('质证' in cnt  or '主张' in cnt)  or ('原告' in cnt and '反驳' in cnt):
                        qst_idx.append(idx)

                if len(dft_idx) >0 :
                    # dft_no_idx = common_elements(dft_idx, dft_no_idx)
                    # if len(dft_no_idx)>0:
                    #
                    #     plt = trial_lst[:dft_no_idx[-1]] # change 0 to -1?
                    #     dft = trial_lst[dft_no_idx[-1]]
                    #     qst = trial_lst[min(dft_no_idx[-1]+1,len(trial_lst)):]

                    if len(qst_idx)>0:

                        plt = trial_lst[:dft_idx[0]]
                        dft = trial_lst[dft_idx[0]:qst_idx[0]]
                        qst = trial_lst[qst_idx[0]:]

                    else:
                        
                        plt = trial_lst[:dft_idx[-1]]
                        dft = trial_lst[dft_idx[-1]:]


                else:
                    plt = trial_lst[:]

                # print 'plt',''.join(plt)
                # print '\n'
                # print 'dft',''.join(dft)
                # print '\n'
                # print 'qst',''.join(qst)

                plt_text = ''.join(plt)
                dft_text = ''.join(dft)
                qst_text = ''.join(qst)

                # print type(judge_type)
                #
                trial_request = str(trial_request)
                # print 'org_text',trial_request
                # print '\n'
                # uuid = str(uuid)
                # dbid = str(dbid)
                # judge_type = str(judge_type)



                sql = "INSERT INTO `tmp_hzj` (`uuid`, `id`,`trial_request`,`plt_claim`,`dft_rep`,`crs_exm`,`judge_type`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cur.execute(sql,(uuid,dbid,trial_request,plt_text,dft_text,qst_text,judge_type))
                conn.commit()






    cur.close()
    conn.close()


art_select()
