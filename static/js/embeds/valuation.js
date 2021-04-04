
self.addEventListener('load', async e =>  {
    let msToDate = (milliseconds) =>' ' + (new Date(milliseconds)) + ' ';
    let disp_date = dtime =>msToDate(dtime).split("GMT")[0];
    let disp_num = number =>String(number).replace(/\B(?=(\d{3})+(?!\d))/g, ",");

    let show_data = async function(title_number,json_data) {
        document.getElementById('title_num').innerHTML =`
             <span class="text text-dark">Title Number:  <em class="text-info">${title_number}</em></span>
        `
        document.getElementById('address').innerHTML = `
            <span class="text text-dark">Address:<em class="text-info"> ${json_data['address']}</em> </span>
        `
        document.getElementById('location').innerHTML = `
            <span class="text text-dark">Location :
            <ul>
                <li>lat: ${json_data['approx_centre']['lat']}</li>
                <li>lng: ${json_data['approx_centre']['lng']}</li>
            </ul></span>        
        `
        document.getElementById('class').innerHTML = `
            <span class="text text-dark">Class:<em class="text-info"> ${json_data['class']}</em> </span>
        `
        document.getElementById('covenants').innerHTML  = `
            <span class="text text-dark">Covenants: <em class="text-info">${json_data['covenants']}</em> </span>        
        `
        document.getElementById('easements').innerHTML  = `
            <span class="text text-dark">Easements: <em class="text-info">${json_data['easements']}</em> </span>        
        `
        document.getElementById('energy_score').innerHTML  = `
            <span class="text text-dark">Energy Score: <em class="text-info">${json_data['energy_score']}</em> </span>        
        `
        document.getElementById('estate_interest').innerHTML  = `
            <span class="text text-dark">Estate Interest: <em class="text-info">${json_data['estate_interest']}</em> </span>        
        `
        document.getElementById('internal_area').innerHTML  = `
            <span class="text text-dark">Internal Area: <em class="text-info">${json_data['internal_area']}</em> </span>        
        `
        document.getElementById('last_sold').innerHTML = `
            <span class="text text-dark">Last Sold :
                <ol>  
                    <li>Amount : <em class="text-info">${disp_num(json_data['last_sold']['amount'])}</em></li>
                    <li>Date: <em class="text-info">${json_data['last_sold']['date']}</em></li>
                </ol>                 
            </span>
        `
        document.getElementById('ownership').innerHTML = `
            <span class="text text-dark">Ownership : <em class="text-info">${json_data['ownership']['type']}</em> </span>
        `
        document.getElementById('plot_size').innerHTML = `
            <span class="text text-dark">Plot Size : <em class="text-info">${json_data['plot_size']}</em> </span>
        `

    }
    document.getElementById('search').addEventListener('click', async  e => {
        e.preventDefault();
        let title_number = document.getElementById('title_number').value;
        if(title_number === ""){alert('Please enter valid title Number'); return false}

        let init_post = {
            'method': 'POST',
            'mode': 'cors',
            'body': JSON.stringify({'title': title_number}),
            'headers': new Headers({'content-type': 'application/json'})
        }

        let request = new Request('/api/v1/title-info', init_post);
        let response = await fetch(request);
        console.log('response: ', response);
        let json_data = await response.json();
        console.log('json_data: ', json_data);
        if (response.ok === true){
            let response = await show_data(title_number,json_data['data'])
        }

    })
})