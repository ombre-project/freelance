var key_3 = "id"

function getCookie(cname) {
  let name = cname + "=";
  let ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    console.log(ca[i]);
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}


document.body.addEventListener("submit", async function (event) {
  event.preventDefault();
  console.log(event.target)
  const form = event.target;
  const result = await fetch(form.action, {
    method: form.method,
    body: new URLSearchParams([...(new FormData(form))]),
  });
  let res = await result;
  try {
        id = getCookie(key_3);
        window.location.replace('/api/v1/users/'+id+'/profile');
    }catch(err) {
        console.log("ERROR : "+err);
        alert("Get permission to set our cookie in your browser .");
    }
});