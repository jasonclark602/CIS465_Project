var slider = document.getElementsByClassName("slider");
var output = document.getElementsByClassName("demo");
output.innerHTML = slider.value;

slider.oninput = function() {
  output.innerHTML = this.value;
}