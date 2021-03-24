/*
* Consumer for Sales API
*
*
* */

let templates = (temp) => {
    switch(temp) {
        case 'prices': return `
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title"> Prices </h3>
                                </div>
                                <!-- expected arguments
                                    - postcode
                                    - bedrooms
                                -->
                            </div>
        `
        case 'valuation-sale' :return ` 
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title"> Valuation Sale</h3>
                                </div>
                                <!-- expected arguments
                                    - postcode 
                                    - internal_area 
                                    - property_type 
                                    - construction_date 
                                    - bedrooms
                                    - bathrooms 
                                    - finish_quality 
                                    - outdoor_space 
                                    - off_street_parking
                                -->                                
                            </div>
        `
        case 'price-per-sqf': return `
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title"> Price Per SQF</h3>
                                </div>
                                <!-- expected arguments
                                    - postcode
                                -->
                                
                            </div>               
        `
        case 'sold-prices':return `
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title"> Sold Prices</h3>
                                </div>
                                <!-- expected arguments
                                    - postcode
                                    - property_type
                                    - max_age
                                -->
                                
                            </div>
        `
        case 'sold-prices-per-sqf':return `
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title"> Sold Prices Per SQF</h3>
                                </div>
                                <!-- expected arguments
                                    - postcode
                                -->
                                
                            </div>
        `
        case 'growth':return `
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title"> Growth</h3>
                                </div>
                                <!-- expected arguments
                                    - postcode
                                -->
                                
                            </div>
        `
        case 'postcode-stats': return `
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title"> Postcode Statistics</h3>
                                </div>
                                <!-- expected arguments
                                    - postcode
                                -->
                                
                            </div>
        
        `
        case 'sourced-properties': return `
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title"> Sourced Properties</h3>
                                </div>
                                <!-- expected arguments
                                    - postcode
                                    - property_list
                                    - radius
                                -->
                                
                            </div>               
        `
        case 'property-info': return `
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title"> Property Info</h3>
                                </div>
                                <!-- expected arguments
                                    - property_id
                                -->
                                
                            </div>                       
        `
        case 'development-gdv': return `
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title"> Development GDV</h3>
                                </div>
                                <!-- expected arguments
                                    - property_id
                                -->
                                
                            </div>                               
        `

    }
}

let apiSalesConsumer = {
    /** use handleBars to load dynamic forms for any website, the website need to only declare the following div tags
     *  main_content, and messages
     *
     * **/
    main_content_dom : "",
    messages_dom : "",
    dom_attached : false,
    api_endpoint : "",
    auth_token : "",
    request_data : {},
    request_headers : new Headers({'Content-Type': 'application/json'}),
    init_request : {
        'method': 'POST',
        'mode': 'cors',
        'body': JSON.stringify(this.request_data),
        'headers': this.request_headers
    },
    attach_dom : async function(){
        try{
            this.main_content_dom = document.getElementById('main_content')
            this.messages_dom = document.getElementById('messages')
            this.dom_attached = true
        }catch(e){
            this.dom_attached = false
        }
    },
    load_template : async function(template){
        return templates[template]
    },
    load_sales_api_form : async function(form_type){
        /** given a user choice load the relevant form to search api **/
        await this.attach_dom()
        if (this.dom_attached === true){
            this.main_content_dom.innerHTML = await this.load_template(form_type)
        }
    },

    fetch_data_from_form : async form => {
      /** locate and fetch all data from form, then locate the relevant endpoint **/
    },

    make_request : async () => {
        /** check for endpoint validity and data then make request and present the results to user **/
        let request = new Request(this.api_endpoint, this.init_request)
    },


}