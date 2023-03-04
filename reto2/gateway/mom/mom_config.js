const amqp = require('amqplib');
require('dotenv').config();

let connection = null;
let channel = null;

async function getConnection() {
  if (!connection) {
    connection = await amqp.connect(`amqp://localhost:${process.env.PORT_SERVER_MOM}`);
    channel = await connection.createChannel();
  }
  return { connection, channel };
}

module.exports = { getConnection };