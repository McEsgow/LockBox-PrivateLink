function handleDrop(event) {
  event.preventDefault();
  // Handle file drop logic
  // Implement as needed
}

function handleDragOver(event) {
  event.preventDefault();
}

function encryptFile() {
  var encryptionKey = document.getElementById('encryptionKeyInput').value;
  // AJAX call to Python backend for file encryption
  $.ajax({
      type: 'POST',
      url: '/encrypt',
      data: { key: encryptionKey },
      success: function(response) {
          // Handle success
          console.log(response);
      },
      error: function(error) {
          // Handle error
          console.error(error);
      }
  });
}

function decryptFile() {
  var encryptionKey = document.getElementById('encryptionKeyInput').value;
  // AJAX call to Python backend for file decryption
  $.ajax({
      type: 'POST',
      url: '/decrypt',
      data: { key: encryptionKey },
      success: function(response) {
          // Handle success
          console.log(response);
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

// EVENTLISTENERS
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('privateKeyInput').addEventListener('input', function() {
    var privateKey = document.getElementById('privateKeyInput').value
    var outputID = 'publicKeyOutput'
    extractPublicKey(outputID, privateKey)
  })
});