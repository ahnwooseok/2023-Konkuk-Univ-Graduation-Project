def getText(filename):
    import docx

    doc = docx.Document(filename)

    fullText = []

    for para in doc.paragraphs:
        fullText.append(para.text)

    return "\n".join(fullText)


print(getText("zzzz.docx"))
