

function uploadPhoto() {
    photo = document.getElementById("photo").files[0]
    console.log(photo)
    labels = document.getElementById("labels")
    params = {
        'Accept': 'image/jpeg',
        'Content-Type': 'image/jpeg',
        'folder': 'amz-a2-b2/' + photo.name,
        'X-Amz-Meta-CustomLabels': labels,
        'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    }
    console.log(params)
    
    body = {
        photo
    }
    sdk.uploadFolderPut(params, body, {})
        .then(function(resp) {
            console.log(resp)
            document.getElementById("photo").value = null
            document.getElementById("labels").value = ""
        }).catch(function(err) {
            console.log(err)
        })

}