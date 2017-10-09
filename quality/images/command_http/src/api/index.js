var express = require('express');
var router = express.Router();
var debug = require('debug')('restrek:index');


router.get('/', function(req, res) {
  res.status(200).json({foo:'bar'})
})


router.get('/status200', function(req, res) {
  res.status(200).json({})
})

router.get('/get_body', function(req, res) {
  res.json({foo: 'bar'})
})


router.get('/get_headers', function(req, res) {
  res.set({
    'X-Custom-header-1': 'thisiscustomheader1',
    'X-Custom-header-2': 'thisiscustomheader2',
    'X-Custom-header-3': 'thisiscustomheader3'
  })
  res.json({})
})


router.post('/test_http_post', function(req, res) {
  res.json(req.body)
})


router.get('/entity/:id', function(req, res) {
  var id = req.params.id
  res.json({
    id: id,
    name: 'Entity Name'
  })
})

module.exports = router