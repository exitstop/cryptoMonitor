#!/usr/bin/env python3

print("Content-type: text/html")
print()
print("<h1>Hello world!</h1>")



print ("""
	<html>
	  <head>
	    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
	    <script type="text/javascript">
	      google.charts.load('current', {'packages':['corechart']});
	      google.charts.setOnLoadCallback(drawChart);

	  function drawChart() {
	    var data = google.visualization.arrayToDataTable([
	      ['Mon', 10, 28, 38, 45],
	      ['Tue', 31, 38, 55, 66],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Wed', 50, 55, 77, 80],
	      ['Thu', 77, 77, 66, 50],
	      ['Fri', 68, 66, 22, 15]
	      // Treat first row as data as well.
	    ], true);

	    var options = {
	      legend:'none',
	      candlestick: {
            fallingColor: { strokeWidth: 1, stroke: '#a52714' }, // red
            risingColor: { strokeWidth: 1, fill: '#ffffff', stroke: '#0f9d58' }   // green
          }
	    };

	    var chart = new google.visualization.CandlestickChart(document.getElementById('chart_div'));

	    chart.draw(data, options);
	  }
	    </script>
	  </head>
	  <body>
	    <div id="chart_div" style="width: 900px; height: 500px;"></div>
	  </body>
	</html>
	""")