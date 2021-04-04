self.addEventListener('load', async e => {
    let msToDate = (milliseconds) => ' ' + (new Date(milliseconds)) + ' ';
    let disp_date = dtime => msToDate(dtime).split("GMT")[0];
    let disp_num = number => String(number).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    let elapse_time = e_time => `${new Date(e_time).getHours()}:${new Date(e_time).getMinutes()}:${new Date(e_time).getSeconds()}`
    let disp_latent = time => `${new Date(parseFloat(time)).getMilliseconds()}`

    let set_data = async function(json_data) {
        console.log("data : ", json_data)
        document.getElementById('degrees').innerHTML = `
        Proportion With Degrees : ${json_data['proportion_with_degree']} %
        `;
        document.getElementById('vehicles').innerHTML = `
            Vehicles Per Household : ${json_data['vehicles_per_household']}
        `
        document.getElementById('ab').innerHTML = `AB : ${json_data['social_grade'].ab} %`
        document.getElementById('c1').innerHTML = `C1 : ${json_data['social_grade'].c1} %`
        document.getElementById('c2').innerHTML = `C2 :${json_data['social_grade'].c2} %`
        document.getElementById('de').innerHTML = `DE :${json_data['social_grade'].de} %`

        document.getElementById('constituencies').innerHTML = ` constituencies : ${json_data['politics'].constituences[0]}`
        document.getElementById('brexit').innerHTML = `Brexit Party : ${json_data['politics']['results']["Brexit Party"]}`
        document.getElementById('conservative').innerHTML = `Conservative : ${json_data['politics']['results']["Conservative"]}`
        document.getElementById('green').innerHTML = `Green : ${json_data['politics']['results']["Green"] }`
        document.getElementById('labour').innerHTML = `Labour : ${json_data['politics']['results']["Labour"]}`
        document.getElementById('liberal').innerHTML = `Liberal Democrat : ${json_data['politics']['results']["Liberal Democrat"]}`

        let demo_data_dom = document.getElementById('demo_data').innerHTML = `
        <tr>
            <td>0-4</td>
            <td>${json_data['age']['0-4']} %</td>            
        </tr>
        <tr>
            <td>5-9</td>
            <td>${json_data['age']['5-9']} %</td>            
        </tr>
        <tr>
            <td>10-14</td>
            <td>${json_data['age']['10-14']} %</td>            
        </tr>
        <tr>
            <td>15-19</td>
            <td>${json_data['age']['15-19']} %</td>            
        </tr>
        <tr>
            <td>20-24</td>
            <td>${json_data['age']['20-24']} %</td>            
        </tr>
        <tr>
            <td>25-29</td>
            <td>${json_data['age']['25-29']} %</td>            
        </tr>
        <tr>
            <td>30-34</td>
            <td>${json_data['age']['30-34']} %</td>            
        </tr>
        <tr>
            <td>35-39</td>
            <td>${json_data['age']['35-39']} %</td>            
        </tr>
        <tr>
            <td>40-44</td>
            <td>${json_data['age']['40-44']} %</td>            
        </tr>
        <tr>
            <td>45-49</td>
            <td>${json_data['age']['45-49']} %</td>            
        </tr>
        <tr>
            <td>50-54</td>
            <td>${json_data['age']['50-54']} %</td>            
        </tr>
        <tr>
            <td>59-59</td>
            <td>${json_data['age']['55-59']} %</td>            
        </tr>
        <tr>
            <td>60-64</td>
            <td>${json_data['age']['60-64']} %</td>            
        </tr>
        <tr>
            <td>65-69</td>
            <td>${json_data['age']['65-69']} %</td>            
        </tr>
        <tr>
            <td>70-74</td>
            <td>${json_data['age']['70-74']} %</td>            
        </tr>
        <tr>
            <td>75-79</td>
            <td>${json_data['age']['75-79']} %</td>            
        </tr>
        <tr>
            <td>80-84</td>
            <td>${json_data['age']['80-84']} %</td>            
        </tr>
        <tr>
            <td>85-89</td>
            <td>${json_data['age']['85-89']} %</td>            
        </tr>
        
        `

        return true;

        };


    document.getElementById('search').addEventListener('click', async e => {
        e.preventDefault();
        let postcode = document.getElementById('post_code').value;
        if (postcode === ""){alert("Enter valid UK postcode"); return false}
        let init_post = {
            'method': 'POST',
            'mode': 'cors',
            'body': JSON.stringify({'postcode': postcode}),
            'headers': new Headers({'content-type': 'application/json'})
        }
        let request = new Request('/api/v1/demographics', init_post);
        let response = await fetch(request);
        let json_data = await response.json();
        if (response.ok === true){
            let response = await set_data(json_data['data'])
        }
        return false;
    })




})