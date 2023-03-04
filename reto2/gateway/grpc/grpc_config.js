//Config grpc client
const grpc = require('@grpc/grpc-js');
require('dotenv').config()
const protoLoader = require('@grpc/proto-loader');
const PROTO_PATH = __dirname + '/files.proto';
const packageDefinition = protoLoader.loadSync(PROTO_PATH);
const files = grpc.loadPackageDefinition(packageDefinition).files;
const client = new files.Files(`localhost:${process.env.PORT_SERVER_GRPC}`, grpc.credentials.createInsecure());

module.exports = client;