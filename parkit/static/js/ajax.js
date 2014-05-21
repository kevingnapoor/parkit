// Make an AJAX request.
function fetch(url, callback) {
    // not even going to try to support IE
    httpRequest = new XMLHttpRequest();

    function callWhenReady() {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status === 200) {
                callback(httpRequest.responseText);
            } else {
                alert('Oh no something went wrong :(');
            }
        }
    }

    httpRequest.onreadystatechange = callWhenReady;
    httpRequest.open('GET', url);
    httpRequest.send();
}
