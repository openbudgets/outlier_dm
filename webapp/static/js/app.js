var height = 400*1.5;
var width = 500*1.5;
var margin = 100*2;
var labelX = 'YEAR';
var labelY = 'MONEY';
var svg = d3.select('.chart')
  .append('svg')
  .attr('class', 'chart')
  .attr("width", width + margin + margin)
  .attr("height", height + margin + margin)
  .append("g")
  .attr("transform", "translate(" + margin + "," + margin + ")");

x_data = data.map(function (d) { return d.x; });
years = x_data.filter(function(item, pos) {
    return x_data.indexOf(item) == pos;
}).sort();

range_array = new Array(years.length);
range_array[0] = 0;
for (var i=1; i<range_array.length; i++) {
  range_array[i] = range_array[i-1] + width / (years.length - 1);
}

var x = d3.scale.ordinal()
  .domain(years)
  .range(range_array);

var y = d3.scale.linear()
  .domain([d3.min(data, function (d) { return d.y; }), d3.max(data, function (d) { return d.y; })])
  .range([height, 0]);

var scale = d3.scale.sqrt()
  .domain([d3.min(data, function (d) { return d.size; }), d3.max(data, function (d) { return d.size; })])
  .range([1, 40]);

var opacity = d3.scale.sqrt()
  .domain([d3.min(data, function (d) { return d.size; }), d3.max(data, function (d) { return d.size; })])
  .range([1, .5]);

var color = d3.scale.category10();

var xAxis = d3.svg.axis().scale(x);
var yAxis = d3.svg.axis().scale(y).orient("left");

// Define the div for the tooltip
var div = d3.select("body").append("div")
  .attr("class", "extra")
  .style("opacity", 0);

// y axis and label
svg.append("g")
  .attr("class", "y axis")
  .call(yAxis)
  .append("text")
  .attr("x", 0)
  .attr("y", -margin + 120)
  .attr("dy", ".71em")
  .style("text-anchor", "end")
  .style("font-weight", "bold")
  .text(labelY);

// x axis and label
svg.append("g")
  .attr("class", "x axis")
  .attr("transform", "translate(0," + height + ")")
  .call(xAxis)
  .append("text")
  .attr("x", width + 70)
  .attr("y", margin - 130)
  .attr("dy", ".71em")
  .style("text-anchor", "end")
  .style("font-weight", "bold")
  .text(labelX);

colors = {};
data.forEach(function(d) {
  colors[d.color] = color(d.color);
});

i = 0;
for (var key in colors) {
  if (!colors.hasOwnProperty(key)) continue;
  i++;
  svg.append("text")
    .style("fill", colors[key])
    .style("font-weight", "bold")
    .style("font-size", "20px")
    .attr("x", width + 50)
    .attr("y", -50 + 20*i)
    .text(key);
}

svg.selectAll("circle")
  .data(data)
  .enter()
  .insert("circle")
  .attr("cx", width / 2)
  .attr("cy", height / 2)
  .attr("opacity", function (d) { return opacity(d.size); })
  .attr("r", function (d) { return scale(d.size); })
  .style("fill", function (d) { return color(d.color); })
  .on("click", function(d, i) {
    div.transition()
      .duration(200)
      .style("opacity", .9);
    div.html("<b><p>Year: " + d.x + "</p><p>Money: " + d.y + "</p><p>Budget Phase: " + d.color + "</p><p>Outlier Score: " + d.size + "</b>")
      .style("left", (d3.event.pageX) + "px")
      .style("top", (d3.event.pageY - 28) + "px");
  })
  .on('mouseover', function (d, i) {
    fade(d.color, .1);
  })
  .on('mouseout', function (d, i) {
    fadeOut();
  })
  .transition()
  .attr("cx", function (d) { return x(d.x); })
  .attr("cy", function (d) { return y(d.y); });

function fade(color, opacity) {
  svg.selectAll("circle")
    .filter(function (d) {
      return d.color != color;
    })
    .transition()
    .style("opacity", opacity);
}

function fadeOut() {
  svg.selectAll("circle")
    .transition()
    .style("opacity", function (d) { opacity(d.size); });
}