Showdown is a Javascript Markdown to HTML converter, based on the original works by John Gruber. It can be used client side (in the browser) or server side (with Node or io).


# Installation

<div class="youtube-player" data-id="aSL-iIskEFU"></div>

## Download tarball

You can download the latest release tarball directly from [releases][releases]

## Bower

  bower install showdown

## npm (server-side)

  npm install showdown

## CDN

You can also use one of several CDNs available:

* github CDN

      https://cdn.rawgit.com/showdownjs/showdown/<version tag>/dist/showdown.min.js

* cdnjs

      https://cdnjs.cloudflare.com/ajax/libs/showdown/<version tag>/showdown.min.js


---------


# Here's some of the syntax supported


# Paragraphs

Paragraphs in Markdown are just one or more lines of consecutive text followed by one or more blank lines.

On July 2, an alien mothership entered Earth's orbit and deployed several dozen saucer-shaped "destroyer" spacecraft, each 15 miles (24 km) wide.

On July 3, the Black Knights, a squadron of Marine Corps F/A-18 Hornets, participated in an assault on a destroyer near the city of Los Angeles.

# Fancy D3

<div id="plot_lab" align="center"></div>

<div id="tooltip_lab">
    <p><strong>Speech Similarity: </strong><span id="sim">0</span></p>
    <p><span id="sp1">0</span></p>
    <p><span id="sp2">0</span></p>
</div>


<div id="plot_con" align="center"></div>

<div id="tooltip_con">
    <p><strong>Speech Similarity: </strong><span id="sim">0</span></p>
    <p><span id="sp1">0</span></p>
    <p><span id="sp2">0</span></p>
</div>


You can create a heading by adding one or more # symbols before your heading text. The number of # you use will determine the size of the heading. This is similar to [**atx style**][atx].

<pre><code class="coffeescript">
d3.json "http://josh-gree.me/static/data_lab.json", (data) ->
    # dimensions of SVG
    sims = data.sims
    labels = data.labels

    window.X = data

    pad = {left:0, top:50, right:0, bottom:120}

    w = window.innerHeight - pad.left - pad.right
    h = w - pad.top - pad.bottom

    svg = d3.select("div#plot")
        .append("svg")
        .attr("width", w + pad.left + pad.right)
        .attr("height", h + pad.top + pad.bottom)

    nvar = data.sims.length
    corXscale = d3.scaleBand().domain(d3.range(nvar)).range([0, w])
    corYscale = d3.scaleBand().domain(d3.range(nvar)).range([h, 0])
    corZscale = d3.interpolateViridis

    corr = []
    for i of sims
        for j of sims[i]
            corr.push {row:nvar - i - 1, col:j, value:sims[i][j], label:labels[i][j]}

    cells = svg.append("g").attr("id", "cells").selectAll("empty")
        .data(corr)
            .enter().append("rect")
            .attr("class", "cell")
            .attr("x", (d) -> corXscale(d.col))
            .attr("y", (d) -> corYscale(d.row))
            .attr("width", corXscale.bandwidth())
            .attr("height", corYscale.bandwidth())
            .attr("transform", "translate(" + pad.left + "," + pad.top + ")")
            .attr("fill", (d) -> corZscale(d.value))
            .attr("stroke", "none")
            .attr("stroke-width", 1)
            .on("mouseover", (d) ->
              x = parseFloat d3.select(this).attr('x')
              x = document.getElementById('plot').offsetLeft + x
              y = parseFloat d3.select(this).attr('y')
              y = document.getElementById('plot').offsetTop + y - 50
              d3.select(this).attr("stroke", "black")

              tt = d3.select("#tooltip")

              tt.style("left", x + "px")
              .style("top", y + "px")

              tt.select("span#sim")
              .text(d3.format(".2f")(d.value))

              labelss = d.label.split ','

              tt.select("span#sp1")
              .text(labelss[0])

              tt.select("span#sp2")
              .text(labelss[1])

              d3.select("#tooltip").classed("hidden", false)
              )
            .on("mouseout", ->
              d3.select(this).attr("stroke","none")
              d3.select("#tooltip").classed("hidden", true)
              )
            # .on("click", ->
            #   window.alert "Hello")
</pre></code>

# The largest heading
## The second largest heading
###### The 6th largest heading

You can also use [setext style][setext] headings.

This is an H1
=============

This is an H2
-------------

# Blockquotes

You can indicate blockquotes with a >.

In the words of Abraham Lincoln:

> Pardon my french


# Styling text

You can make text **bold** or *italic*.

*This text will be italic*

**This text will be bold**

Both bold and italic can use either a `*` or an `_` around the text for styling. This allows you to combine both bold and italic if needed.

**Everyone _must_ attend the meeting at 5 o'clock today.**


# Lists

## Unordered lists

You can make an unordered list by preceding list items with either a * or a -.

* Item
* Item
* Item

- Item
- Item
- Item

## Ordered lists

You can make an ordered list by preceding list items with a number.

1. Item 1
2. Item 2
3. Item 3


## Nested lists

You can create nested lists by indenting list items by two spaces.

1. Item 1
  1. A corollary to the above item.
  2. Yet another point to consider.
2. Item 2
  * A corollary that does not need to be ordered.
  * This is indented four spaces, because it's two spaces further than the item above.
  * You might want to consider making a new list.
3. Item 3


# Code formatting

## Inline formats

Use single backticks (\`) to format text in a special monospace format. Everything within the backticks appear as-is, with no other special formatting.

Here's an idea: why don't we take `SuperiorProject` and turn it into `**Reasonable**Project`.

You can also use triple backticks to format text as its own distinct block.


Check out this neat program I wrote:

```
x = 0
x = 2 + 2
what is x
```


# Links

Showdown supports two style of links: *inline* and *reference*.

## Inline

You can create an inline link by wrapping link text in brackets ( `[ ]` ), and then wrapping the link in parentheses ( `( )` ).

For example, to create a hyperlink to `showdown.github.io`, with a link text that says, Showdown is great!, you'd write this in Markdown:

[Showdown is great!](http://showdown.github.io/)

## Reference

Reference-style links use a second set of square brackets, inside which you place a label of your choosing to identify the link:

This is [an example][id] reference-style link.

Then, anywhere in the document (usually at the end), you define your link label like this, on a line by itself:

[id]: http://example.com/  "Optional Title Here"

## Maths
<div id="container">
<p id="button-row1">
<button id="start">Start</button>
<button id="stop">Stop</button>
<button id="restart">Clear</button>
<button id="rand">Random</button>
</p>
<canvas id="life" width="1220" height="620">Your browser does not support canvas.</canvas>

This should be an inline equation <span>\\\(y = m x + c\\\)</span> and then we should have some inline maths...

<div>
$$a x^2 + b x + c = 0$$
</div>

<pre><code class="python">
def doc_embedding(text):
    # tokenize
    tokenizer = RegexpTokenizer(r'\w+')
    text = [tokenizer.tokenize(txt.lower()) for txt in text]

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

    text = [[token for token in txt if token not in stop] for txt in text]

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

    return dictionary, corpus, corpus_tfidf, corpus_lsi, tfidf, lsi, c
</code></pre>


[sd-logo]: https://raw.githubusercontent.com/showdownjs/logo/master/dist/logo.readme.png
[releases]: https://github.com/showdownjs/showdown/releases
[atx]: http://www.aaronsw.com/2002/atx/intro
[setext]: https://en.wikipedia.org/wiki/Setext
