// .jsw files enable you to write functions that run on the server side

// Test any backend function by clicking the "Play" button on the left side of the code panel

// About testing backend functions: https://support.wix.com/en/article/velo-testing-your-backend-functions

// Sample function



import {fetch} from 'wix-fetch';

export async function  fetch_sales_api(postalcode, backend_api) {
	let data = JSON.stringify({postcode:postalcode})
    console.log('json stringy values', data)
    let init_post = {
        method: 'POST',
        headers: { 'Content-type': 'application/json'},
		body:data
    }
	if (backend_api !== ""){
		console.log('sales api has been called')
		let url = 'https://propertydevelopment.worktravel.agency/api/v1/' + backend_api.replace("_","-")
		console.log('url has been created', url)
		let response = await fetch(url, init_post)
		console.log("Response :",response)
		return await response.json()
	}else{
		return JSON.stringify({"status": "failure", "message": "url not submitted"})
	}
}

// Execute the sample function above by copying the following into your page code

/*
import {multiply} from 'backend/aModule';

$w.onReady(function () {

	multiply(4,5).then(product => {
	    console.log(product);
	      // Logs: 20
	})
	.catch(error => {
		console.log(error);
	});
});
*/