function dropHandler(ev) {
    console.log('File(s) dropped');
  
    // Prevent default behavior (Prevent file from being opened)
    ev.preventDefault();
  
    if (ev.dataTransfer.items) {
      // Use DataTransferItemList interface to access the file(s)
      for (var i = 0; i < ev.dataTransfer.items.length; i++) {
        // If dropped items aren't files, reject them
        if (ev.dataTransfer.items[i].kind === 'file') {
          var file = ev.dataTransfer.items[i].getAsFile();
          console.log('... file[' + i + '].name = ' + file.name);
        }
      }
    } else {
      // Use DataTransfer interface to access the file(s)
      for (var i = 0; i < ev.dataTransfer.files.length; i++) {
        console.log('... file[' + i + '].name = ' + ev.dataTransfer.files[i].name);
      }
    }
}


// From online-->
function saveTextAsFile(){
    var textToSave = document.getElementById("inputTextToSave").value;
    var textToSaveAsBlob = new Blob([textToSave], {type:".pdf"});
    var textToSaveAsURL = window.URL.createObjectURL(textToSaveAsBlob);
    var fileNameToSaveAs = document.getElementById("inputFileNameToSaveAs").value;
 
    var downloadLink = document.createElement("a");
    downloadLink.download = fileNameToSaveAs;
    downloadLink.innerHTML = "Download File";
    downloadLink.href = textToSaveAsURL;
    downloadLink.onclick = destroyClickedElement;
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
 
    downloadLink.click();
}
 
function destroyClickedElement(event){
    document.body.removeChild(event.target);
}


// From online-->

// Because we want to access DOM nodes,
// we initialize our script at page load.
window.addEventListener('load', function() {

    // These variables are used to store the form data
    const file = {
        dom: document.getElementById("input_pdf"),
        binary: null
    };
  
    // Use the FileReader API to access file content
    const reader = new FileReader();
  
    // Because FileReader is asynchronous, store its
    // result when it finishes to read the file
    reader.addEventListener("load", function() {
        file.binary = reader.result;
    });
  
    // At page load, if a file is already selected, read it.
    if(file.dom.files[0]) {
        reader.readAsBinaryString(file.dom.files[0]);
    }
  
    // If not, read the file once the user selects it.
    file.dom.addEventListener("change", function() {
        if(reader.readyState === FileReader.LOADING) {
            reader.abort();
        }
    
        reader.readAsBinaryString(file.dom.files[0]);
    });
  
    // sendData is our main function
    function sendData() {
        // If there is a selected file, wait it is read
        // If there is not, delay the execution of the function
        if(!file.binary && file.dom.files.length > 0) {
            setTimeout(sendData, 10);
            return;
        }
    
        // To construct our multipart form data request,
        // We need an XMLHttpRequest instance
        const XHR = new XMLHttpRequest();
    
        // We need a separator to define each part of the request
        const boundary = "blob";
    
        // Store our body request in a string.
        let data = "";
  
        // So, if the user has selected a file
        if(file.dom.files[0]) {
            // Start a new part in our body's request
            data += "--" + boundary + "\r\n";
    
            // Describe it as form data
            data += 'content-disposition: form-data; '
            // Define the name of the form data
                + 'name="' + file.dom.name + '"; '
            // Provide the real name of the file
                + 'filename="' + file.dom.files[0].name + '"\r\n';
            // And the MIME type of the file
            data += 'Content-Type: ' + file.dom.files[0].type + '\r\n';
    
            // There's a blank line between the metadata and the data
            data += '\r\n';
    
            // Append the binary data to our body's request
            data += file.binary + '\r\n';
        }
    
        // Define what happens on successful data submission
        XHR.addEventListener('load', function(event) {
            alert('Yeah! Data sent and response loaded.');
        });
    
        // Define what happens in case of error
        XHR.addEventListener('error', function(event) {
            alert('Oops! Something went wrong.');
        });
    
        // Set up our request
        XHR.open('POST', 'https://example.com/cors.php');
    
        // Add the required HTTP header to handle a multipart form data POST request
        XHR.setRequestHeader('Content-Type', 'multipart/form-data; boundary=' + boundary);
    
        // And finally, send our data.
        XHR.send(data);
    }
  
    // Access our form...
    const form = document.getElementById("theForm");
  
    // ...to take over the submit event
    form.addEventListener('submit', function(event) {
      event.preventDefault();
      sendData();
    });
});