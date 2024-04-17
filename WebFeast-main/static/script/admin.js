function addsales() {
    var formdata = new FormData(document.getElementById("add-form"));
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/addsales');
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log(xhr.responseText);
        } else {
            console.log('Request failed.  Returned status of ' + xhr.status);
        }
    };
    xhr.send(formdata);
}
