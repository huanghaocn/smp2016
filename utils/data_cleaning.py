# coding=utf-8

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def getCosine(a, b):
    ab_sum = np.dot(a, b)
    a_sum_square = np.dot(a, a.T)
    b_sum_square = np.dot(b, b.T)
    if a_sum_square == 0 or b_sum_square == 0:
        return 0
    return float(ab_sum) / (np.sqrt(a_sum_square) * np.sqrt(b_sum_square))


with open("/home/qibai/Documents/PycharmProjects/smp2016/data/train/train_status.txt") as trainLines:
    data_cleaned_train_status = open("/home/qibai/Documents/smpData/train/cleaned_train_status.txt", 'w')
    vectorizer = CountVectorizer()
    weiboText = []
    count_vector_tweews = []
    text = ""
    uid = ""
    up_similarity = 0.9
    for line in trainLines:
        if uid == line.split(",")[0]:
            text += line.strip().split(",")[5] + " "
            weiboText.append(line.strip())
            continue
        if text != "":
            vectorizer.fit(text)
        for tweet in weiboText:
            count_vector_tweet = vectorizer.transform(tweet.split(",")[5])
            count_vector_tweews.append(count_vector_tweet.toarray())
        if len(count_vector_tweews) != 0:
            for i in range(len(count_vector_tweews) - 1):
                count_vector_tweet_i = count_vector_tweews[i]
                for j in range(i + 1, len(count_vector_tweews)):
                    count_vector_tweew_j = count_vector_tweews[j]
                    similarity = getCosine(np.array(count_vector_tweet_i), np.array(count_vector_tweew_j))
                    if similarity >= up_similarity:
                        break
                if similarity < up_similarity :
                    data_cleaned_train_status.write(weiboText[i] + '\n')
            data_cleaned_train_status.write(weiboText[len(count_vector_tweews) - 1] + '\n')
        uid = line.split(",")[0]
        text += line.strip().split(",")[5] + " "
        weiboText = []
        count_vector_tweews = []
        weiboText.append(line.strip())
