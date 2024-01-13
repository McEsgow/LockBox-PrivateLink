var b64DroppedFile = ''
var droppedFileName = ''
function handleDrop(event) {
  event.preventDefault();

  // Access the dropped files
  const files = event.dataTransfer.files;

  // Check if any file is dropped
  if (files.length > 0) {
    const file = files[0];
    const reader = new FileReader();

    // Read the file as data URL, which will be base64 encoded
    reader.readAsDataURL(file);

    // Define a callback function to handle the result
    reader.onload = function () {
      // The result contains the base64 encoded file data
      b64DroppedFile = reader.result.split(',')[1];
      droppedFileName = file.name;
      updateFileInfo(file.name, file.size);
    };

    // Handle potential errors during file reading
    reader.onerror = function (error) {
      console.error('Error reading the file:', error);
    };
  }
}

function encryptFileButton() {
  encryptFile(b64DroppedFile, droppedFileName);
}

function decryptFileButton() {
  decryptFile(b64DroppedFile, droppedFileName);
}

function updateFileInfo(filename, filesize) {
  const fileInfoDiv = document.getElementById('file-info');
  fileInfoDiv.innerHTML = `Filename: ${filename}<br>Size: ${(filesize / 1024 /1024).toFixed(2)} MB`;

  if (filename.endsWith('.lb')) {
    document.getElementById('encryptFileButton').disabled = true
    document.getElementById('decryptFileButton').disabled = false
  }
  else {
    document.getElementById('encryptFileButton').disabled = false
    document.getElementById('decryptFileButton').disabled = true
  }

}

function handleDragOver(event) {
  event.preventDefault();
}

function encryptFile(b64FileData, fileName) {
  var encryptionKey = document.getElementById('lockBoxKeyInput').value;
  // AJAX call to Python backend for file encryption
  $.ajax({
      type: 'POST',
      url: '/encrypt',
      data: { file: b64FileData, filename: fileName, encryptionKey:encryptionKey},
      success: function(response) {
        document.getElementById('file-status').innerHTML = response.status;
        setTimeout(function () {
          document.getElementById('file-status').innerHTML = '';
        }, 5000);
      },
      error: function(error) {
          // Handle error
          console.error(error);
      }
  });
}

function decryptFile(b64FileData, fileName) {
  var encryptionKey = document.getElementById('lockBoxKeyInput').value;
  // AJAX call to Python backend for file encryption
  $.ajax({
      type: 'POST',
      url: '/decrypt',
      data: { file: b64FileData, filename: fileName, encryptionKey:encryptionKey},
      success: function(response) {
        console.log(response);
        document.getElementById('file-status').innerHTML = response.status;
        setTimeout(function () {
          document.getElementById('file-status').innerHTML = '';
        }, 5000);
      },
      error: function(error) {
          // Handle error
          console.error(error);
      }
  });
}

function generateStrongKey(inputId) {
  // AJAX call to Python backend for strong key generation
  $.ajax({
      type: 'GET',
      url: '/generate_key',
      success: function(response) {
          // Update the input field with the generated key
          document.getElementById(inputId).value = response.key;
      },
      error: function(error) {
          // Handle error
          console.error(error);
      }
  });
}

function generatePrivateKey(inputId, outputID) {
  // AJAX call to Python backend for strong key generation
  $.ajax({
      type: 'GET',
      url: '/generate_private_key',
      success: function(response) {
          // Update the input field with the generated key
          document.getElementById(inputId).value = response.key;
          extractPublicKey(outputID, response.key);
      },
      error: function(error) {
          // Handle error
          console.error(error);
      }
  });
}

function extractPublicKey(outputID, privateKey) {
  // AJAX call to Python backend for strong key generation
  $.ajax({
    type: 'POST',
    url: '/extract_public_key',
    data: { key: privateKey },
    success: function(response) {
        // Handle success
        document.getElementById(outputID).value = response.key;
    },
    error: function(error) {
        // Handle error
        console.error(error);
    }
});
}


function copyToClipboard(inputId) {
  // Get the input element by ID
  const inputElement = document.getElementById(inputId);

  // Check if the input element exists
  if (inputElement) {
    // Select the text inside the input element
    inputElement.select();

    try {
      // Attempt to copy the selected text to the clipboard using the Clipboard API
      document.execCommand('copy');
      console.log('Text copied to clipboard');
    } catch (err) {
      console.error('Unable to copy text to clipboard', err);
    }

    // Deselect the text after copying
    window.getSelection().removeAllRanges();
  } else {
    console.error('Input element with ID ' + inputId + ' not found');
  }
}

function decryptSecretKey(inputId, privateKeyID, outputId){
    // AJAX call to Python backend for strong key generation
    $.ajax({
      type: 'POST',
      url: '/decrypt_secret_key',
      data: { encrypted_key: document.getElementById(inputId).value, private_key: document.getElementById(privateKeyID).value },
      success: function(response) {
          // Handle success
          document.getElementById(outputId).value = response.key;
      },
      error: function(error) {
          // Handle error
          console.error(error);
      }
  });
}

function encryptSecretKey(secretKeyInputId, publicKeyInputID, outputId){
  // AJAX call to Python backend for strong key generation
  $.ajax({
    type: 'POST',
    url: '/encrypt_secret_key',
    data: { secret_key: document.getElementById(secretKeyInputId).value, public_key: document.getElementById(publicKeyInputID).value },
    success: function(response) {
        // Handle success
        document.getElementById(outputId).value = response.key;
    },
    error: function(error) {
        // Handle error
        console.error(error);
    }
});
}

function ecryptFile() {
  
}

// EVENTLISTENERS
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('privateKeyInput').addEventListener('input', function() {
    var privateKey = document.getElementById('privateKeyInput').value
    var outputID = 'publicKeyOutput'
    extractPublicKey(outputID, privateKey)
  })
});