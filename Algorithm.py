import numpy as np
import math
np.set_printoptions(precision=4)

# 查看数组中重复元素并返回重复元素的索引值
def getDuplicationIndex(arr,equal):
    newList = []
    for element in arr:
        if element not in newList:
            newList.append(element)
        else:
            if equal is False:
                return arr.index(element)+1
            else:
                return arr.index(element)


# 此方法用于等级评价，将等级评价标准与待评估参数组成数组并进行排序，排序后待评估参数的索引值即为其等级
def indexGradeRating(criterion, param, equal):
    criterion.append(param)
    criterion.sort()
    if(len(criterion)>len(set(criterion))):
        indexGrade = getDuplicationIndex(criterion,equal)+1
    else:
        indexGrade = criterion.index(param)+1
    return indexGrade


def strRating(strCriterion,param):
    if param == strCriterion[0]:
        rating = 1
    elif param == strCriterion[1]:
        rating = 2
    elif param == strCriterion[2]:
        rating = 3
    elif param == strCriterion[3]:
        rating = 4
    # 处理特殊情况
    else:
        rating = 5
    return rating

# 对安全性指标A下属的三级子目标进行打分
def getGradeForA(param):
    A11 = indexGradeRating([0.23,0.65,0.81],param[0],True)
    A12 = indexGradeRating([0.33,0.68,0.79],param[1],True)
    A13 = indexGradeRating([0.18,0.62,0.78],param[2],True)
    A21 = indexGradeRating([0.61,0.71,0.75],param[3],True)
    A22 = indexGradeRating([0.61,0.71,0.75],param[4],True)

    if param[5]>0.82:
        A23 = 1
    elif param[5]<=0.82 and param[5]>0.62:
        A23 = 2
    elif param[5]<=0.62 and param[5]>0.28:
        A23 = 3
    else:
        A23 = 4

    return [A11,A12,A13],[A21,A22,A23]


# 对适用性指标S下属的三级子目标进行打分
def getGradeForS(param):
    s11 = strRating(['无振感', '有轻微振感', '有明显振感', '有剧烈振感'], param[0])
    s12 = strRating(['闸门无气蚀，通气孔面积满足要求', '闸门有轻微气蚀，通气孔面积不足',
                     '闸门有气蚀破坏，通气孔面积严重不足',
                     '闸门气蚀破坏严重，通气孔面积严重不足'], param[1])
    s13 = strRating(['平顺', '有水跃或波动', '存在打击闸门或漩涡', '存在严重打击或夹气'], param[2])

    s21 = strRating(['无', '轻微', '有破坏', '有严重破坏'], param[3])
    s22 = strRating(['优良', '合格', '一般', '不合格'], param[4])
    s23 = strRating(['优良', '合格', '维修更换后合格', '不合格'], param[5])
    s24 = strRating(['完好', '轻微破损', '有破损', '破损严重'], param[6])

    return [s11,s12,s13],[s21,s22,s23,s24]


# 对适用性指标N下属的三级子目标进行打分
def getGradeForN(param):
    N11 = indexGradeRating([0.3,0.45,0.8],param[0],True)
    N12 = indexGradeRating([0.12,0.48,0.72],param[1],True)
    N13 = indexGradeRating([0.25,0.5,0.75],param[2],True)
    N21 = indexGradeRating([0.1,0.3,0.6],param[3],True)
    N31 = strRating(['齐全','基本齐全','不全','无'],param[4])
    N32 = strRating(['遵守规程','基本遵守规程','未严格遵守规程','随意操作'],param[5])
    N33 = strRating(['定期检修','基本定期','不定期','无检修'],param[6])
    return [N11,N12,N13],[N21],[N31,N32,N33]


# 此方法通过模糊互补判断矩阵得到权重向量
def getWeights(Q):
    Q = np.array(Q)
    n = Q.shape[0]
    # print(Q)
    a = (n-1)/2
    weights = []
    # for i in range(0,Q.shape[0]):
    #     sum = 0
    #     for j in range(0,Q.shape[1]):
    #         sum += (1/(n*a))*Q[i][j]
    #     print(sum)
    #     w = (1/n)-(1/(2*a))+sum
    #     weights.append(w)
    for i in range(0,Q.shape[0]):
        sum = 0
        for j in range(0,Q.shape[1]):
            sum += Q[i][j]
        w = (1/n)-(1/(2*a))+(1/(n*a))*sum
        weights.append(w)
    return np.array(weights)


# 计算单指标和谐度矩阵
def getXHD(param):
    XHD = []
    for i in range(len(param)):
        row = [0,0,0,0]
        start = param[i]-1
        for j in range(start,len(row)):
            row[j] = 1
        XHD.append(row)
    return np.array(XHD)


# 通过和谐度矩阵和权重计算和谐度向量
def getYHD(weights,XHD):
    return np.dot(weights,XHD)


# 检查模糊矩阵的一致性
def isConsistent(Q):
    Q = np.array(Q)
    for i in range(Q.shape[0]):
        for j in range(Q.shape[1]):
            for k in range((Q.shape[1])):
                if (math.isclose(Q[i][j], Q[i][k]-Q[j][k]+0.5)==False):
                    return False
    return True


# 重新构造模糊一致矩阵
def correctInconsistency(Q):
    R = []
    Q = np.array(Q)
    for i in range(Q.shape[0]):
        sum = 0
        for j in range(Q.shape[1]):
            sum += Q[i][j]
        average = sum/Q.shape[1]
        print(average)
        R.append(average)

    correctedQ = np.zeros((Q.shape[0],Q.shape[1]))
    for m in range(Q.shape[0]):
        for n in range(Q.shape[1]):
            correctedQ[m][n] = (R[m]-R[n])/2 + 0.5

    return correctedQ.tolist()

#param：参数, QList：模糊判断矩阵， HD0：阈值
def getHealthGrade(param, QList = [],HD0 = 0.6):

    # #检查所有Q的一致性
    # for i in range(len(QList)):
    #     if (isConsistent(QList[i]) == False):
    #         QList[i] = correctInconsistency(QList[i])


    # 计算YAHD
    # 通过Q获得权重
    # weights_A1 = getWeights(QList[1])
    # weights_A2 = getWeights(QList[2])
    weights_A1 = np.array([0.5527,0.2962,0.1511])
    weights_A2 = np.array([0.2395,0.1593,0.6012])
    # 构建和谐度矩阵
    A1,A2 = getGradeForA(param[0:6])
    XHDA1 = getXHD(A1)
    XHDA2 = getXHD(A2)
    # XHDA1 = getXHD([3,4,2])
    # XHDA2 = getXHD([1,3,3])
    # 计算二级子目标的和谐度向量
    YHDA1 = getYHD(weights_A1,XHDA1)
    YHDA2 = getYHD(weights_A2,XHDA2)
    # weights_A = getWeights(QList[3])
    # 计算一级子目标的和谐度向量
    weights_A = np.array([0.4,0.6])
    YHDA = np.dot(weights_A,np.vstack([YHDA1,YHDA2]))

    # 计算YSHD
    # weights_s1 = getWeights(QList[4])
    # weights_s2 = getWeights(QList[5])
    weights_s1 = np.array([0.7600,0.1600,0.0800])
    weights_s2 = np.array([0.4483,0.2414,0.0690,0.2414])
    S1, S2 = getGradeForS(param[6:13])
    XHDS1 = getXHD(S1)
    XHDS2 = getXHD(S2)
    # XHDS1 = getXHD([3,1,3])
    # XHDS2 = getXHD([3,4,2,3])
    YHDS1 = getYHD(weights_s1,XHDS1)
    YHDS2 = getYHD(weights_s2,XHDS2)
    # weights_S= getWeights(QList[6])
    weights_S = np.array([0.463,0.537])

    # YsHD这个地方存在误差
    YHDS = np.dot(weights_S,np.vstack([YHDS1,YHDS2]))
    # YHDS = np.array([0.0741,0.1111,0.8704,1])


    # 计算YNHD
    # weights_N1 = getWeights(QList[7])
    # weights_N3 = getWeights(QList[8])
    weights_N1 = np.array([0.5496,0.2397,0.2107])
    weights_N2 = np.array([1])
    weights_N3 = np.array([0.1774,0.4326,0.39])

    N1,N2,N3 = getGradeForN(param[14:])
    XHDN1 = getXHD(N1)
    XHDN2 = getXHD(N2)
    XHDN3 = getXHD(N3)
    # XHDN1 = getXHD([3,3,4])
    # XHDN2 = getXHD([4])
    # XHDN3 = getXHD([3,2,3])
    YHDN1 = getYHD(weights_N1,XHDN1)
    YHDN2 = getYHD(weights_N2,XHDN2)
    YHDN3 = getYHD(weights_N3,XHDN3)
    # weights_N = getWeights(QList[9])
    weights_N = np.array([0.5658,0.1671,0.2671])
    temp1 = np.vstack([YHDN1,YHDN2])
    YHDN = np.dot(weights_N,np.vstack([temp1,YHDN3]))


    # 计算YPHD
    # weights = getWeights(QList[0])
    weights = np.array([0.5,0.2,0.3])
    temp2 = np.vstack([YHDA,YHDS])
    YpHD = np.dot(weights,np.vstack([temp2,YHDN]))
    # print(np.vstack([temp2,YHDN]))
    # print(YpHD)


    # 评价闸门等级
    HD0 = 0.6
    grade = 0
    for i in range(YpHD.shape[0]):
        if HD0 > YpHD[i]:
            grade += 1
        else:
            grade += 1
            break
    return grade

# ————————————————————————测试用——————————————————————————————————————————
# A1,A2 = getGradeForA([0.23,0.83,0.41,
#                       0.264,0.58,0.528])
# N1,N2,N3 = getGradeForN([0.69,0.528,0.76,0.72,"不全","基本遵守规程","不定期"])
# print(A1,A2)

# print(getWeights([[0.50,0.55,0.55,0.60,0.52,0.58],
#                   [0.45,0.50,0.50,0.55,0.47,0.53],
#                   [0.45,0.50,0.50,0.55,0.47,0.53],
#                   [0.40,0.45,0.45,0.50,0.42,0.48],
#                   [0.48,0.53,0.53,0.58,0.50,0.56],
#                   [0.42,0.473,0.47,0.52,0.44,0.50]]))
# print(correctInconsistency([[0,1],[1,1]]))

# print(isConsistent(np.array(correctInconsistency(
#                             [[0.50,0.6,0.6,0.7,0.5,0.7],
#                             [0.4,0.50,0.50,0.6,0.4,0.6],
#                             [0.4,0.50,0.50,0.6,0.4,0.6],
#                             [0.3,0.4,0.4,0.50,0.3,0.5],
#                             [0.5,0.6,0.6,0.7,0.5,0.5],
#                             [0.3,0.4,0.4,0.5,0.5,0.50]]))))
# ——————————————————————————————————————————————————————————————————————

if __name__ == '__main__':

    # grade 为闸门健康度评价结果
    grade = getHealthGrade([0.73, 0.83, 0.41, 0.264, 0.58, 0.528, '有明显振感',
                            '闸门无气蚀，通气孔面积满足要求', '闸门有轻微气蚀，通气孔面积不足',
                            '存在打击闸门或漩涡', '有破坏', '不合格', '合格', '有破损',
                            0.69, 0.528, 0.76, 0.72, '不全', '基本遵守规程', '不定期'],)
    print(grade)