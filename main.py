import requests
import json
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def saveData(obj, name: str):
    with open(f'{name}.pickle', 'wb') as f:
        pickle.dump(obj, f)


def loadData(filename: str):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
        return data


def grabber(url):
    # api =
    # r = requests.get(url+f'&apiKey={api}')
    # saveData(r,'request')
    r = loadData('request.pickle')
    json_text = json.loads(r.text)
    # print(js)
    text = ""

    for obj in json_text['articles']:
        text += str(obj['content']).lower()

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words and word.isalpha() and word != 'chars']

    data_frequencies = {}

    for word in filtered_text:
        data_frequencies[word] = data_frequencies.get(word, 0) + 1

    dataFrequencies50 = dict(sorted(data_frequencies.items(), key=lambda f: -f[1])[:50])
    print(dataFrequencies50)
    word_cloud = WordCloud(width=900, height=500, max_words=50, background_color="white", relative_scaling=1,
                           normalize_plurals=False).generate_from_frequencies(dataFrequencies50)

    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


# response = requests.get('https://newsapi.org/v2/everything?q=russia&pageSize=100&page=10&from=2019-01-23&to=2019-01-23&apiKey=KEY')

if __name__ == '__main__':
    grabber('https://newsapi.org/v2/everything?q=russia&from=2021-08-01')
