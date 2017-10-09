var express = require('express')
var app = express();
var bodyParser = require('body-parser')
var cookieParser = require('cookie-parser')
var session = require('express-session')
var debug = require('debug')('rest-api:app')
var config = require('./config')


app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))
var cookieSecret = 'fdr44gd4hjf'
app.use(cookieParser(cookieSecret))

app.use(function(req, res, next) {
  res.removeHeader("x-powered-by")
  next()
})

const sessionOpt = {
  name: "wsid",
  proxy: true,
  resave: true,
  ttl: 36000,
  saveUninitialized: true,
  secret: cookieSecret
}

app.use(session(sessionOpt))

app.use('*', function(req, res, next) {
  var sess = req.session
  debug('SESSION', sess)
  next()
})

app.use('/cookies', require(__dirname + '/api/cookies'))
app.use('/', require(__dirname + '/api/index'))

app.use(function(req, res, next) {
  var err = new Error('Not Found')
  err.status = 404
  next(err)
})

app.use(function(err, req, res, next) {
    res.status(500).send(err.message)
})

var serve = app.listen(config.port, function() {
  var host = serve.address().address
  var port = serve.address().port

  debug('Listening at http://%s:%s', host, port)
})