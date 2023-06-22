digitalWrite(D1,0);
pinMode(D29,"input_pullup");
var d = [];
setWatch(function(e) {
  d.push(1000*(e.time-e.lastTime));
}, D29, {edge:"both",repeat:true});

var lastLen = 0;
setInterval(function() {
  if (d.length && d.length==lastLen) {
    d.shift(); // remove first element
    console.log(d.map(a=>a.toFixed(1)).toString());
    d=[];
  }
  lastLen = d.length;
},200);
