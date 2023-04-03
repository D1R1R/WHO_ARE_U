import requests
import pymorphy2

url = 'https://query.wikidata.org/sparql'


class Question_analyzer():
    def __init__(self):
        self._morph = pymorphy2.MorphAnalyzer()

    def identifier(self, word):
        query = """
            PREFIX wd: <http://www.wikidata.org/entity/>
            SELECT DISTINCT ?qid
            WHERE {

              ?item rdfs:label "$"@ru .

              BIND(STRAFTER(STR(?item), STR(wd:)) AS ?qid) .

            }
            """.replace('$', word)
        return self.get_data(query.replace('$', word))

    def analyze(self, msg: str):
        msg = msg.lower()
        code_name = None
        name = None
        for word in msg.split():
            word = self._morph.parse(word)[0].normal_form
            if msg[:msg.index(':')] == 'место':
                word = word.capitalize()
            try:
                code_name = self.identifier(word)['results']['bindings'][0]['qid']['value']
                break
            except:
                continue
        if code_name:
            if msg[:msg.index(':')] == 'семья':
                try:
                    word = ' '.join(msg.split()[msg.split().index(word) + 1:])
                    word = self._morph.parse(word)[0].normal_form
                    word = ' '.join([x.capitalize() for x in word.split()])
                    name = self.identifier(word)['results']['bindings'][0]['qid']['value']
                    return self.family(code_name, name)
                except:
                    return 'Вы ввели некоректный запрос и я не смог его распознать. Попробуйте ввести /help'
            elif msg[:msg.index(':')] == 'место':
                return self.sity(code_name)
            elif msg[:msg.index(':')] == 'работа':
                try:
                    word = msg[msg.index('в') + 2:]
                    word = self._morph.parse(word)[0].normal_form
                    word = word.capitalize()
                    name = self.identifier(word)['results']['bindings'][0]['qid']['value']
                    return self.profession(code_name, name)
                except:
                    return 'Вы ввели некоректный запрос и я не смог его распознать. Попробуйте ввести /help'  
        return 'Вы ввели некоректный запрос и я не смог его распознать. Попробуйте ввести /help'

    def sity(self, sity_name):
        # Place: sity
        query = '''
            SELECT ?people ?peopleLabel
            WHERE
            {
            ?people wdt:P31 wd:Q5 .
            ?people wdt:P27 wd:$ .
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ru". }
            }
            LIMIT 15
        '''
        return self.answer_format(self.get_data(query.replace('$', sity_name)))

    def profession(self, code_name, prof):
        # Work: profession {в} sity
        query = '''
            SELECT ?people ?peopleLabel
            WHERE
            {
            ?people wdt:P31 wd:Q5 .
            ?people wdt:P27 wd:% .
            ?people wdt:P106 wd:$ .
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ru". }
            }
            LIMIT 15
        '''
        return self.answer_format(self.get_data(query.replace('$', code_name).replace('%', prof)))

    def family(self, code_name: str, name: str):
        # Family: pos name
        query = '''
            SELECT ?people ?peopleLabel
            WHERE
            {
            ?people wdt:$ wd:%.
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ru". }
            }
            LIMIT 15
        '''
        return self.answer_format(self.get_data(query.replace('$', code_name).replace('%', name)))
        
    def get_data(self, query):
        answer = requests.get(url, params={
            'format': 'json',
            'query': query})
        data = answer.json()
        return data
    
    def answer_format(self, str_json):
        answ = dict()
        for elements in str_json['results']['bindings']:
            answ[elements['peopleLabel']['value']] = elements['people']['value']
        return answ
