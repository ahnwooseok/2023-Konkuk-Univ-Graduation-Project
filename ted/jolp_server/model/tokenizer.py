from konlpy.tag import Mecab

class CustomTokenizer:
    def __init__(self):
        self.tagger = Mecab()
    def __call__(self, sent):
        sent = sent[:1000000]
        word_tokens = self.tagger.morphs(sent)
        result = [word for word in word_tokens if len(word) > 1]
        return result