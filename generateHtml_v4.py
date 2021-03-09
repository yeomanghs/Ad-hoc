
def generateHtml(jsonStructure, htmlName):
    wrapper = """<meta charset="utf-8">
    <script src="https://d3js.org/d3.v4.min.js" type="text/javascript"></script>
    <script src="https://d3js.org/d3-selection-multi.v1.js"></script>
        <style type="text/css">
            .node:checked~svg cirle{fill: green}              
            .link { stroke: #999; stroke-opacity: .6; stroke-width: 1px; }
            .link:hover{stroke: #800;; stroke-width:2px;}
        </style>
    <body>
        <div>
            <h2 style="padding-left:16px;font-size:20px" id = "content">Node Info</h2>
            <h2 style="padding-right:16px;font-size:20px" id = "content2">Relationship Type</h2>            
        </div>
        <svg width="2000" height="1500"></svg>
    <script>

    var colors = d3.scaleOrdinal(d3.schemeCategory10);
    
    var svg = d3.select("svg"),
        width = +svg.attr("width"),
        height = +svg.attr("height"),
        node,
        link;
        
    var svg2 = d3.select("svg");
    
    var categories = ["Target", "Entity", "Contact", "Account", "STR", "Address"]
    
    svg2.selectAll("mydots")
      .data(categories)
      .enter()
      .append("circle")
        .attr("cx", 100)
        .attr("cy", function(d,i){ return 100 + i*25}) // 100 is where the first dot appears. 25 is the distance between dots
        .attr("r", 7)
        .style("fill", function(d){ return colors(d)})

    svg2.selectAll("mylabels")
      .data(categories)
      .enter()
      .append("text")
        .attr("x", 120)
        .attr("y", function(d,i){ return 100 + i*25}) // 100 is where the first dot appears. 25 is the distance between dots
        .style("fill", function(d){ return colors(d)})
        .text(function(d){ return d})
        .attr("text-anchor", "left")
        .style("alignment-baseline", "middle")

    svg.append('defs').append('marker')
        .attrs({'id':'arrowhead',
            'viewBox':'-0 -5 10 10',
            'refX':13,
            'refY':0,
            'orient':'auto',
            'markerWidth':13,
            'markerHeight':13,
            'xoverflow':'visible'})
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', '#999')
        .style('stroke','none');

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {return d.NeoId;}).distance(100).strength(1))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    var rawData = %s;

        update(rawData.links, rawData.nodes);

        function update(links, nodes) {
            link = svg.selectAll(".link")
                .data(links)
                .enter()
                .append("line")
                .attr("class", "link")
                .attr('marker-end','url(#arrowhead)')
                .on("mouseenter", showRelInfo)

            link.append("title")
                .text(function (d) {return d.type;})

            edgepaths = svg.selectAll(".edgepath")
                .data(links)
                .enter()
                .append('path')
                .attrs({
                    'class': 'edgepath',
                    'fill-opacity': 0,
                    'stroke-opacity': 0,
                    'id': function (d, i) {return 'edgepath' + i}
                })
                .style("pointer-events", "none");

            edgelabels = svg.selectAll(".edgelabel")
                .data(links)
                .enter()
                .append('text')
                .style("pointer-events", "none")
                .attrs({
                    'class': 'edgelabel',
                    'id': function (d, i) {return 'edgelabel' + i},
                    'font-size': 15,
                    'fill': '#aaa'
                });

            edgelabels.append('textPath')
                .attr('xlink:href', function (d, i) {return '#edgepath' + i})
                .style("text-anchor", "middle")
                .style("pointer-events", "none")
                .attr("startOffset", 50)
                .attr("font-size", 13)
                .text(function (d) {return ""})

            node = svg.selectAll(".node")
                .data(nodes)
                .enter()
                .append("g")
                .attr("class", "node")
                .call(d3.drag()
                        .on("start", dragstarted)
                        .on("drag", dragged)
                )
                .on("click", showInfo)

            node.append("circle")
                .attr("r", 8)
                .style("fill", function (d) {return colors(d.label);})

            node.append("title")
                .text(function(d) {return "";});

            node.append("text")
                .attr("dy", -3)
                .text(function (d) {
                if (d.label == "Entity"){
                return ''}
                else if (d.label == "Target"){
                return d.label + ":" + d.pName;}
                else if (d.label == "Account"){
                return ''}
                else if (d.label == "STR"){
                return ''}
                else if (d.label == "Contact"){
                return ''}
                });

            simulation
                .nodes(nodes)
                .on("tick", ticked);

            simulation.force("link")
                .links(links);
        }
        
        function showRelInfo(d){
        var includedList = ['type']
        var filterDict = Object.keys(d).reduce(function (filtered, key) {
                if (includedList.includes(key)) filtered[key] = d[key];
                return filtered;
            }, {});
        var enterRelText = d3.select('#content2')
                             .selectAll('div')
                             .data(d3.entries(filterDict))
                             
            enterRelText.enter()
                    .append('div')
            
            enterRelText.text(d => d.value)

            enterRelText.exit().remove()
        }
        
        function showInfo(d){
        var includedList = ['pName', 'pOffence','pRecordID','pOccupation', 'pCountry', 'pIdList',
                            'pAccountNo', 'p2006', 'p2007', 'p2008', 'p2009', 'p2010', 'p2011', 'p2012',
                            'p2013', 'p2014', 'p2015', 'p2016', 'p2017', 'p2018', 
                            'p2019', 'p2020', 'pTotalAmount','pReportingIns', 'pContactInfo']
        var filterDict = Object.keys(d).reduce(function (filtered, key) {
                if (includedList.includes(key)) filtered[key] = d[key];
                return filtered;
            }, {});
        var enterText = d3.select('#content')
                .selectAll('div')
                .data(d3.entries(filterDict))

            enterText.enter()
                    .append('div')
            
            enterText.text(d => d.key.slice(1) + " : " + d.value)

            enterText.exit().remove()
        }
        
        
        function ticked() {
            link
                .attr("x1", function (d) {return d.source.x;})
                .attr("y1", function (d) {return d.source.y;})
                .attr("x2", function (d) {return d.target.x;})
                .attr("y2", function (d) {return d.target.y;});

            node
                .attr("transform", function (d) {return "translate(" + d.x + ", " + d.y + ")";});

            edgepaths.attr('d', function (d) {
                return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
            });

            edgelabels.attr('transform', function (d) {
                if (d.target.x < d.source.x) {
                    var bbox = this.getBBox();

                    rx = bbox.x + bbox.width / 2;
                    ry = bbox.y + bbox.height / 2;
                    return 'rotate(180 ' + rx + ' ' + ry + ')';
                }
                else {
                    return 'rotate(0)';
                }
            });
        }

        function dragstarted(d) {
            if (!d3.event.active) simulation.alphaTarget(0.3).restart()
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(d) {
            d.fx = d3.event.x;
            d.fy = d3.event.y;
        }

    </script>"""
    final = wrapper %(jsonStructure)

    with open(htmlName, 'w') as f:
        f.write(final)
    print('%s is saved' %htmlName)
