import natasha

segmenter = natasha.Segmenter()
emb = natasha.NewsEmbedding()
morph_tagger = natasha.NewsMorphTagger(emb)
syntax_parser = natasha.NewsSyntaxParser(emb)
ner_tagger = natasha.NewsNERTagger(emb)
morph_vocab = natasha.MorphVocab()

antonims = {
    "отец": "сын:дочь",
    "папа": "сын:дочь",
    "мать": "сын:дочь",
    "мама": "сын:дочь",
    "дети": "сын:дочь",
    "родители": "отец:мать",
    "дочь": "отец:мать",
    "сын": "отец:мать",
    "дочка": "отец:мать",
    "сын": "отец:мать",
    "жена": "муж",
    "муж": "жена",
    "дедушка": "бабушка",
    "бабушка": "дедушка",
    "брат": "сестра",
    "сестра": "брат",
}

def choose_type(text: str):
    request_type = None

    doc = get_start(text)
    for span in doc.spans:
        if span.type in {'PER', 'LOC'}:
            if request_type:
                request_type = None
                break
            request_type = span.type
    return request_type

def find_names(text: str):
    doc = get_start(text)
    markup = syntax_parser(text.split())
    # dictionary of dependent words
    markup_dict = {_.id: _.text for _ in markup.tokens}
    for span in doc.spans:
        for token in markup.tokens:
            for els in span.text.split():
                if els in token.text:
                    span.normalize(morph_vocab)
                    if token.head_id in markup_dict.keys():
                        code_name = markup_dict[token.head_id].lower()
                        # Case checking only for persons
                        if span.type == 'PER':
                            for sent in doc.sents:
                                for tokens in sent.morph.tokens:
                                    # Case checking
                                    if tokens.pos == 'PROPN' and tokens.feats['Case'] == 'Gen':
                                        try:
                                            code_name = antonims[code_name]
                                            break
                                        except:
                                            pass
                        return code_name, span.normal
                    return span.normal

def get_start(text: str):
    doc = natasha.Doc(text)

    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)
    return doc
