function openPage(pageName) {
  var i;
  var x = document.getElementsByClassName("view-page");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  console.log(pageName);
  document.getElementById(pageName).style.display = "block";
  console.log(document.getElementById(pageName).style.display);
}


