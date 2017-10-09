var express = require('express')
var router = express.Router()
var debug = require('debug')('restrek:cookies')


router.get('/get_cookies', function(req, res) {
  res.cookie('cookie1', 'thisisthecookie1', { httpOnly: true })
  res.cookie('cookie2', 'thisisthecookie2', { httpOnly: true })
  res.status(200).json({})
})

module.exports = router