var express = require("express");
 
var app = express();
 
app.use(express.static('build'));
 
//app.use('/', express.static(__dirname + '/public/css'));
//app.use('/js', express.static(__dirname + '/public/js'));
//app.use('/images', express.static(__dirname + '/public/images'));
 
var server = app.listen(8081, function(){
    var port = server.address().port;
    console.log("Server started at http://localhost:%s", port);
});