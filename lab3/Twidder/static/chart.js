/**
 * Created by linwe991 on 01/03/17.
 */

showChart = function() {
    var data = [4, 8, 15, 16, 23, 42];
    console.log("showChart");
    d3.select(".chart").selectAll("div").data(data).enter().append("div").style("width", function(d) { return d * 10 + "px"; }).text(function(d) { return d; });
;
};
