function login() {
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function () {
    document.querySelector(".homepage").innerHTML = this.responseText;
  };
  xhttp.open("GET", "ajax_info.txt", true);
  xhttp.send();
}
