'use strict';

const config = {}

const env = process.env.NODE_ENV || "development"
const isProduction = env === "production"

config.port = 4501

module.exports = config
