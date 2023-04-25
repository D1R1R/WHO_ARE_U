import requests

import analyzer


url = 'https://query.wikidata.org/sparql'


class Question_analyzer():
    def identifier(self, word):
        # getting prefixs
        # normal word -> Wikidata id
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
        # type of request      
        reqest_type = analyzer.choose_type(msg)
        if reqest_type:
            if reqest_type == "PER":
                code_name, name = analyzer.find_names(msg)
                # For persons in Gen Case
                for idx in code_name.split(':'):
                    try:
                        idx = self.identifier(idx)['results']['bindings'][0]['qid']['value']
                        name = self.identifier(name)['results']['bindings'][0]['qid']['value']
                        return self.family(idx, name)
                    except:
                        return 'Вы ввели некоректный запрос и я не смог его распознать. Попробуйте ввести /help'
            elif reqest_type == "LOC":
                code_name, name = analyzer.find_names(msg)
                try:
                    code_name = self.identifier(code_name)['results']['bindings'][0]['qid']['value']
                    name = self.identifier(name)['results']['bindings'][0]['qid']['value']
                    return self.profession(code_name, name)
                except:
                    try:
                        name = self.identifier(name)['results']['bindings'][0]['qid']['value']
                        return self.sity(name)
                    except:
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
        # Work: profession in sity
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
            LIMIT 10
        '''
        return self.answer_format(self.get_data(query.replace('$', code_name).replace('%', name)))
        
    def get_data(self, query):
        # request to Wikidata
        answer = requests.get(url, params={
            'format': 'json',
            'query': query})
        data = answer.json()
        return data
    
    def answer_format(self, str_json):
        # format json
        answ = dict()
        for elements in str_json['results']['bindings']:
            answ[elements['peopleLabel']['value']] = elements['people']['value']
        return answ
import requests

import analyzer


url = 'https://query.wikidata.org/sparql'


class Question_analyzer():
    def identifier(self, word):
        # getting prefixs
        # normal word -> Wikidata id
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
        # type of request      
        reqest_type = analyzer.choose_type(msg)
        if reqest_type:
            if reqest_type == "PER":
                code_name, name = analyzer.find_names(msg)
                # For persons in Gen Case
                for idx in code_name.split(':'):
                    try:
                        idx = self.identifier(idx)['results']['bindings'][0]['qid']['value']
                        name = self.identifier(name)['results']['bindings'][0]['qid']['value']
                        return self.family(idx, name)
                    except:
                        return 'Вы ввели некоректный запрос и я не смог его распознать. Попробуйте ввести /help'
            elif reqest_type == "LOC":
                code_name, name = analyzer.find_names(msg)
                try:
                    code_name = self.identifier(code_name)['results']['bindings'][0]['qid']['value']
                    name = self.identifier(name)['results']['bindings'][0]['qid']['value']
                    return self.profession(code_name, name)
                except:
                    try:
                        name = self.identifier(name)['results']['bindings'][0]['qid']['value']
                        return self.sity(name)
                    except:
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
        # Work: profession in sity
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
            LIMIT 10
        '''
        return self.answer_format(self.get_data(query.replace('$', code_name).replace('%', name)))
        
    def get_data(self, query):
        # request to Wikidata
        answer = requests.get(url, params={
            'format': 'json',
            'query': query})
        data = answer.json()
        return data
    
    def answer_format(self, str_json):
        # format json
        answ = dict()
        for elements in str_json['results']['bindings']:
            answ[elements['peopleLabel']['value']] = elements['people']['value']
        return answ
