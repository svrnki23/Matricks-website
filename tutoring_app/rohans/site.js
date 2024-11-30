/* Set the width of the side navigation to 250px and the left margin of the page content to 250px 
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
  }
  
   Set the width of the side navigation to 0 and the left margin of the page content to 0 
  function closeNav() {
    document.getElementById("mySidenav").style.width = "7px";
    document.getElementById("main").style.marginLeft = "7px";
  }
*/

document.addEventListener("DOMContentLoaded", function () {
  // Load Navbar
  fetch("base.html")
      .then(response => response.text())
      .then(html => {
          document.body.insertAdjacentHTML("afterbegin", html);
      });
});