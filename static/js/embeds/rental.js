self.addEventListener('load', async e => {

    let msToDate = (milliseconds) => ' ' + (new Date(milliseconds)) + ' ';
    let disp_date = dtime => msToDate(dtime).split("GMT")[0];
    let disp_num = number => String(number).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    let elapse_time = e_time => `${new Date(e_time).getHours()}:${new Date(e_time).getMinutes()}:${new Date(e_time).getSeconds()}`
    let disp_latent = time => `${new Date(parseFloat(time)).getMilliseconds()}`

    let post_code_dom = document.getElementById('post_code');
    let bedrooms_dom = document.getElementById('bedrooms');
    let get_data = async function(json_data){
        return json_data['data']['long_let']
    }
    let display_raw_data = async function(raw_data){
        console.log("RAW DATA: ", raw_data);
            let node = ''
        raw_data.forEach(house => {
            console.log(house);
            node += `
                <tr>
                    <td>${house.type}</td>
                    <td>${house.bedrooms}</td>
                    <td>${house.distance}</td>
                    <td>${house.lng}</td>
                    <td>${house.lat}</td>
                    <td>${"&#163; "+disp_num(house.price)}</td>
                </tr>
            `
        });

        document.getElementById('price_data').innerHTML = node;
        return true
    }
    document.getElementById('search').addEventListener('click', async e => {
        e.preventDefault();
        if (post_code_dom.value === "") {
            alert("Please enter a valid UK Postcode");
            return false;
        }
        if (bedrooms_dom.value === "") {
            alert("Please enter number of bedrooms");
            return false;
        }
        let init_post = {
            'method': 'POST',
            'mode': 'cors',
            'body': JSON.stringify({'postcode': post_code_dom.value, 'bedrooms': bedrooms_dom.value}),
            'headers': new Headers({'content-type': 'application/json'})
        }

        let request = new Request('/api/v1/rents', init_post);
        let response = await fetch(request);
        console.log('response: ', response);
        let json_data = await response.json();
        console.log('json_data: ', json_data);
        if (response.ok === true) {
            let averages_data = await get_data(json_data);
            document.getElementById('average_prices').innerHTML = `Average Prices :${"&#163; "+disp_num(averages_data['average'])}`;
            document.getElementById('d70_pc').innerHTML = `
            70 Percentile Range = 
            ${"&#163; "+disp_num(averages_data['70pc_range'][0]) + " to &#163; " + disp_num(averages_data['70pc_range'][1])}`;
            document.getElementById('d80_pc').innerHTML = `
            80 Percentile Range = 
            ${"&#163; "+disp_num(averages_data['80pc_range'][0]) + " to &#163; " + disp_num(averages_data['80pc_range'][1])}`;
            document.getElementById('d90_pc').innerHTML = `
            90 Percentile Range = 
            ${"&#163; "+disp_num(averages_data['90pc_range'][0]) + " to &#163; " + disp_num(averages_data['90pc_range'][1])}`;
            document.getElementById('d100_pc').innerHTML = `
            100 Percentile Range = 
            ${"&#163; "+disp_num(averages_data['100pc_range'][0]) + " to &#163; " + disp_num(averages_data['100pc_range'][1])}`;
            let response = await display_raw_data(averages_data['raw_data']);
        }
        return false
    })

});