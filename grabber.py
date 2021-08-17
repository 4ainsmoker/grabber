import requests
import json
import pickle
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


def textFilter(text: str):
    #Cписок для отсчения конструкция can, when и т.д.
    stop_words = set(stopwords.words('english'))
    # Производим токенизацию
    word_tokens = word_tokenize(text)
    return [word for word in word_tokens if word not in stop_words and word.isalpha() and word != 'chars']


def grabber(url):
    if False:
        api_key = 0  # ваш api key
        r = requests.get(url + f'&apiKey={api_key}')
        saveData(r, 'request')
    else:
        r = loadData('request.pickle')
    json_text = json.loads(r.text)
    # print(js)
    text = ""

    for obj in json_text['articles']:
        text += str(obj['content']).lower()

    filtered_text = textFilter(text)

    data_frequencies = {}

    for word in filtered_text:
        data_frequencies[word] = data_frequencies.get(word, 0) + 1

    result = dict(sorted(data_frequencies.items(), key=lambda i: i[1], reverse=True)[:50])
    print(result)
    word_cloud = WordCloud(width=1920, height=1080, max_words=50, background_color="white", relative_scaling=1,
                           normalize_plurals=False).generate_from_frequencies(result)
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    params = 'country=us&language=en&q=russia&from=2021-08-01'
    grabber(f'https://newsapi.org/v2/everything?{params}')