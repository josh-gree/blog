<pre><code class="python">
texts = ["The cat sat on the mat",
         "The feline perched on the rug",
         "It was his right",
         "He went to the right"]
</pre></code>

<pre><code class="python">
# got rid of capitals and split each text into a list of words
texts = [text.lower().split() for text in texts]
texts

[['the', 'cat', 'sat', 'on', 'the', 'mat'],
 ['the', 'feline', 'perched', 'on', 'the', 'rug'],
 ['it', 'was', 'his', 'right'],
 ['he', 'went', 'to', 'the', 'right']]
</pre></code>

<pre><code class="python">
# remove very common words
stop_words = ["the","on","was"]
texts = [[token for token in txt if token not in stop_words] for txt in texts]
texts

[['cat', 'sat', 'mat'],
 ['feline', 'perched', 'rug'],
 ['it', 'his', 'right'],
 ['he', 'went', 'to', 'right']
</pre></code>

<pre><code class="python">
# create a dictionary for all unique words in all texts
# this is just a mapping word -> int
all_words = set(reduce(add,texts))
dictionary = dict(zip(all_words,range(len(all_words))))
dictionary

{'cat': 5,
 'feline': 3,
 'he': 10,
 'his': 0,
 'it': 2,
 'mat': 1,
 'perched': 8,
 'right': 7,
 'rug': 4,
 'sat': 11,
 'to': 6,
 'went': 9}
</pre></code>

<pre><code class="python">
# can now represent each text as a bag of words vector
import numpy
text_vecs = numpy.zeros((len(texts),len(all_words)))

for ind,text in enumerate(texts):
    for word in text:
        text_vecs[ind,dictionary[word]] += 1

text_vecs

array([[ 0.,  1.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  1.],
       [ 0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  1.,  0.,  0.,  0.],
       [ 1.,  0.,  1.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  1.,  1.,  0.,  1.,  1.,  0.]])
</pre></code>


<pre><code class="python">
u = text_vecs[0,:] # The cat sat on the mat
v = text_vecs[1,:] # The feline perched on the rug

similarity = 1 - distance.cosine(u,v)
similarity

0.0
</pre></code>

<pre><code class="python">
u = text_vecs[2,:] # It was his right
v = text_vecs[3,:] # He went to the right

similarity = 1 - distance.cosine(u,v)
similarity

0.28867513459481287
</pre></code>

<div id="plot_lab" align="center"></div>

<div id="tooltip_lab" class="hidden">
    <p><strong>Speech Similarity: </strong><span id="sim">0</span></p>
    <p><span id="sp1">0</span></p>
    <p><span id="sp2">0</span></p>
</div>
</br>
</br>


<div id="plot_con" align="center"></div>

<div id="tooltip_con" class="hidden">
    <p><strong>Speech Similarity: </strong><span id="sim">0</span></p>
    <p><span id="sp1">0</span></p>
    <p><span id="sp2">0</span></p>
</div>
</br>
</br>


<div id="plot_libdem" align="center"></div>

<div id="tooltip_libdem" class="hidden">
    <p><strong>Speech Similarity: </strong><span id="sim">0</span></p>
    <p><span id="sp1">0</span></p>
    <p><span id="sp2">0</span></p>
</div>
