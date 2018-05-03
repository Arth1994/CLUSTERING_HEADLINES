from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
import os
import nltk

#nltk.download()
path = os.path.abspath(os.path.dirname(__file__))

stateDct={}
# Tokenizer to return stemmed words, we use this
def tokenize_and_stem(s):
    # declaring stemmer and stopwords language
    stemmer = SnowballStemmer("spanish", ignore_stopwords=True)
    stop_words = set(stopwords.words("spanish"))
    words = word_tokenize(s)
    filtered = [w for w in words if w not in stop_words and w != "<" and w != "!" and w != ">" and not w.isdigit()]
    stems = [stemmer.stem(t) for t in filtered]
    return stems

id = 0

def formatter(x, stop_words):
    global id
    id += 1
    stateDct[id] = str(x).split("<<<>>>")[0]
    return str(id)+"!!!! "+' '.join([word for word in x.split() if word not in stop_words])

def main():

    data = pd.read_csv(os.path.join(path, 'json.txt'), names=['text'])
    # text data in dataframe and removing stops words
    stop_words = set(stopwords.words('spanish'))
    #print(stop_words)
    data['text'] = data['text'].apply(lambda x: formatter(x,stop_words))
    #print(data)
    # Using TFIDF vectorizer to convert convert words to Vector Space
    tfidf_vectorizer = TfidfVectorizer(max_features=200000,
                                       use_idf=True,
                                       stop_words=None,
                                       tokenizer=tokenize_and_stem)


    
    # Fit the vectorizer to text data
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['text'])
    terms = tfidf_vectorizer.get_feature_names()
    #print(terms)

    # Kmeans++
    km = KMeans(n_clusters=10, init='k-means++', max_iter=300, n_init=1, verbose=0, random_state=3425)
    km.fit(tfidf_matrix)
    labels = km.labels_
    clusters = labels.tolist()
    
    # Calculating the distance measure derived from cosine similarity
    distance = 1 - cosine_similarity(tfidf_matrix)

    # Dimensionality reduction using Multidimensional scaling (MDS)
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    pos = mds.fit_transform(distance)
    xs, ys = pos[:, 0], pos[:, 1]

    # Saving cluster visualization after mutidimensional scaling
    for x, y, in zip(xs, ys):
        plt.scatter(x, y)
    plt.title('News Headlines after MDS')
    plt.savefig(os.path.join(path, 'MDS1.png'))

    # Creating dataframe containing reduced dimensions, identified labels and text data for plotting KMeans output
    df = pd.DataFrame(dict(label=clusters, data=(data['text']), x=xs, y=ys))
    df.to_csv(os.path.join(path, 'kmeans_dataframe1.txt'), sep='\t')

    label_color_map = {0: 'red',
                       1: 'blue',
                       2: 'green',
                       3: 'pink',
                       4: 'purple',
                       5: 'yellow',
                       6: 'orange',
                       7: 'gray',
                       8: 'olive',
                       9: 'cyan'
                       }

    csv = open(os.path.join(path, 'kmeans_clusters1.txt'), 'w')
    
    fig, ax = plt.subplots(figsize=(17, 9))

    mydict = {}
    lst = []
    for index, row in (df.iterrows()):
        cluster = row['label']
        label_color = label_color_map[row['label']]
        label_text = str(row['data'])
        ax.plot(row['x'], row['y'], marker='o', ms=12, c=label_color)
        row = label_text
        if cluster in mydict:
            mydict[cluster].append(row)
        else:
            lst = []
            lst.append(row)
            mydict[cluster] = lst
        #csv.write(row)
    
    for row in mydict.iteritems():
        for x in row[1]:
            temp = x.split("<<<>>>")[0]
            rowid = temp.split("!!!!")[0]
            writestr = str(row[0]) + "\t" + stateDct[int(rowid)] + "<<<>>>" + x.split("<<<>>>")[1]+ "\n"
            csv.write(writestr)

    for i in range(len(df)):
        ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['label'], size=8)

    plt.title('News Headlines using KMeans Clustering')
    plt.savefig(os.path.join(path, 'kmeans1.png'))


if __name__ == '__main__':
    main()