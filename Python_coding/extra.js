// Get the container element
var btnContainer = document.getElementById("myDIV");

// Get all buttons with class="btn" inside the container
var btns = btnContainer.getElementsByClassName("btn");

// Loop through the buttons and add the active class to the current/clicked button
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
}


function saveFormDataAsFile() {
  // Get form data
  const formData = new FormData(document.getElementById('myForm'));
  let dataToSave = '';

  for (const [key, value] of formData.entries()) {
    dataToSave += `${key}: ${value}\n`;
  }

  // Create a Blob object from the data
  const blob = new Blob([dataToSave], { type: 'text/plain' });

  // Create a temporary URL for the Blob
  const url = URL.createObjectURL(blob);

  // Create a link element and trigger a download
  const a = document.createElement('a');
  a.href = url;
  a.download = 'formData.txt'; // Name of the downloaded file
  document.body.appendChild(a);
  a.click();

  // Clean up the temporary URL and element
  URL.revokeObjectURL(url);
  document.body.removeChild(a);
}