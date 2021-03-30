var express = require('express');
const axios = require('axios').default;
var proxy = require('express-http-proxy');


var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

var app = express();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);

app.use('/API', proxy('https://fadapi.azurewebsites.net'));

app.get('/border', function(req, res) {
  axios.get('https://fadapi.azurewebsites.net/StLuciaBorder')
  .then(function (response) {
    // handle success
    console.log('data:', response.data); // Print the data received
    res.send(response.data); //Display the response on the website
    console.log(response);
  })
  .catch(function (error) {
    // handle error
    console.log(error);
  })
  .then(function () {
    // always executed
    console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
  });
});

module.exports = app;
