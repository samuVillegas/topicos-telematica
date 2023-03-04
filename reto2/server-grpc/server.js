const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const PROTO_PATH = __dirname + '/files.proto';
const packageDefinition = protoLoader.loadSync(PROTO_PATH);
const files = grpc.loadPackageDefinition(packageDefinition).files;
const { execSync } = require('child_process');
require('dotenv').config()


//Function to list files
function listFiles(call, callback) {
  const result = execSync('cd ../files && ls');
  const response = { message: result };
  callback(null, response);
}

//Function to list files by file name
function getFile(call, callback) {
  const result = execSync(`find ../files -name "*${call.request.fileName}*"`);
  const response = { message: result };
  callback(null, response);
}

//Main function
function main() {
  const server = new grpc.Server();
  server.addService(files.Files.service, { listFiles: listFiles, getFile: getFile });
  server.bindAsync(`localhost:${process.env.PORT}`, grpc.ServerCredentials.createInsecure(), () => {
    console.log(`Server running at http://localhost:${process.env.PORT}`);
    server.start();
  });
}

main();
