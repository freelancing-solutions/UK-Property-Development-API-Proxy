// API Reference: https://www.wix.com/velo/reference/api-overview/introduction
// “Hello, World!” Example: https://learn-code.wix.com/en/article/1-hello-world
// importing from fetch_sales_api: public:sales.api.js

import {fetch_sales_api} from 'backend/aModule'


$w.onReady(function () {
	// Write your JavaScript here

	// To select an element by ID use: $w("#elementID")

	// Click "Preview" to run your code
	/** disabling the dropdown list until user enters postal code */
 	$w("#selectsearchapi").disable();


});

export async function dropdown1_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	/** modify the input elements here display the input fields
	 * needed to capture the input needed for each endpoint */
	let extra_field  = $w("#extraField");
	let property_types_field = $w("#propertyTypes");
	let property_age_field = $w("#propertyAge");
	let data;
	let postcode = $w("#postalcode");

	switch (event.target.value) {
		case "prices":
			/** added variable bedrooms */

			extra_field.placeholder = "Number of Bedrooms"
			// showing relevant field
			extra_field.show();
			extra_field.enable();
			/** hiding the other fields */
			property_age_field.hide();
			property_age_field.hide();
			property_types_field.hide();
			break;

		case "prices_per_sqf":
			/** prices per squarefeet */
			extra_field.hide();
			property_age_field.hide();
			property_age_field.hide();
			property_types_field.hide();

			break;


		case "sold_prices":
			/**  three more fields are required */
			extra_field.show();
			property_age_field.show();
			property_age_field.show();
			property_types_field.show();

			break;

		case "growth":
			/** continue its fine but only change to growth display later on */

			extra_field.hide();
			property_age_field.hide();
			property_age_field.hide();
			property_types_field.hide();
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

	let content_table = $w("#apicontent");
	let endpoint = $w("#selectsearchapi").value;
	let extra_field  = $w("#extraField");
	let property_types_field = $w("#propertyTypes");
	let property_age_field = $w("#propertyAge");
	let postcode = $w("#postalcode");

	let data;

	switch(endpoint){
		case "prices":
			postcode = postcode.value;
			let bedrooms = extra_field.value;
			data = {"postcode":postcode,"bedrooms":bedrooms};
			break;
		case "sold_prices":
			postcode = postcode.value;
			let property_type = extra_field.value;
			let max_age = property_age_field.value;
			data = {"postcode": postcode, "property_type": property_type, "max_age": max_age};
			break;
		default:
			postcode = postcode.value;
			data = {"postcode":postcode};
			break;
	}
	let response = await fetch_sales_api(data,endpoint)
	console.log("response : ", response);
	if (response['status'] === "success"){
		let display_interface = await show_output_interface(endpoint)
		/** at this stage consider that the output contains the elements needed to display each of the endpoints */
		switch(endpoint){
			case "prices":{
				let api_content = display_interface[0];
				api_content.rows = [{average: response['data']['average'], d90pc_range:response['data']['90pc_range'],
					d80pc_range:response['data']['80pc_range'], d70pc_range:response['data']['70pc_range'],
					d10pc_range:response['data']['100pc_range']
				}]
			}
				break;
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
		case "prices":{
				let content_table = $w("#apicontent");
				output_interface.push(content_table);

		}
			break;
		case "sold_prices":
			/*** add the template for sold_prices here */
			break;
		case "sold_prices_per_sqf":
		/*** add the template for sold_prices per sqf here */
			break;
		case "growth":
		/*** add the template for growth here */
			break;

		case "postcode_stats":
		/*** add the template for postcode_stats here */
			break;
		case "sourced_properties":
		/*** add the template for sourced_properties here */
			break;

		case "property_info":
		/*** add the template for property_info here */
			break;
		case "development_gdv":
		/*** add the template for development_gdv here */
			break;
		default:
			break;
	}

	/** The options above are only for sales
	 *
	 * rental templates
	 * area templates
	 * evaluate templates still need to be added
	 */

	return output_interface
}