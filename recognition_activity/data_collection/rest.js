function sending_data(){
	document.getElementById('send_d').innerHTML = "Sending data";
}

function sending_act(){
	document.getElementById('send_a').innerHTML = "Sending activity";
}

function stop_send(){
	document.getElementById('send_d').innerHTML = "No data send";
	document.getElementById('send_a').innerHTML = "No activity send";
}


function send_data(x, y, z){
	var msg={X : x, Y : y , Z : z};
	fetch('https://demo.thingsboard.io/api/v1/N2AxGgvu8vkscRonykTT/telemetry', {
        method: "POST",
        mode: 'no-cors',
        body: JSON.stringify(msg),
        headers: {
            'Content-type': 'application/json'
        }
    });
}

function send_activity( act ){
	var msg = { activity : act }
	fetch('https://demo.thingsboard.io/api/v1/xQGhgoE4a5LdplwyVXlT/telemetry', {
        method: "POST",
        mode: 'no-cors',
        body: JSON.stringify(msg),
        headers: {
            'Content-type': 'application/json'
        }
    });
}

