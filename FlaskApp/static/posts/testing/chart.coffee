data_mychart = [ {
  'color': 'green'
  'values': [
    {
      'y': 0.6679304109346873
      'x': 0.069950279789620984
    }
    {
      'y': 0.26920413951355426
      'x': 0.24473290609458942
    }
    {
      'y': 0.78668609268167644
      'x': 0.90987461534918523
    }
    {
      'y': 0.69899354208211295
      'x': 0.90114537230164304
    }
    {
      'y': 0.53750672045237435
      'x': 0.94234021827180769
    }
    {
      'y': 0.98221652450673769
      'x': 0.46836204208085808
    }
    {
      'y': 0.083888722679611449
      'x': 0.72494019054133751
    }
    {
      'y': 0.22611438130812545
      'x': 0.84818152903060806
    }
    {
      'y': 0.84095290368800768
      'x': 0.48088797480204715
    }
    {
      'y': 0.57466722364714906
      'x': 0.69186454547450171
    }
  ]
  'key': 'Positive'
  'yAxis': '1'
} ]
nv.addGraph ->
  chart = nv.models.lineChart()
  chart.margin
    top: 30
    right: 60
    bottom: 20
    left: 60
  datum = data_mychart
  chart.xAxis.tickFormat (d) ->
    d3.time.format('%H:%M') new Date(parseInt(d))
  chart.yAxis.tickFormat d3.format(',.02f')
  chart.tooltipContent (key, y, e, graph) ->
    `var y`
    `var y`
    x = d3.time.format('%d %b %Y')(new Date(parseInt(graph.point.x)))
    y = String(graph.point.y)
    y = String(graph.point.y)
    tooltip_str = '<center><b>' + key + '</b></center>' + y + ' on ' + x
    tooltip_str
  chart.showLegend true
  d3.select('#mychart svg').datum(datum).transition().duration(500).attr('width', 800).attr('height', 450).call chart
  return
