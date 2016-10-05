d3.json "http://josh-gree.me/static/data_con.json", (data) ->
    # dimensions of SVG
    sims = data.sims
    labels = data.labels

    window.X = data

    pad = {left:0, top:50, right:0, bottom:120}

    w = 600
    h = 600

    svg = d3.select("div#plot_con")
        .append("svg")
        .attr("width", w)
        .attr("height", h)

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
            .attr("fill", (d) -> corZscale(d.value))
            .attr("stroke", "none")
            .attr("stroke-width", 1)
            .on("mouseover", (d) ->

              x = parseFloat d3.select(this).attr('x')
              x = document.getElementById('plot_con').offsetLeft + x + 150
              y = parseFloat d3.select(this).attr('y')
              y = document.getElementById('plot_con').offsetTop + y + 50

              d3.select(this).attr("stroke", "black")

              tt = d3.select("#tooltip_con").classed("hidden", false)

              tt.style("left", x + "px")
              .style("top", y + "px")

              tt.select("span#sim")
              .text(d3.format(".2f")(d.value))

              labelss = d.label.split ','

              tt.select("span#sp1")
              .text(labelss[0])

              tt.select("span#sp2")
              .text(labelss[1])

              )
            .on("mouseout", ->
              d3.select(this).attr("stroke","none")
              d3.select("#tooltip_con").classed("hidden", true)
              )
            # .on("click", ->
            #   window.alert "Hello")