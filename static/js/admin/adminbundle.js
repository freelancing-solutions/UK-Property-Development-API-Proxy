

self.addEventListener('load', function(){
    //TODO- if its mobile screen rearrange the row orders otherwise leave defaults
    let display_arrangement = document.getElementById('display_arrangement')

    let admin_defaults = {}

    let display = document.getElementById('manager_screen')

    document.getElementById('property_types_butt').addEventListener('click', render_property_types)
    document.getElementById('construction_dates').addEventListener('click', render_construction_dates)
    document.getElementById('finish_quality').addEventListener('click', render_finish_quality)
    document.getElementById('outdoor_space').addEventListener('click', render_outdoor_space)

    /** Sidebar Menu DOM **/
    document.getElementById( 'tests_link').addEventListener('click', render_tests_page)

    let init_get = {
            method: 'GET',
            headers: new Headers({ 'Content-type': 'application/json'}),
            mode: 'cors',
            credentials: 'same-origin',
            cache:'no-cache'
    }

    //Init Function
    let init = async function(){
        console.log(admin_defaults);
        //fetching api search defaults
        let new_request = new Request('/admin/admin-api-defaults', init_get)
        let response = await fetch(new_request)
        admin_defaults = await response.json()
        console.log('Admin Defaults : ', admin_defaults)
    }

    let update_settings = async e => {
        //fetching api settings defaults
        let new_request = new Request('/admin/fetch-api-settings', init_get)
        let response = await fetch(new_request)
        let setting_defaults = await response.json()

        if (setting_defaults.status === 'success'){
                await render_settings_updates(setting_defaults)
                if (setting_defaults.payload.api_status){
                    await render_shutdown_butt()
                }else{
                    await render_restart_butt()
                }
            }
    }
    /** update settings **/

    /** form Renderers **/
    async function render_property_types(e){
            //meant to prevent the link from doing anything it ussually does
            e.preventDefault();

            display.innerHTML = `
                <div class="card-header">
                    <h3 class="card-title"> Property types defaults</h3>
                </div>
                
                <div class="card-body">
                    <p class="card-text"> Set Property types preferences</p>
                    <form class="form-horizontal">
                        <div class="form-group">
                            <div class="input-group-prepend">
                                <label>Select Available Property Types</label>
                            </div>
                            <select class="form-control" multiple="true" id="property_types_selections">                       
                                <option value="flat" > flat </option>
                                <option value="detached_house"> detached house </option>
                                <option value="terraced_house"> terraced house </option>
                                <option value="semi_detached_house"> semi detached house </option>                            
                            </select>
                        </div>
                        <div class="form-group">
                            <button class="btn btn-primary" id="update_property_types_butt">
                                <i class="fas fa-save"> </i> 
                                Update Defaults 
                            </button>
                        </div>
                        <div class="form-group" id="message_data">
                        
                        </div>
                    </form>
                </div>
            `

                let type_selection = document.getElementById('property_types_selections');
                console.log('Am i loading');
                    let init_get = {
                        method : "GET",
                        headers: new Headers({ 'Content-type': 'application/json'}),
                        mode: 'cors',
                        credentials: 'same-origin',
                        cache:'no-cache'
                    }
                    let new_request = new Request('/admin/property-types', init_get)
                    let response = await fetch(new_request)
                    let property_types_data = await response.json()
                    try{
                        await property_types_data.payload.forEach(type => {
                            console.log('Types from datastore : ', type);
                                switch(type){
                                    case 'flat': type_selection.options[0].selected = true; break;
                                    case 'detached_house': type_selection.options[1].selected = true; break;
                                    case 'terraced_house': type_selection.options[2].selected = true; break;
                                    case 'semi_detached_house': type_selection.options[3].selected = true; break;
                                }
                        })
                    }catch(e){}
            document.getElementById('update_property_types_butt').addEventListener('click', async (e) =>{
                //prevent the button from doing the ussual when clicked
                e.preventDefault();
                let property_types = document.getElementById('property_types_selections');
                let selected_property_types = {
                    'flat': property_types.options[0].selected,
                    'detached_house': property_types.options[1].selected,
                    'terraced_house': property_types.options[2].selected,
                    'semi_detached_house': property_types.options[3].selected
                }
                console.log(JSON.stringify(selected_property_types));
                let init_post = {
                    method: 'POST',
                    headers: new Headers({ 'Content-type': 'application/json'}),
                    mode: 'cors',
                    credentials: 'same-origin',
                    body:JSON.stringify(selected_property_types),
                    cache:'no-cache'
                }
                let update_request = new Request('/admin/property-types', init_post)
                let response = await fetch(update_request)
                let response_data = await response.json()
                document.getElementById('message_data').innerHTML = response_data.message
            })

            //meant to prevent the link from doing anything it ussually does
            return false

    }

    async function render_construction_dates(e){
        e.preventDefault();
        display.innerHTML = `
                <div class="card-header">
                    <h3 class="card-title"> Construction Dates defaults</h3>
                </div>           
                <div class="card-body">
                    <p class="card-text"> Set Allowed Construction Dates</p>
                    <form class="form-horizontal">
                        <div class="form-group">
                            <div class="input-group-prepend">
                                <label>Select Available Construction Dates</label>
                            </div>
                            <select class="form-control" multiple="true" id="construction_dates_select">                       
                                <option value="pre_1914" > Pre 1914 </option>
                                <option value="1914_2000"> 1914 - 2000 </option>
                                <option value="2000_onwards"> 2000_onwards </option>                                                            
                            </select>
                        </div>
                        <div class="form-group">
                            <button class="btn btn-primary" id="update_defaults">
                                <i class="fas fa-save"> </i> 
                                Update Defaults 
                            </button>
                        </div>
                        <div class="form-group" id="message_data">
                        
                        </div>
                    </form>
                </div>                        
        `
                let dates_selection = document.getElementById('construction_dates_select');
                    console.log('loading dates selections');
                    let init_get = {
                        method : "GET",
                        headers: new Headers({ 'Content-type': 'application/json'}),
                        mode: 'cors',
                        credentials: 'same-origin',
                        cache:'no-cache'
                    }
                    let new_request = new Request('/admin/construction-dates', init_get)
                    let response = await fetch(new_request)
                    let dates_selections_data = await response.json()
                    try{
                        await dates_selections_data.payload.forEach(date => {
                            console.log('Types from datastore : ', date);
                                switch(date){
                                    case 'pre_1914': dates_selection.options[0].selected = true; break;
                                    case '1914_2000': dates_selection.options[1].selected = true; break;
                                    case '2000_onwards': dates_selection.options[2].selected = true; break;
                                }
                        })
                    }catch(e){}

                    document.getElementById('update_defaults').addEventListener('click', async (e) =>{
                        //prevent the button from doing the ussual when clicked
                        e.preventDefault();
                        let dates_selection = document.getElementById('construction_dates_select');
                        let dates_selected = {
                            'pre_1914': dates_selection.options[0].selected,
                            '1914_2000': dates_selection.options[1].selected,
                            '2000_onwards': dates_selection.options[2].selected,
                        }
                        console.log(JSON.stringify(dates_selected));
                        let init_post = {
                            method: 'POST',
                            headers: new Headers({ 'Content-type': 'application/json'}),
                            mode: 'cors',
                            credentials: 'same-origin',
                            body:JSON.stringify(JSON.stringify(dates_selected)),
                            cache:'no-cache'
                        }
                        let update_request = new Request('/admin/construction-dates', init_post)
                        let response = await fetch(update_request)
                        let response_data = await response.json()
                        document.getElementById('message_data').innerHTML = response_data.message
                    })

                    return false
    }

    async function render_finish_quality(e){
        e.preventDefault();
        display.innerHTML = `
                <div class="card-header">
                    <h3 class="card-title"> Finish Quality Defaults</h3>
                </div>
                <div class="card-body">
                    <p class="card-text"> Set Allowed Finish Quality Settings</p>
                    <form class="form-horizontal">
                        <div class="form-group" data-select2-id="95">
                          <label>Multiple</label>
                          <select id="finish_quality_select" class="select2" multiple="" data-placeholder="Select Finish Quality" style="width: 100%;" data-select2-id="7" tabindex="-1" aria-hidden="true">
                                <option value="very_high" data-select2-id="0" > Very High </option>
                                <option value="high" data-select2-id="1"> High </option>
                                <option value="average" data-select2-id="2"> Average </option>
                                <option value="below_average" data-select2-id="3"> Below Average </option>
                                <option value="unmodernised" data-select2-id="4"> Un Modernised </option>
                          </select>
                        </div>
                        <div class="form-group">
                            <button type="button" class="btn btn-primary" id="update_property_types_butt">
                                <i class="fas fa-save"> </i> 
                                Update Defaults 
                            </button>
                        </div>
                        <div class="form-group" id="message_data">
                        
                        </div>
                    </form>
                </div>
        
        `
                let finishing_selection = document.getElementById('finish_quality_select');
                    console.log('loading finishing quality selections');
                    let init_get = {
                        method : "GET",
                        headers: new Headers({ 'Content-type': 'application/json'}),
                        mode: 'cors',
                        credentials: 'same-origin',
                        cache:'no-cache'
                    }
                    let request = new Request('/admin/finish-quality', init_get)
                    let response = await fetch(request)
                    let finish_quality_data = await response.json()
                    try{
                        await finish_quality_data.payload.forEach(quality => {
                            console.log('Types from datastore : ', quality);
                                switch(quality){
                                    case 'very_high':finishing_selection.options[0].selected = true; break;
                                    case 'high': finishing_selection.options[1].selected = true; break;
                                    case 'average': finishing_selection.options[2].selected = true; break;
                                    case 'below_average': finishing_selection.options[3].selected = true; break;
                                    case 'unmodernised': finishing_selection.options[4].selected = true; break;
                                }
                        })
                    }catch(e){}

                    document.getElementById('update_defaults').addEventListener('click', async (e) =>{
                        //prevent the button from doing the ussual when clicked
                        e.preventDefault();
                        let finishing_selection = document.getElementById('finish_quality_select');
                        let finish_selected = {
                            'very_high': finishing_selection.options[0].selected,
                            'high': finishing_selection.options[1].selected,
                            'average': finishing_selection.options[2].selected,
                            'below_average': finishing_selection.options[3].selected,
                            'unmodernised': finishing_selection.options[4].selected,
                        }
                        console.log(JSON.stringify(finish_selected));
                        let init_post = {
                            method: 'POST',
                            headers: new Headers({ 'Content-type': 'application/json'}),
                            mode: 'cors',
                            credentials: 'same-origin',
                            body:JSON.stringify(finish_selected),
                            cache:'no-cache'
                        }
                        let update_request = new Request('/admin/finish-quality', init_post)
                        let response = await fetch(update_request)
                        let response_data = await response.json()
                        document.getElementById('message_data').innerHTML = response_data.message
                        return false
                    })

                    return false

    }

    async function render_outdoor_space(e){
        e.preventDefault();
        display.innerHTML = `
                <div class="card-header">
                    <h3 class="card-title"> Outdoor Space Defaults</h3>
                </div>
                
                <div class="card-body">
                    <p class="card-text"> Set Allowed Outdoor Space Settings</p>
                    <form class="form-horizontal">
                        <div class="form-group">
                            <div class="input-group-prepend">
                                <label>Select Available Outdoor Space Settings</label>
                            </div>
                            <select class="form-control" multiple="true" id="finish_quality_select">                       
                                <option value="none" > None </option>
                                <option value="balcony_terrace"> Balcony Terrace </option>
                                <option value="garden"> Garden </option>
                                <option value="garden_very_large"> Large Garden </option>
                            </select>
                        </div>
                        <div class="form-group">
                            <button class="btn btn-primary" id="update_defaults">
                                <i class="fas fa-save"> </i> 
                                Update Defaults 
                            </button>
                        </div>
                        <div class="form-group" id="message_data">
                        
                        </div>
                    </form>
                </div>       
        `
    }

    /** sidebar menu renderes **/
    async function render_tests_page(e){
        e.preventDefault()
        async function call_api(endpoint, data){
                let init_post = {
                    method: 'POST',
                    headers: new Headers({ 'Content-type': 'application/json'}),
                    mode: 'cors',
                    credentials: 'same-origin',
                    cache:'no-cache',
                    body: data
                }
                let url = '/api/v1/'+ endpoint.replace('_','-')
                let request = new Request(url,init_post)
                let response = await fetch(request)
                let response_data = await response.json()
                if (response_data.status === "success"){
                    document.getElementById('json_results').innerHTML = JSON.stringify(response_data)
                    document.getElementById('api_results_message').innerHTML = `
                    <span class="text-info"> API Endpoint Worked fine results are displayed above</span>
                    `
                }else{
                    document.getElementById('api_results_message').innerHTML = `
                    <span class="text-info"> There seems to be a problem with this Endpoint , consider the following steps:</span>
                    <ul>
                        <li>Check if your API Health is OK and State is UP</li>
                        <li>Check your input and make sure its properly entered</li>
                        <li>If errors still persist manually Purge API Caches</li>
                        <li>If errors persist Check API Health @ <a href="https://propertydata.co.uk/api/status"> //propertydata.co.uk/api/status</a></li>
                        <li>If you still didn't find the problem and cannot rectify the error, let your developer know of the problem</li>                        
                    </ul>
                    `
                }
        }

        display.innerHTML = `
            <div class="card-header">
                <h3 class="card-title"> API Test Tool Kit</h3>
            </div>                        
            <div class="card-body">
                    <div class="card-body">
                        <div class="card-header">
                            <h3 class="card-title"> Sales API</h3>
                        </div>                        
                        <form class="form-horizontal">
                            <div class="form-group">
                                <div class="input-group-prepend">
                                    <label>Select Endpoint</label>
                                </div>
                                <select class="form-control" id="sales_endpoint">
                                    <option value="valuation_sales" disabled> Valuation Sale </option>
                                    <option value="prices"> Prices </option>
                                    <option value="price_per_sqf"> Price Per SQF </option>
                                    <option value="sold_prices"> Sold Prices </option>
                                    <option value="sold_prices_per_sqf" disabled> Sold Prices Per SQF </option>
                                    <option value="growth"> Growth </option>
                                    <option value="postcode_stats" disabled> Post Code Stats </option>
                                    <option value="sourced_properties"> Sourced Properties </option>
                                    <option value="property_info" disabled> Property Info </option>
                                    <option value="development_gdv" disabled> Development gdv </option>                                                                        
                                </select>                                
                            </div>
                            <div id="api_description"></div>
                            <div class="form-group">
                                <input id="postcode" class="form-control" placeholder="postcode" />
                            </div>
                            <div class="form-group">
                                <input id="bedrooms" class="form-control" placeholder="bedrooms" />
                            </div>
                            <button class="btn btn-success btn-sm" id="test_sales_api"> Click to Test </button>
                                                                                        
                            <div class="form-group align-items-start">
                                <pre>
                                    <code id="json_results">
                                    
                                    </code>
                                </pre>                                
                            </div>
                            <div class="form-group align-items-start">
                                <pre>
                                    <div class="card-text" id="api_results_message">
                                        <p class="text-info"></p>
                                    </div>
                                </pre>
                            </div>                            
                        </form>
                    </div>                               
            </div>      
        `
        document.getElementById('sales_endpoint').addEventListener('click', e => {
            let description_dom = document.getElementById('api_description')
            description_dom.innerHTML = ""

            /** descriptions **/
            let prices_description = `
                <div class='card-body'>
                     <div class="card-header">
                        <h5 class="card-title">Prices API</h5>    
                    </div>
                     <div class="text-info">
                        <p>Availability : <em>England, Wales, Scotland, N.Ireland</em></p>
                        <p>Description : For a given UK postcode (full, district or sector) and optional filters, returns statistical average and confidence intervals of live property asking prices, from the smallest radius at which there is reasonable data.</p>
                        <p>Input : <em>postcode, number of bedrooms</em></p>                                                                         
                    </div>
                </div>
            
            `
            let price_per_sqf_description = `
                <div class="card-body">
                    <div class="card-header">
                        <h3 class="card-title"> Prices Per SQF</h3>    
                    </div>
                    <div class="text-info">
                        <p>Availability: <em>England, Wales, Scotland, N.Ireland</em></p>
                        <p>Description: For a given UK postcode (full, district or sector), returns statistical average and confidence intervals of live property asking prices per square foot, from the smallest radius at which there is reasonable data. Read more about our price per square foot data here.</p>
                        <p>Input: <em>postcode</em></p>
                    </div>
                </div>
            `
            let sold_prices_per_sqf_description = `
                <div class="card-body">
                    <div class="card-header">
                        <h3 class="card-title">Sold Prices Per SQF</h3>    
                    </div>
                    <div class="text-info">
                        <p>Availability: <em>England, Wales</em></p>
                        <p>For a given UK postcode (full, district or sector) and optional filters, returns statistical average and confidence intervals of property sold prices per square foot.</p>
                        <p>Input: <em>postcode</em></p>
                    </div>
                </div>                       
            `
            let growth_description = `
                <div class="card-body">
                    <div class="card-header">
                        <h3 class="card-title">Growth</h3>    
                    </div>
                    <div class="text-info">
                        <p>Availability: <em>England, Wales, Scotland, N.Ireland</em></p>
                        <p>For a given UK postcode (full, district or sector), returns five-year capital growth figures.</p>
                        <p>Input: <em>postcode</em></p>
                    </div>
                </div>                                               
            `
            let sourced_properties_description = `
                <div class="card-body">
                    <div class="card-header">
                        <h3 class="card-title">Sourced Properties</h3>    
                    </div>
                    <div class="text-info">
                        <p>Availability: <em>England, Wales, N.Ireland</em></p>
                        <p>Returns properties currently on any one of our specialist situation property sourcing lists, within a given radius of a supplied postcode. Properties are sorted by distance to the input postcode, where the closest properties are returned first.</p>
                        <p>Input: <em>postcode</em></p>
                    </div>
                </div>                                                           
            `
            /** insert description **/
            switch (e.target.value){
                case "prices":description_dom.innerHTML = prices_description;break;
                case "price_per_sqf": description_dom.innerHTML = price_per_sqf_description;break;
                case "sold_prices_per_sqf": description_dom.innerHTML = sold_prices_per_sqf_description; break;
                case "growth": description_dom.innerHTML = growth_description; break;
                case "sourced_properties": description_dom.innerHTML = sourced_properties_description; break;
            }
        })

        document.getElementById('test_sales_api').addEventListener('click', e  =>{
            e.preventDefault()
            let postcode = ""
            let bedrooms = ""
            try {
                postcode = document.getElementById("postcode").value;
            }catch(e){}
            try{
                bedrooms = document.getElementById('bedrooms').value;
            }catch (e){}

            let endpoint = document.getElementById('sales_endpoint').value;
            console.log('postcode : ', postcode);
            console.log('bedrooms : ', bedrooms);
            console.log('endpoint : ', endpoint);

            switch (endpoint){
                case "prices": call_api(endpoint,JSON.stringify({postcode:postcode,bedrooms:bedrooms}));break;
                case "price_per_sqf": call_api(endpoint, JSON.stringify({postcode:postcode}));break;
                // case "sold_prices": call_api(endpoint, JSON.stringify({postcode}));break;
                case "sold_prices_per_sqf": call_api(endpoint, JSON.stringify({postcode:postcode}));break;
                case "growth": call_api(endpoint, JSON.stringify({postcode:postcode}));break;
                case "sourced_properties": call_api(endpoint, JSON.stringify({postcode:postcode}));break;
            }

            return false
        })
    }

    /** state updates renders **/
    async function render_settings_updates(settings){
                    document.getElementById('total_requests_label').innerHTML =`
                    <span class="text text-info text-bold"> Total Requests : ${settings.payload.total_requests} </span>`
                    document.getElementById('cached_requests_label').innerHTML = `
                    <span class="text text-warning text-bold"> Cached Requests : ${settings.payload.cached_requests} </span>\`
                    `
                    document.getElementById('failed_requests_label').innerHTML = `
                    <span class="text text-danger text-bold"> Failed Requests : ${settings.payload.failed_requests} </span>\`
                    `
                    if (settings.payload.api_status){
                        document.getElementById('api_state').innerHTML = `                        
                            <li id="api_state"> <span class="text text-info"> API State : <em class="fa fa-thumbs-up"> Up</em></span> </li>
                        `
                    }else{
                        document.getElementById('api_state').innerHTML = `                        
                            <li id="api_state"> <span class="text text-danger"> API State : <em class="fa fa-thumbs-down"> Down</em></span> </li>
                        `
                    }

                    if (settings.payload.api_health){
                        document.getElementById('api_health').innerHTML = `
                            <span class="text text-info" >API Health : <em class="fa fa-user"> Happy </em> </span>
                        `
                    }else{
                        document.getElementById('api_health').innerHTML = `
                            <span class="text text-danger" >API Health : <em class="fa fa-user-check"> Sad</em> </span>
                        `
                    }
                    document.getElementById('quick_actions_messages').innerHTML =''

    }

    async function render_shutdown_butt(){
        document.getElementById('action_buttons').innerHTML = `
              <button class="btn btn-danger" id="shutdown_api">
                  <i class="fas fa-thumbs-down"> </i>
                  Shutdown API
              </button>                    
        `
        document.getElementById('shutdown_api').addEventListener('click', async e => {

            e.preventDefault();

            let init_post = {
                method: 'POST',
                headers: new Headers({ 'Content-type': 'application/json'}),
                mode: 'cors',
                credentials: 'same-origin',
                cache:'no-cache'
            }
            let request = new Request('/admin/shutdown-api', init_post)
            console.log('shutdown api is being clicked', request);
            let response = await fetch(request)
            let response_data = await response.json()
            document.getElementById('quick_actions_messages').innerHTML = response_data.message
        })
    }

    async function render_restart_butt(){
        document.getElementById('action_buttons').innerHTML = `
              <button class="btn btn-primary" id="restart_api">
                  <i class="fas fa-thumbs-up"> </i>
                  Restart API
              </button>                    
        `
        document.getElementById('restart_api').addEventListener('click', async e => {
            e.preventDefault();

            let init_post = {
                method: 'POST',
                headers: new Headers({ 'Content-type': 'application/json'}),
                mode: 'cors',
                credentials: 'same-origin',
                cache:'no-cache'
            }
            let request = new Request('/admin/restart-api', init_post)
            console.log('shutdown api is being clicked', request);
            let response = await fetch(request)
            let response_data = await response.json()
            document.getElementById('quick_actions_messages').innerHTML = response_data.message
        })

    }


    init().then(response => {
        console.log("admin initialized")
        setInterval(update_settings,50000);
    });
    /* initialize */

});
