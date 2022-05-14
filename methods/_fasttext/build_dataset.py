from gensim.corpora import WikiCorpus
"""
https://dumps.wikimedia.org/idwiki/latest/idwiki-latest-pages-articles.xml.bz2
"""
dataset = WikiCorpus("idwiki-latest-pages-articles.xml.bz2", dictionary={})

with open("wiki-id-formatted.txt", 'w', encoding="utf8") as output:
    counter = 0
    for text in dataset.get_texts():
        output.write(' '.join(text) + "\n")
        counter = counter + 1
        if counter > 100000:
            break
