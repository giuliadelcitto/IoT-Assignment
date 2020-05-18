function sending_data(){
	//change the div content to match the condition to send data
	document.getElementById('send_d').innerHTML = "Sending data";
}

function sending_act(){
	//change the div content to match the condition to send activity
	document.getElementById('send_a').innerHTML = "Sending activity";
}

function stop_send(){
	//change the div content to NOT match the condition to send data and activity
	document.getElementById('send_d').innerHTML = "No data send";
	document.getElementById('send_a').innerHTML = "No activity send";
}


function send_data(x, y, z){
	//the data are format in json as require from thingsboard
	var msg=JSON.stringify({X : x, Y : y , Z : z});
	//use a post method to send data to the right device using the ACCESS TOKEN
	//no-cors option to avoid CORS ERROR
	fetch('https://demo.thingsboard.io/api/v1/N2AxGgvu8vkscRonykTT/telemetry', {
        method: "POST",
        mode: 'no-cors',
        body: msg,
        headers: {
            'Content-type': 'application/json'
        }
    });
}

function send_activity( act ){
	//the data are format in json as require from thingsboard
	var msg = { activity : act }
	//use a post method to send activity to the right device using the ACCESS TOKEN
	//no-cors option to avoid CORS ERROR
	fetch('https://demo.thingsboard.io/api/v1/xQGhgoE4a5LdplwyVXlT/telemetry', {
        method: "POST",
        mode: 'no-cors',
        body: JSON.stringify(msg),
        headers: {
            'Content-type': 'application/json'
        }
    });
}

