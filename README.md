# grabber
## Задание
Представим, что Вы готовите слайд для презентации об актуальных трендах в англоязычных новостях, касающихся России.

С сайта google news (https://news.google.com) (язык и регион - English | United States) необходимо
прокачать все статьи за последний месяц (на момент прокачки) с ключевым словом Russia.
Затем для скачанных статей необходимо рассчитать топ-50 упоминаемых тем и представить их в виде word (tag) cloud.

Данное задание необходимо выполнить с помощью Python.
Для представления в виде word cloud можно использовать уже существующие библиотеки.
Пример word cloud можно посмотреть по [ссылке](https://altoona.psu.edu/sites/altoona/files/success-word-cloud.jpg).
### Решение 
- Для извлечения контента из статей был выбран API Google. (В режиме разработчика позволяет загружать до 100 страниц и нельзя получить полный текст статьи.)
- Извлеченные данные необходимо обработать. В данных целях используется библиотека nltk, позволяющая нормализовать слова и избавиться от "стоп-слов".
- Далее, подготовленные и нормализованные слова подсчитываются в словаре, где в качестве ключа используется слово, а в качестве значения указывается количество повторений.

Подготовка извлеченных данных:
```
def textFilter(text: str):
    #производим нормализацию через лемматизацию или стэмминг
    normal = dict(lem=WordNetLemmatizer().lemmatize, stem=PorterStemmer().stem)
    #Cписок для отсчения конструкция can, when и т.д.
    stop_words = set(stopwords.words('english'))
    # Производим токенизацию и нормализацию слов
    return [normal['stem'](word) for word in word_tokenize(text) if word not in stop_words and word.isalpha()]
```
Подсчет наиболее часто встречающихся слов:
```
    data_frequencies = {}
    for word in filtered_text:
        data_frequencies[word] = data_frequencies.get(word, 0) + 1
    result = dict(sorted(data_frequencies.items(), key=lambda i: i[1], reverse=True)[:50])
```
### Результат
![Image Alt](https://github.com/4ainsmoker/grabber/blob/master/lem.png)
