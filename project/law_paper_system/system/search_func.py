'''

接口为search_api(query)，传入检索词句，返回检索结果

其中，检索结果为文书的列表，每个文书是一个列表，内容为：

[0.文书id，1.法院id，2.标题，3.案号，
 4.案件类型，5.审理程序，6.时间，7.原告，
 8.被告，9.文书性质，10.文书内容]
 
'''

import pymysql
import jieba.posseg as psg
import re
db = pymysql.connect('localhost', 'root', '', 'project')
cursor = db.cursor()

def search_location(place): #若place在location中，返回文书结果，否则返回空集
    sql = """SELECT location_id 
             FROM location
             WHERE province like '%%%s%%' or city like '%%%s%%' """ % (place,place)
    res = cursor.execute(sql)
    if res: #地点可以匹配到，则根据地点搜索
        location_id = cursor.fetchall() #元组的元组
        location_id = list(zip(*location_id))[0] #转为单个元组
        sql = """SELECT * FROM paper
                 WHERE court_id in (SELECT court_id FROM court
                                    WHERE location_id in %s""" % str(location_id)[:-2]+'));' #去掉元组最后的逗号，加上结尾
        cursor.execute(sql)
        return cursor.fetchall()
    return None

def search_court(court_name): #若name在法院名称中，返回文书结果，否则返回空集
    sql = """SELECT court_id 
             FROM court
             WHERE court_name like '%%%s%%'""" % court_name
    res = cursor.execute(sql)
    if res: #法院名称可以匹配到，则根据法院id搜索
        court_id = cursor.fetchall() #元组的元组
        court_id = list(zip(*court_id))[0] #转为单个元组
        sql = """SELECT * FROM paper
                 WHERE court_id in %s""" % str(court_id)[:-2]+');' #去掉元组最后的逗号，加上结尾
        cursor.execute(sql)
        return cursor.fetchall()
    return None

def search_case_type(type): #若type在案件类型中，返回文书结果，否则返回空集
    sql = """SELECT case_type 
             FROM case_type
             WHERE case_type like '%%%s%%'""" % type
    res = cursor.execute(sql)
    if res: #案件类型可以匹配到，则根据案件类型搜索
        case_type = cursor.fetchall() #元组的元组
        case_type = list(zip(*case_type))[0] #转为单个元组
        sql = """SELECT * FROM paper
                 WHERE case_type in %s""" % str(case_type)[:-2]+');' #去掉元组最后的逗号，加上结尾
        cursor.execute(sql)
        return cursor.fetchall()
    return None

def search_title(title): #匹配标题
    sql = """SELECT * FROM paper
             WHERE title like '%%%s%%';""" % title
    res = cursor.execute(sql)
    if res: return cursor.fetchall()
    return None

def search_in_content(content): #精确匹配
    sql = """SELECT * FROM paper
             WHERE content like '%%%s%%';""" % content
    res = cursor.execute(sql)
    return cursor.fetchall()

def minus(all, A): #结果的差集
    res = [each for each in all if each not in A]
    return res

def add(A, B): #结果的并集
    res = list(A)
    [res.append(each) for each in B if B not in A]
    return res

def intersect(A, B): #结果的交集
    res = [each for each in B if each in A]
    return res

def search_exact_match_one_word(query): #query是一个词，地点、法院名称、案件类型、标题、年份、文书内容，只能精确匹配
    place_res = search_location(query)
    if place_res != None: return place_res
    court_res = search_court(query)
    if court_res != None: return court_res
    case_type_res = search_case_type(query)
    if case_type_res != None: return case_type_res
    title_res = search_title(query)
    if title_res != None: return title_res
    return search_in_content(query)

def cut_word_match(query): #进行分词模糊匹配
    query = query.strip()
    word_flag_ls = list(psg.cut(query))
    if len(word_flag_ls) == 1: return search_exact_match_one_word(query)
    tmp_res = []
    res = search_title('')
    for pair in word_flag_ls:
        pair = list(pair)
        if pair[1].startswith('n') or pair[1].startswith('v') or pair[1].startswith('z'): #名词、动词、状态
            tmp = search_exact_match_one_word(pair[0]) #每个词的搜索结果
            tmp_res.append(tmp)
            res = intersect(res, tmp) #取交集，排在前面
    for tmp in tmp_res:
        [res.append(each) for each in tmp if each not in res]
    return res

def process_result(res): #处理检索结果，转为列表的列表
    new_res = []
    for each in res:
        tmp = list(each)
        tmp[6], tmp[10] = str(tmp[6])[:-9], re.sub(r'\*', '/n', tmp[10]).split('/n')
        tmp.append(tmp[10][:9])
        new_res.append(tmp)
    return new_res

def search(query): #query是一个词，地点、法院名称、年份、文书内容，若不是句式搜索，则进行分词模糊匹配
    cp = query
    try:
        #与或非句式搜索
        if query[0] == '^':
            query = query[1:].strip()
            return minus(search_title(''), search_in_content(query[1:].strip()))
        if '|' in query:
            queries = query.split('|')
            a = []
            for each in queries:
                a = add(a, search_exact_match_one_word(each.strip()))
            return a
        if '&' in query:
            queries = query.split('&')
            a = search_title('')
            for each in queries:
                a = intersect(a, search_exact_match_one_word(each.strip()))
            return a
        #分词模糊匹配
        return cut_word_match(query)
    except Exception as e:
        print(str(e))
        print('>>>出bug了，快记一下')
        print('>>>刚才搜的是：', cp)
        return []

def search_api(query):
    res = search(query)
    return process_result(res)

def delete_api(paper_id):
    sql = """DELETE FROM paper
             WHERE id = %s;""" % str(paper_id)
    try:
        cursor.execute(sql)
    except Exception as e:
        print(str(e))
        print('删除失败')
        db.rollback()
        return False
    db.commit()
    return True

def search_one_api(paper_id):
    sql = """SELECT * FROM paper
             WHERE id = %s;""" % str(paper_id)
    res = cursor.execute(sql)
    if res: res = cursor.fetchall()
    new_res = []
    for each in res:
        tmp = list(each)
        tmp[6], tmp[10] = str(tmp[6])[:-9], re.sub(r'\*', '/n', tmp[10]).split('/n')[1:]
        new_res.append(tmp)
    return new_res[0]

def get_num():
    sql = """SELECT COUNT(*) FROM paper;"""
    res = cursor.execute(sql)
    paper_num = cursor.fetchall()[0][0]
    sql = """SELECT COUNT(*) FROM court;"""
    res = cursor.execute(sql)
    court_num = cursor.fetchall()[0][0]
    return paper_num, court_num
