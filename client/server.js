// MODULES =================================================
var express = require('express');

var server = express();
server.use(express.static(__dirname));

var port = process.env.PORT || 9000;
server.listen(port);

// expose server
exports = module.exports = server;