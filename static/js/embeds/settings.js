self.addEventListener('load', async e => {
    console.log('document loaded');
    document.getElementById('submit_butt').addEventListener('click', async e => {
        e.preventDefault();
        let search_option = document.getElementById('search_option').value;
        let postcode = document.getElementById('postcode').value;
        let message = document.getElementById('message');
        let email = document.getElementById('email').value;

        let init_post = {
            'method': 'POST',
            'mode': 'cors',
            'body': JSON.stringify({'search':search_option, 'postcode': postcode, 'email': email}),
            'headers': new Headers({'content-type': 'application/json'})
        }
        let request = new Request('/notification-settings', init_post);
        let response = await fetch(request);
        let json_data = await response.json();
        if (response.ok === true){
            message.innerHTML = `<span class="card-text text-info"> ${json_data['message']}</span>`
        }else{
            message.innerHTML = `<span class="card-text text-danger"> ${json_data['message']}</span>`
        }

    })
})