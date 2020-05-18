//inizialize the sensor
let sensor = new  LinearAccelerationSensor({frequency: 1});

function getdata(){
	var l=[];
	var d =0;
	var activity="";
	//activate the sensor
	sensor.start();
	//start the reading
	sensor.onreading = () => {
		//read the value from each axis
		l[0]= sensor.x.toFixed(2) ;
		l[1]= sensor.y.toFixed(2) ;
		l[2]= sensor.z.toFixed(2) ;
		//display the values
		document.getElementById('status').innerHTML = "x:" + l[0] +" y:" + l[1] + " z:" + l[2];
		//check if the send_data has been activated
		if(document.getElementById('send_d').innerHTML == "Sending data"){
			//trigger send function
			send_data(l[0], l[1], l[2]);
		}
		
		//calculate final linear acceleration
		d=Math.sqrt(l[0]*l[0] + l[1]*l[1] + l[2]*l[2] ).toFixed(2);
		//display the activity recognized
		if ( d > 3){
			activity="running";
			document.getElementById('status_act').innerHTML = activity;
		}else if (d > 0.6){
			activity="walking";
			document.getElementById('status_act').innerHTML = activity;
		}else{
			activity="standing";
			document.getElementById('status_act').innerHTML = activity;
		}
		
		//check if the send_aactivity has been activated
		if(document.getElementById('send_a').innerHTML == "Sending activity"){
			//trigger send function
			send_activity(activity);
		}
	};
	sensor.onerror = event => {
		document.getElementById('status').innerHTML = "Error Name" + event.error.name + "Error Message " + event.error.message;
	};

}

function stop(){
	//deactivate the sensor
	sensor.stop()
	document.getElementById('status').innerHTML = "No data from sensor";
	document.getElementById('status_act').innerHTML = "No activity detect";
}
