# coding=utf-8

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import codecs
from sklearn import neighbors
knn = neighbors.KNeighborsClassifier() #取得knn分类器
data = np.array([[3,104],[2,100],[1,81],[101,10],[99,5],[98,2]]) # <span style="font-family:Arial, Helvetica, sans-serif;">data对应着打斗次数和接吻次数</span>
labels = np.array([1,1,1,2,2,2]) #<span style="font-family:Arial, Helvetica, sans-serif;">labels则是对应Romance和Action</span>
knn.fit(data,labels) #导入数据进行训练'''
knn.predict([18,90])
import gensim
model = gensim.models.Word2Vec.load_word2vec_format("/home/qibai/Documents/smpData/smp_vector.bin",binary=True)
for key,val in model.most_similar(u"中国",topn=40):
    print key+" "+str(val)


# def getCosine(a, b):
#     ab_sum = np.dot(a, b.T)
#     a_sum_square = np.dot(a, a.T)
#     b_sum_square = np.dot(b, b.T)
#     if a_sum_square == 0 or b_sum_square == 0:
#         return 0
#     return float(ab_sum) / (np.sqrt(a_sum_square) * np.sqrt(b_sum_square))
#
#
# def duplicateDetection(origin="../data/train/train_status.txt",
#                        output="../data/train/cleaned_train_status.txt",
#                        up_similarity=0.9):
#     """
#
#     :param origin: origin file for duplicate detection
#     :param output: the file path for save remove duplicate tweets
#     :param up_similarity: the param to control
#     :return:
#     """
#     with codecs.open(origin) as trainLines, \
#             open(output, 'w') as data_cleaned_train_status:
#         vectorizer = CountVectorizer()
#         weiboText = []
#         count_vector_tweets = []
#         text = []
#         uid = ""
#         num = 0
#         for line in trainLines:
#             if uid == line.split(",")[0]:
#                 text.append(line.strip().split(",")[5])
#                 weiboText.append(line.strip())
#                 continue
#             if len(text) != 0:
#                 count_matrixs = vectorizer.fit_transform(text)
#                 for i in range(count_matrixs.shape[0]):
#                     count_vector_tweets.append(count_matrixs[i].toarray())
#             if len(count_vector_tweets) != 0:
#                 for i in range(len(count_vector_tweets) - 1):
#                     similarity = 0
#                     count_vector_tweet_i = count_vector_tweets[i]
#                     for j in range(i + 1, len(count_vector_tweets)):
#                         count_vector_tweet_j = count_vector_tweets[j]
#                         similarity = getCosine(np.array(count_vector_tweet_i), np.array(count_vector_tweet_j))
#                         if similarity >= up_similarity:
#                             num += 1
#                             print "delete %s rows", num
#                             break
#                     if similarity < up_similarity:
#                         data_cleaned_train_status.write((weiboText[i] + '\n'))
#                 data_cleaned_train_status.write(weiboText[len(count_vector_tweets) - 1] + '\n')
#             uid = line.split(",")[0]
#             text = []
#             text.append(line.strip().split(",")[5])
#             weiboText = []
#             count_vector_tweets = []
#             weiboText.append(line.strip())
#
#
# if __name__ == '__main__':
#     duplicateDetection(origin="../data/train/train_status.txt",
#                        output="../data/train/cleaned_train_status.txt",
#                        up_similarity=0.9)
