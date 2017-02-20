I recently came across an interesting [blog post](https://civisanalytics.com/blog/data-science/2016/01/15/data-science-on-state-of-the-union-addresses/) in which NLP (natural language processing) techniques were used to analyse all the US state of the union addresses from George Washington up until Obama's last address. The post references a much more advanced [historical analysis](http://www.pnas.org/content/112/35/10837.full) of these speeches in which they are used to understand how political discourse within the US has changed since the time of George Washington - a very interesting read! The image below shows the distinct streams of discourse found within the state of the union addresses.

![Evolution of political discourse in the US](http://www.pnas.org/content/112/35/10837/F5.large.jpg)

Upon reading this post I came up with a plan to learn some NLP and to indulge my obsession with UK politics. The first thing I needed to decide was on the kind of text I would analyse - the closest analogue to the US state of the union is perhaps the speech given at the state opening of parliament by the current monarch.

![Queens Speech](http://ichef.bbci.co.uk/news/660/media/images/81948000/jpg/_81948322_009375262-1.jpg)

These speeches are however written by the government and spoken by the monarch, they usually consist mainly of a list of upcoming legislation and are generally devoid of much personality - there are certain things that the monarch would never be asked to say which a politician would be happy to say! They are also rather difficult to get hold of without hunting through hansard (the UK parliaments record of daily business) which is not as yet completely digitised! There is no official statement given by the Prime Minister each year but what we do have is the party conference speeches which are given each year by the leaders of the main political parties. I was able to scrape these speeches, using [Scrapy](https://scrapy.org/) from [here](http://www.britishpoliticalspeech.org/speech-archive.htm). Now this collection of speeches is far from complete and does not extend as far into the past as the US state of the union but it is mostly complete from 1900 onwards. The most glaring absence is that of Winston Churchill since his family have rather zealously protected his public speeches using copyright an interesting podcast discussing this topic can be found [here](http://freakonomics.com/podcast/who-owns-the-words-that-come-out-of-your-mouth-a-new-freakonomics-radio-podcast/) - in my opinion it beggars belief that it is possible to enforce copyright on public speeches but hey ho anything to make some money!

## Analysis of the speeches

My analysis of the conference speeches is more or less identical to that used in the state of the union blog post. I want to come up with a similarity score for each pair of speeches and make a pretty interactive plot that shows this information - yay I get to play with [D3.js](https://d3js.org/). Hopefully we will be able to see some instances of interesting changes in content throughout the 20th century. In order to come up with a similarity rating the following steps were needed;

- Clean the text and tokenise.
- Remove extremely common words that add little discriminative value.
- Form bag of words vectors - each text is represented by the counts of the words it contains.
- Weight these vectors using text frequency inverse document frequency weighting - this takes into account document length and tries to give more discriminative power.
- Obtain a lower dimensional representation of the vectors - using singular value decomposition.
- Calculate similarity using cosine distance between text vectors.

All these steps were achieved using [Gensim](https://radimrehurek.com/gensim/) a python library that enables easy semantic modelling of text along with [NLTK](http://www.nltk.org/) a library that provides various tools for working with text. Starting from a list of strings for each speech the following code gets the similarity scores;

<pre><code class="python">

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from collections import Counter
from gensim import corpora, models, similarities

# tokenize
tokenizer = RegexpTokenizer(r'\w+')
texts = [tokenizer.tokenize(txt.lower()) for txt in texts]

# remove stop words
stop = set(stopwords.words('english'))
stop.add('applause')
stop.add('us')
stop.add('one')
stop.add('cheers')
stop.add('laughter')
stop.add('hear')
stop.add('madam')
stop.add('mrs')
stop.add('cent')
stop.add('ed')
stop.add('say')

texts = [[token for token in txt if token not in stop] for txt in texts]

# remove single count words
c = Counter()
[c.update(txt) for txt in text]
text = [[token for token in txt if c[token] > 1] for txt in text]

# create dictionary word -> id
dictionary = corpora.Dictionary(text)

# one hot document encoding
corpus = [dictionary.doc2bow(txt) for txt in text]

# tfidf model
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

# lsi model
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100)
corpus_lsi = lsi[corpus]

# calculate similarities
index = similarities.MatrixSimilarity(corpus_lsi)
sims = np.array([index[lsi[corp]] for corp in corpus])
</pre></code>  

## visualisation
I grouped the speeches by political party and created three interactive plots. The first plot shows the similarities between speeches given by leaders of the labour party.

## Labour party conference speeches.
<div id="plot_lab" align="center"></div>

<div id="tooltip_lab" class="hidden">
    <p><strong>Speech Similarity: </strong><span id="sim">0</span></p>
    <p><span id="sp1">0</span></p>
    <p><span id="sp2">0</span></p>
</div>
</br>
</br>

The similarities between the speeches given by leaders of the Conservative party are shown below;

## Conservative party conference speeches.
<div id="plot_con" align="center"></div>

<div id="tooltip_con" class="hidden">
    <p><strong>Speech Similarity: </strong><span id="sim">0</span></p>
    <p><span id="sp1">0</span></p>
    <p><span id="sp2">0</span></p>
</div>

</br>
</br>

And finaly for the leaders of the Liberal Democrats;

## Liberal Democrat party conference speeches.
<div id="plot_libdem" align="center"></div>

<div id="tooltip_libdem" class="hidden">
    <p><strong>Speech Similarity: </strong><span id="sim">0</span></p>
    <p><span id="sp1">0</span></p>
    <p><span id="sp2">0</span></p>
</div>

</br>
</br>

I also scraped the data for the US state of the union speeches from [here](http://stateoftheunion.onetwothree.net/texts/index.html) and created an interactive plot for those too!

## State of the union
<div id="plot_sou" align="center"></div>

<div id="tooltip_sou" class="hidden">
    <p><strong>Speech Similarity: </strong><span id="sim">0</span></p>
    <p><span id="sp1">0</span></p>
    <p><span id="sp2">0</span></p>
</div>

</br>
</br>

All my analysis and visualisation code can be found on Github [here](https://github.com/josh-gree/conf_speeches).
