function searchPhotos() {
    query = document.getElementById('search').value
    console.log(query)
    params = {'q': query}
    sdk.searchGet(params, {}, {})
        .then(function(resp){
            console.log(resp)
            urls = resp.data
            console.log(urls)
            for (var i = 0; i < urls.length; i+=1) {
                url = urls[i]
                img = document.createElement("img")
                img.src = url
                console.log(img)
                document.body.appendChild(img)
            }
        }).catch(function(err) {
            console.log(err)
        })
}

function startRecord() {
    
    recognition.start();
    console.log("recognition started")

}

function stopRecord() {
    recognition.stop()
    console.log("recognition stopped")
}
