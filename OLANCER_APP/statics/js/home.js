var slideIndex = 2;

showDivs(slideIndex);

function plusDivs(n) {
  showDivs(slideIndex += n);
}

function showDivs(n) {
  var i;
  var x = document.getElementsByClassName("card_comment");
  var y = document.getElementsByClassName("img_card_comment");
  if (n > x.length) {slideIndex = 1}
  if (n < 1) {slideIndex = x.length} ;
  for (i = 0; i < x.length; i++) {
    x[i].classList.remove("card_selected");
    y[i].classList.remove("img_selected");
  }
  x[slideIndex-1].classList.add("card_selected");
  y[slideIndex-1].classList.add("img_selected");
}