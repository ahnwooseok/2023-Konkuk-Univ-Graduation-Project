
import platform
from app import logger
class CustomTokenizer:
    def __init__(self):
        system = platform.system()
        if system == "Darwin":
            from konlpy.tag import Mecab
            self.tagger = Mecab()
        elif system == "Windows":  
            from eunjeon import Mecab
            self.tagger = Mecab()
    def __call__(self, sent):
        try:
            sent = sent[:1000000]
            word_tokens = self.tagger.pos(sent)
            result = [word[0] for word in word_tokens if word[1]  == "NNG"]
            return result
        except:
            logger.error(sent)
            return []
        