function PreviewImage() {
        var oFReader = new FileReader();
        oFReader.readAsDataURL(document.getElementById("uploadImage").files[0]);

        oFReader.onload = function (oFREvent) {
            document.getElementById("uploadPreview").src = oFREvent.target.result;
        };
    };


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

var c1 = document.querySelectorAll(".cards_1 .card");
var c2 = document.querySelectorAll(".cards_2 .card");
var c3 = document.querySelectorAll(".cards_3 .card");
var c4 = document.querySelectorAll(".cards_4 .card");

for(var i = 0; i < c1.length ; i++){
    if( i > 2){
        c1[i].style.display = "none";
    }
}

for(var i = 0; i < c2.length ; i++){
    if( i > 2){
        c2[i].style.display = "none";
    }
}

for(var i = 0; i < c3.length ; i++){
    if( i > 2){
        c3[i].style.display = "none";
    }
}

for(var i = 0; i < c4.length ; i++){
    if( i > 2){
        c4[i].style.display = "none";
    }
}

var btn_back_4 = document.getElementById("btn_card_back_4");
var btn_next_4 = document.getElementById("btn_card_next_4");
var btn_back_3 = document.getElementById("btn_card_back_3");
var btn_next_3 = document.getElementById("btn_card_next_3");
var btn_back_2 = document.getElementById("btn_card_back_2");
var btn_next_2 = document.getElementById("btn_card_next_2");
var btn_back_1 = document.getElementById("btn_card_back_1");
var btn_next_1 = document.getElementById("btn_card_next_1");

btn_back_4.addEventListener('click', (event) => {
    for(var i = c4.length -1 ; i >= 0 ; i--){
        if (c4[i].style.display === "" || c4[i].style.display === "flex"){
            var temp = i - 3
            if ( temp >= 0){
                c4[i].style.display = "none";
                c4[temp].style.display = "flex";
            }
            break
        }
    }
});

btn_next_4.addEventListener('click', (event) => {
    for(var i = 0; i < c4.length ; i++){
        if (c4[i].style.display === "" || c4[i].style.display === "flex"){
            var temp = i + 3
            if (c4.length > temp){
                c4[i].style.display = "none";
                c4[temp].style.display = "flex";
            }
            break
        }
    }
});

btn_back_3.addEventListener('click', (event) => {
    for(var i = c3.length -1 ; i >= 0 ; i--){
        if (c3[i].style.display === "" || c3[i].style.display === "flex"){
            var temp = i - 3
            if ( temp >= 0){
                c3[i].style.display = "none";
                c3[temp].style.display = "flex";
            }
            break
        }
    }
});

btn_next_3.addEventListener('click', (event) => {
    for(var i = 0; i < c3.length ; i++){
        if (c3[i].style.display === "" || c3[i].style.display === "flex"){
            var temp = i + 3
            if (c3.length > temp){
                c3[i].style.display = "none";
                c3[temp].style.display = "flex";
            }
            break
        }
    }
});

btn_back_2.addEventListener('click', (event) => {
    for(var i = c2.length -1 ; i >= 0 ; i--){
        if (c2[i].style.display === "" || c2[i].style.display === "flex"){
            var temp = i - 3
            if ( temp >= 0){
                c2[i].style.display = "none";
                c2[temp].style.display = "flex";
            }
            break
        }
    }
});

btn_next_2.addEventListener('click', (event) => {
    for(var i = 0; i < c2.length ; i++){
        if (c2[i].style.display === "" || c2[i].style.display === "flex"){
            var temp = i + 3
            if (c2.length > temp){
                c2[i].style.display = "none";
                c2[temp].style.display = "flex";
            }
            break
        }
    }
});

btn_back_1.addEventListener('click', (event) => {
    for(var i = c1.length -1 ; i >= 0 ; i--){
        if (c1[i].style.display === "" || c1[i].style.display === "flex"){
            var temp = i - 3
            if ( temp >= 0){
                c1[i].style.display = "none";
                c1[temp].style.display = "flex";
            }
            break
        }
    }
});

btn_next_1.addEventListener('click', (event) => {
    for(var i = 0; i < c4.length ; i++){
        if (c1[i].style.display === "" || c1[i].style.display === "flex"){
            var temp = i + 3
            if (c1.length > temp){
                c1[i].style.display = "none";
                c1[temp].style.display = "flex";
            }
            break
        }
    }
});

function onClickCard(id){
    let user_id = window.location.pathname.split("/");
    window.location.replace('/api/v1/users/'+user_id[4]+'/project-finish/'+id);
}

function onClickCardDownload(id){
    let user_id = window.location.pathname.split("/");
    window.location.replace('/api/v1/users/'+user_id[4]+'/project-upload/'+id);
}