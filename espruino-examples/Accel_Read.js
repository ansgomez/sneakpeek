//Turn on accelerometer with 1.6 Hz
Puck.accelOn(1.6);

//Print accelerometer values every two seconds
setInterval(function () { 
  var m = Puck.accel();
  console.log("X: " + m.acc.x + " Y: " + m.acc.y + " Z: " + m.acc.z);
}, 2000);