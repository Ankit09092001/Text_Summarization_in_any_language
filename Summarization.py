import spacy
from spacy.lang.en.stop_words import STOP_WORDS
# Stop words woh word h jinko hata diya toh sentence ke meaning ko farak nhi padega.
from string import punctuation
from heapq import nlargest
from flask import Flask,request

app = Flask(__name__)

text = """Wikipedia[note 3] is a multilingual free online encyclopedia written and maintained by a community of volunteers, known as Wikipedians, through open collaboration and using a wiki-based editing system called MediaWiki. Wikipedia is the largest and most-read reference work in history.[3] It is consistently one of the 10 most popular websites ranked by Similarweb and formerly Alexa; as of 2023, Wikipedia was ranked the 5th most popular site in the world according to Semrush.[4] It is hosted by the Wikimedia Foundation, an American non-profit organization funded mainly through donations.

Wikipedia was launched by Jimmy Wales and Larry Sanger on January 15, 2001. Sanger coined its name as a blend of wiki and encyclopedia. Wales was influenced by the "spontaneous order" ideas associated with Friedrich Hayek and the Austrian School of economics after being exposed to these ideas by the libertarian economist Mark Thornton.[5] Initially available only in English, versions in other languages were quickly developed. Its combined editions comprise more than 60 million articles, attracting around 2 billion unique device visits per month and more than 15 million edits per month (about 5.7 edits per second on average) as of January 2023.[6][7] In 2006, Time magazine stated that the policy of allowing anyone to edit had made Wikipedia the "biggest (and perhaps best) encyclopedia in the world".[8]"""

stopwords = list(STOP_WORDS)
# print(stopwords)

@app.route('/summarize', methods = ['GET','POST'])
def summarizer():
    # Taking input from nlp
    rawdoc = request.form['rawdoc']
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(rawdoc)
    # print(doc)

    # Tokenization of words
    tokens = [token.text for token in doc]
    # print(tokens)

    # Word frequency after neglecting stop words and punctuation
    word_freq={}

    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    # print(word_freq)

    # Checking maximum frequency of word in doc
    max_freq = max(word_freq.values())
    # print(max_freq)

    # Dividing the max frequency with all frequency to normalize the frequency
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    # Tokenization of sentences
    sent_tokens = [sent for sent in doc.sents]
    # print(sent_tokens)


    # Sentence frequency
    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]   
    # print(sent_scores)


    # It decides the percentage of summarization, here it is 30% percent
    select_len = int(len(sent_tokens) * 0.3)


    # List of summarized text that is done in order of higher frequency of sentences
    summary = nlargest(select_len, sent_scores, sent_scores.get)
    # print(summary)


    # Converting summarized list into summarized para
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    print(summary)
    return summary

if __name__ == '__main__':
    app.run(debug=True)