// API Reference: https://www.wix.com/velo/reference/api-overview/introduction
// “Hello, World!” Example: https://learn-code.wix.com/en/article/1-hello-world
// importing from fetch_sales_api: public:sales.api.js

import {fetch_sales_api} from 'backend/aModule'

$w.onReady(function () {
	// Write your JavaScript here

	// To select an element by ID use: $w("#elementID")

	// Click "Preview" to run your code
	/** disabling the dropdown list until user enters postal code */
 	$w("#selectsearchapi").disable()
});

export async function dropdown1_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	let extra_field = $w("#extraField")
	/** modify the input elements here display the input fields
	 * needed to capture the input needed for each endpoint */
	switch (event.target.value) {
		case "prices":
			/** added variable bedrooms */

			extra_field.placeholder = "Number of Bedrooms"
			extra_field.show()
			break;

		case "sold_prices_per_sqf":
			/** prices per squarefeet */
			extra_field.hide()
			extra_field.disable()
			break;

		case "sold_prices":
			/**  three more fields are required */
			break;

		case "growth":
			/** continue its fine but only change to growth display later on */
			break;

	}


}

export async function postal_code_oninput(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here:
	// enabling endpoint selection
	if ($w("#selectsearchapi").enabled){}else{$w("#selectsearchapi").enable()}

}

export async function submit_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here:
		// Add your code for this event here:
	let postalcode = $w("#postalcode").value
	let content_table = $w("#apicontent")
	let endpoint = $w("#selectsearchapi").value



	let response = await fetch_sales_api(postalcode,endpoint)
	if (response.status === "success"){
		let display_interface = await show_output_interface(endpoint)
		/** at this stage consider that the output contains the elements needed to display each of the endpoints */
		switch(endpoint){
		case "sold_prices":
			break;
		case "sold_prices_per_sqf":
			break;
		case "growth":
			break;

		case "postcode_stats":
			break;
		case "sourced_properties":
			break;

		case "property_info":
			break;
		case "development_gdv":
			break;
		default:
			break;
		}
	}
}

export async function display_api_data(data){
	// TODO - Add data to table
	// enable datatable to display the data to user
}



export async function show_output_interface (choice) {
	/** function used to modify the user interface for several output formats*/
	/** an array containing elements needed to show the output for several endpoints */
	let output_interface = []
	switch(choice){
		case "sold_prices":
			break;
		case "sold_prices_per_sqf":
			break;
		case "growth":
			break;

		case "postcode_stats":
			break;
		case "sourced_properties":
			break;

		case "property_info":
			break;
		case "development_gdv":
			break;
		default:
			break;

	}
	return output_interface
}