import docx
from PyPDF2 import PdfFileReader
import feedparser
import os
import pdf

from nltk.corpus.reader.plaintext import PlaintextCorpusReader

def read_docx(filename) :
    file = docx.Document(filename)
    content = []
    for p in file.paragraphs:
        content.append(p.text)
    return '\n'.join(content)

def read_pdf(filename, password = ''):
    pdf_file = open(filename, 'rb')
    read_pdf = PdfFileReader(pdf_file)
    if password:
        read_pdf.decrypt(password)
    content = []
    for i in range(read_pdf.getNumPages()-1):
        content.append(read_pdf.getPage(i).extractText())
    return '\n'.join(content)

def read_rss(url):
    feed = feedparser.parse(url)
    print("피드 제목:", feed['feed']['title'])
    print("포스트 수:", len(feed.entries))
    for i in range(len(feed.entries)):
        post = feed.entries[i]
        content = post.content
        print("포스트 제목:", post.title)
        print("포스트 원본:", content)


def get_text(filename):
    file = open(filename, 'r')
    return file.read()

def main():
    path = 'corpus/'
    if not os.path.isdir(path):
        os.mkdir(path)
    sample_1 = get_text("/Users/ahnwooseok/Downloads/github/2023-Konkuk-Univ-Graduation-Project/peter/file_nlp/sample_1.txt")
    sample_2 = pdf.getTextPDF("/Users/ahnwooseok/Downloads/github/2023-Konkuk-Univ-Graduation-Project/peter/file_nlp/sample_2.pdf")
    sample_3 = word.getTextWord("/Users/ahnwooseok/Downloads/github/2023-Konkuk-Univ-Graduation-Project/peter/file_nlp/sample_3.docx")

    files = [sample_1, sample_2, sample_3]
    for index, file in enumerate(files):
        with open(path+str(index)+'.txt', 'w') as fout:
            fout.write(f)
    corpus = PlaintextCorpusReader(path, '.*')


if __name__ == '__main__':
    main()
