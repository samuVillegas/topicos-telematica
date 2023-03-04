const client = require('./grpc_config');


// Function to list files
function listFiles() {
    return new Promise((resolve, reject) => {
        client.listFiles({}, function (error, response) {
            if (error) {
                reject(error);
            } else {
                resolve(response);
            }
        });
    });
}
// Function to get file by file name
function getFile(fileName) {
    return new Promise((resolve, reject) => {
        client.getFile({ fileName: fileName }, function (error, response) {
            if (error) {
                reject(error);
            } else {
                resolve(response);
            }
        });
    });
}

module.exports = {
    listFiles,
    getFile
}