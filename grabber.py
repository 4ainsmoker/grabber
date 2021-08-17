import requests
import json
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud
from nltk.stem import PorterStemmer
import matplotlib.pyplot as plt


def saveData(obj, name: str):
    with open(f'{name}.pickle', 'wb') as f:
        pickle.dump(obj, f)


def loadData(filename: str):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
        return data


def textFilter(text: str):
    #производим нормализацию через лемматизацию или стэмминг
    normal = dict(lem=WordNetLemmatizer().lemmatize, stem=PorterStemmer().stem)
    #Cписок для отсчения конструкция can, when и т.д.
    stop_words = set(stopwords.words('english'))
    # Производим токенизацию и нормализацию слов
    return [normal['lem'](word) for word in word_tokenize(text) if word not in stop_words and word.isalpha()]


def grabber(url):
    text = ""

    if False:
        api_key = 'FORAPI' #ваш api
        r = requests.get(url + f'&apiKey={api_key}')
        saveData(r, 'response')
    else:
        r = loadData('response.pickle')
    json_text = json.loads(r.text)

    for obj in json_text['articles']:
        text += str(obj['description']).lower()

    filtered_text = textFilter(text)

    data_frequencies = {}
    for word in filtered_text:
        data_frequencies[word] = data_frequencies.get(word, 0) + 1
    result = dict(sorted(data_frequencies.items(), key=lambda i: i[1], reverse=True)[:50])
    word_cloud = WordCloud(width=1920, height=1080, max_words=50, background_color="white", relative_scaling=1,
                           normalize_plurals=False).generate_from_frequencies(result)
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    #API разработчика позволяет получить только 100 страниц
    params = 'language=en&q=russia&from=2021-08-01&pageSize=100'
    grabber(f'https://newsapi.org/v2/everything?{params}')
