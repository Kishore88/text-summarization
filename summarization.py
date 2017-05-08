import sys
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import numpy

def LDA(data) :

   # list for tokenized documents in loop
   texts = []

   # create English stop words list
   en_stop = stopwords.words('english')

   ## Tokenizing
   tokenizer = RegexpTokenizer(r'\w+')

   # create English stop words list
   en_stop = stopwords.words('english')

   # loop through document list
   tokens = tokenizer.tokenize(data)
   stopped_tokens = [i for i in tokens if not i in en_stop]
   texts.append(stopped_tokens)

   # turn our tokenized documents into a id <-> term dictionary
   dictionary = corpora.Dictionary(texts)

   # convert tokenized documents into a document-term matrix
   corpus = [dictionary.doc2bow(text) for text in texts]

   ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=1, id2word = dictionary, passes=100)
   #ldamodel.print_topics(num_topics=1, num_words=20)
   list = ldamodel.show_topics(num_topics=20, formatted=False)
   topics = []
   for i in list[0][1]:
     topics.append(i[0])
   return topics


def summarize(data, top_sentences, n=400, cluster_threshold=8):
    print data
    # Adapted from "The Automatic Creation of Literature Abstracts" by H.P. Luhn
    #
    # Parameters:
    # * n  - Number of words to consider
    # * cluster_threshold - Distance between words to consider
    # * top_sentences - Number of sentences to return for a "top n" summary
            
    # Begin - nested helper function
    def score_sentences(sentences, important_words):
        scores = []
        sentence_idx = -1
    
        for s in [nltk.tokenize.word_tokenize(s) for s in sentences]:
    
            sentence_idx += 1
            word_idx = []
    
            # For each word in the word list...
            for w in important_words:
                try:
                    # Compute an index for important words in each sentence
                    word_idx.append(s.index(w))
                except ValueError as exc: # w not in this particular sentence
                    pass
    
            word_idx.sort()
    
            # It is possible that some sentences may not contain any important words
            if len(word_idx)== 0: continue
    
            # Using the word index, compute clusters with a max distance threshold
            # for any two consecutive words
    
            clusters = []
            cluster = [word_idx[0]]
            i = 1
            while i < len(word_idx):
                if word_idx[i] - word_idx[i - 1] < cluster_threshold:
                    cluster.append(word_idx[i])
                else:
                    clusters.append(cluster[:])
                    cluster = [word_idx[i]]
                i += 1
            clusters.append(cluster)
    
            # Score each cluster. The max score for any given cluster is the score 
            # for the sentence.
    
            max_cluster_score = 0
            for c in clusters:
                significant_words_in_cluster = len(c)
                total_words_in_cluster = c[-1] - c[0] + 1
                score = 1.0 * significant_words_in_cluster \
                    * significant_words_in_cluster / total_words_in_cluster
    
                if score > max_cluster_score:
                    max_cluster_score = score
    
            scores.append((sentence_idx, score))
    
        return scores    
    

    # It's entirely possible that this "clean page" will be a big mess. YMMV.
    # The good news is that the summarize algorithm inherently accounts for handling
    # a lot of this noise.
   
    sentences = [s for s in nltk.tokenize.sent_tokenize(data)]
    normalized_sentences = [s.lower() for s in sentences]

    words = [w.lower() for sentence in normalized_sentences for w in
             nltk.tokenize.word_tokenize(sentence)]

    top_n_words = LDA(data)
    print top_n_words
    scored_sentences = score_sentences(normalized_sentences, top_n_words)

    # approach would be to return only the top N ranked sentences

    top_n_scored = sorted(scored_sentences, key=lambda s: s[1])[-top_sentences:]
    top_n_scored = sorted(top_n_scored, key=lambda s: s[0])

    # Decorate the post object with summaries
    return dict(top_n_summary=[sentences[idx] for (idx, score) in top_n_scored])

