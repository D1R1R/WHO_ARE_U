import natasha

segmenter = natasha.Segmenter()
emb = natasha.NewsEmbedding()
morph_tagger = natasha.NewsMorphTagger(emb)
syntax_parser = natasha.NewsSyntaxParser(emb)
ner_tagger = natasha.NewsNERTagger(emb)
morph_vocab = natasha.MorphVocab()

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
    markup_dict = {_.id: _.text for _ in markup.tokens}
    for span in doc.spans:
        for token in markup.tokens:
            for els in span.text.split():
                if els in token.text:
                    span.normalize(morph_vocab)
                    if token.head_id in markup_dict.keys():
                        return markup_dict[token.head_id].lower(), span.normal
                    return span.normal
                    break

def get_start(text: str):
    doc = natasha.Doc(text)

    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)
    return doc
