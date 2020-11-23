function getValue (slider, id) {
  var span = document.getElementById(id);
  span.innerText = slider.value;

}


function changeInnerText(btnGray) {
  if (btnGray.innerText != "GrayScale"){
    btnGray.innerText = "GrayScale";
  }
  else {
    btnGray.innerText = "RGB";
  }
}  


function changeLabel(checkbox){
  var label = document.getElementById("switch_label")
  var sliders = document.getElementsByClassName("slider")
  var bg;
  if (checkbox.checked){
    label.innerText = "Brightness";
    bg = [
      "linear-gradient(90deg, black 0%, rgba(255,0,0,1) 50%, white 100%)",
      "linear-gradient(90deg, black 0%, rgba(0,255,0,1) 50%, white 100%)",
      "linear-gradient(90deg, black 0%, rgba(0,0,255,1) 50%, white 100%)"
    ]
  }
  else{
    label.innerText = "Saturation";
    bg = [
      "linear-gradient(90deg, rgb(150, 150, 150) 0%, rgb(150, 75, 75) 50%,  rgb(150, 0, 0) 100%)",
      "linear-gradient(90deg, rgb(150, 150, 150) 0%, rgb(75, 150, 75) 50%,  rgb(0, 150, 0) 100%)",
      "linear-gradient(90deg, rgb(150, 150, 150) 0%, rgb(75, 75, 150) 50%,  rgb(0, 0, 150) 100%)"
    ]
  }

  for(i = 0; i < sliders.length; i++){
    sliders[i].style.background = bg[i];
  }
}