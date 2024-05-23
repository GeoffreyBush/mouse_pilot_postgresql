function fetchFamilyTree(mouseId) {
  var container = document.getElementById("family-tree-container");
  container.style.display = "block"; // Make sure the container is visible
  container.classList.remove("hidden");
  container.classList.add("visible");


  // Fetch the family tree data
  fetch("/website/family_tree/" + mouseId + "/")
    .then((response) => response.json())
    .then((data) => {
      console.log("Fetched data:", data); // Log the fetched data

      // Create the D3 tree layout
      var treeLayout = d3.tree().size([400, 200]); // adjust size as needed

      // Convert the data to a D3 hierarchy
      var rootNode = d3.hierarchy(data);

      // Compute the tree layout
      treeLayout(rootNode);

      // Select the SVG element
      var svg = d3.select("#family-tree");

      // Clear the SVG for new tree
      svg.selectAll("*").remove();

      // Append a group element and translate it to the center
      var g = svg.append("g").attr("transform", "translate(0, 300)"); // adjust translation as needed

      // Create a zoom behavior
      var zoom = d3
        .zoom()
        .scaleExtent([0.1, 2]) // limit the zoom scale between 0.1x and 10x
        .on("zoom", function () {
          g.attr("transform", d3.event.transform); // apply the zoom transform to the group element
        });

      // Apply the zoom behavior to the SVG
      svg.call(zoom);

      // Create the nodes
      var circles = g
        .selectAll("circle")
        .data(rootNode.descendants())
        .enter()
        .append("circle")
        .attr("cx", function (d) {
          return d.x;
        })
        .attr("cy", function (d) {
          return -d.y;
        }) // flip the tree
        .attr("r", 10); // increase the node size

      // Create the links
      var lines = g
        .selectAll("line")
        .data(rootNode.links())
        .enter()
        .append("line")
        .attr("x1", function (d) {
          return d.source.x;
        })
        .attr("y1", function (d) {
          return -d.source.y;
        }) // flip the tree
        .attr("x2", function (d) {
          return d.target.x;
        })
        .attr("y2", function (d) {
          return -d.target.y;
        }) // flip the tree
        .style("stroke", "black");

      // Add labels
      g.selectAll("text")
        .data(rootNode.descendants())
        .enter()
        .append("text")
        .attr("x", function (d) {
          return d.x;
        })
        .attr("y", function (d) {
          return -d.y;
        }) // flip the tree
        .attr("dy", ".35em") // vertically center text
        .attr("text-anchor", "middle") // center text horizontally
        .attr("fill", "white") // make the text white
        .text(function (d) {
          // display the mouse ID and role
          return d.data.name + (d.data.role ? " (" + d.data.role + ")" : "");
        });
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      );
    });
}
function closeFamilyTree() {
  var container = document.getElementById('family-tree-container');
  var svg = document.getElementById('family-tree');
  while (svg.firstChild) {
    svg.removeChild(svg.firstChild);
  }
  container.style.display = 'none';
}
