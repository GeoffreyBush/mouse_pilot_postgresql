console.log("request_popup.js loaded")

// Adapted from https://www.w3schools.com/howto/howto_css_modals.asp

// Remove all mouse information from modal
function wipeModal(parent) {
    let children = parent.children
    for (i = 0; i < children.length; i++) {
        if (children[i].id !== "modal-span") {
            parent.removeChild(children[i]);
        }
    }
}

// Create popup of additional request information
function showMessagesForRequest(tdElement) {
  const requestId = tdElement.getAttribute('data-request-id');
  fetch(`website/show_message/${requestId}/`) 
    .then(response => {
      console.log(response)
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.text();
    })
    .then(html => {
      document.querySelector('#request-messaging-pop-up').innerHTML = html;
      document.getElementById('myModal').style.display = 'block';
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

// Close the modal when anywhere outside of the modal content is clicked
window.onclick = function(event) {
    let modal = document.getElementById('myModal');
    if (event.target == modal) {
        modal.style.display = 'none';
        wipeModal(document.getElementById('request-messaging-pop-up'));
    }
};

document.addEventListener("DOMContentLoaded", function() {
  // Attach the close functionality to the span
  document.getElementById('modal-span').addEventListener('click', function() {
    document.getElementById('myModal').style.display = 'none';
  });
});