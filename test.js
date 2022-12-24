const http = require('http')
const request = require('request');
const url = require('url')

http.createServer((req, res) => {
    params = url.parse(req.url, true).query;

    if (!params.image) {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end('false');
    }

    let options = {
        uri: 'http://127.0.0.1/mosaic',
        qs: {
            image: params.image
        }
    };

    request.get(options, function (error, response, body) {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(body);
    });
}).listen(8080)
