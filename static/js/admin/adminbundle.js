

self.addEventListener('load', function(){
    //TODO- if its mobile screen rearrange the row orders otherwise leave defaults
    let display_arrangement = document.getElementById('display_arrangement')

    let admin_defaults = {}

    let display = document.getElementById('manager_screen')

    document.getElementById('property_types_butt').addEventListener('click', render_property_types)
    document.getElementById('construction_dates').addEventListener('click', render_construction_dates)
    document.getElementById('finish_quality').addEventListener('click', render_finish_quality)
    document.getElementById('outdoor_space').addEventListener('click', render_outdoor_space)

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
            //meant to prevent the link from doing anything it ussually does
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
                        <div class="form-group">
                            <div class="input-group-prepend">
                                <label>Select Available Finish Quality Settings</label>
                            </div>
                            <select class="form-control" multiple="true" id="finish_quality_select">                       
                                <option value="very_high" > Very High </option>
                                <option value="high"> High </option>
                                <option value="average"> Average </option>
                                <option value="below_average"> Below Average </option>
                                <option value="unmodernised"> Un Modernised </option>
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
        setInterval(update_settings,10000);
    });
    /* initialize */

});
