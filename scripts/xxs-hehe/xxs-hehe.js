var page = require('webpage').create();
var system = require('system');
var args = system.args;

if (args.length < 3) {
  console.log('Usage: phantomjs xxs-hehe.js <url> <hmac-to-be-stolen>');
} else {
  var url = args[1];
  var hmac = args[2]
}

phantom.addCookie({
  'name'     : 'userid',
  'value'    : hmac,
  'domain'   : 'localhost',
  'path'     : '/',                /* required property */
  'httponly' : true,
  'secure'   : true,
  'expires'  : (new Date()).getTime() + (1000 * 60 * 60)   /* <-- expires in 1 hour */
});



page.open(url, function (status) {
    if (status !== 'success') {
        console.log('Unable to load the address!');
        phantom.exit();
    } else {
        window.setTimeout(function () {
            console.log('Page loaded ok!');
            // page.render('test.png');
            phantom.exit();
        }, 1000); // Change timeout as required to allow sufficient time
    }
});
