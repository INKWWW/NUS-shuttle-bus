'use strict'

var http = require('http'); //加载http模块
var fs = require('fs');
//创建
var server = http.createServer(function (req, res) {
    //res.writeHead(200, {'Context-Type': 'text/plain'});
    fs.readFile('index.html', function(err, data){
        if (err) {
            res.write('DON\'T WORK');                
        }
        else{
            res.write(data);
        }
        res.end();
    });
    //res.end('!!!This is my local server test!!!\n');
});

server.listen(3000, '127.0.0.1'); //监听port

console.log('server running at http://127.0.0.1:3000/');
