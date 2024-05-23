// Adapted from https: //www.geeksforgeeks.org/how-to-create-responsive-admin-dashboard-using-html-css-javascript/
console.log("base.js loaded");

let menuicn = document.querySelector(".menuicn");
let nav = document.querySelector(".navcontainer");

menuicn.addEventListener("click", () => {
    nav.classList.toggle("navclose");
})