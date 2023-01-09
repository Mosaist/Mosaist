const http = require('http');
const fs = require('fs');

http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type':'text/html'});
    html = fs.readFileSync('./index.html');
    res.end(html);
}).listen(80, '0.0.0.0');