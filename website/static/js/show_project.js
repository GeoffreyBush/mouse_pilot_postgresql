console.log("show_project.js loaded")

// When checkbox is clicked, highlight the table row for that mouse
function highlightMouse(rowID) {
    row = document.getElementById(rowID);
    row.classList.toggle("highlighted-row")
}