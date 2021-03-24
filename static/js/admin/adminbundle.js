

self.addEventListener('load', function(){
    //TODO- if its mobile screen rearrange the row orders otherwise leave defaults
    let display_arrangement = document.getElementById('display_arrangement');



    let display = document.getElementById('manager_screen');

    document.getElementById('property_types_butt').addEventListener('click', (e)=>{
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
                            <label>Select Property Types</label>
                        </div>
                        <select class="form-control" multiple="true" id="property_types_selections">
                            <option value="flat"> flat </option>
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
            let update_request = new Request('/admin', init_post)
            let response = await fetch(update_request)
            let response_data = await response.json()
            document.getElementById('message_data').innerHTML = response_data.message
        })
        return false
    });





})
