function fun() {


        const params = {
            'user_id': (document.getElementById('input_1').value)
        }

        const http = new XMLHttpRequest()
        http.open('POST', 'http://localhost:5000/get_rec')
        http.setRequestHeader('Content-type', 'application/json')
        http.send(JSON.stringify(params)) // Make sure to stringify
        http.onload = function() {
                console.log(this.responseText);
            alert(http.responseText)
        }


}

