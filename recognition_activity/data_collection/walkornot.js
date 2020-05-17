let sensor = new  LinearAccelerationSensor({frequency: 1});

function getdata(){
	var prec=0;
	var act=0;
	var l=[];
	var d =0;
	var activity="";
	sensor.start();
	sensor.onreading = () => {
		l[0]= sensor.x.toFixed(2) ;
		l[1]= sensor.y.toFixed(2) ;
		l[2]= sensor.z.toFixed(2) ;
		document.getElementById('status').innerHTML = "x:" + l[0] +" y:" + l[1] + " z:" + l[2];
		
		if(document.getElementById('send_d').innerHTML == "Sending data"){
			send_data(l[0], l[1], l[2]);
		}
		
		d=Math.sqrt(l[0]*l[0] + l[1]*l[1] + l[2]*l[2] ).toFixed(2);
		if ( d > 2){
			activity="running";
			document.getElementById('status_act').innerHTML = activity;
		}else if (d > 0.6){
			activity="walking";
			document.getElementById('status_act').innerHTML = activity;
		}else{
			activity="stanning";
			document.getElementById('status_act').innerHTML = activity;
		}
		
		if(document.getElementById('send_a').innerHTML == "Sending activity"){
			send_activity(activity);
		}
		
		prec = act;
	};
	sensor.onerror = event => {
		document.getElementById('status').innerHTML = "Error Name" + event.error.name + "Error Message " + event.error.message;
	};

}

function stop(){
	sensor.stop()
	document.getElementById('status').innerHTML = "No data from sensor";
	document.getElementById('status_act').innerHTML = "No activity detect";
}
