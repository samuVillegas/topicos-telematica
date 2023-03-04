const express = require("express");
const { execSync } = require('child_process');
const amqp = require("amqplib");
require('dotenv').config()
const app = express();

let channel, connection;

const QUEUE_REQUEST = 'queue-request';
const QUEUE_RESPONSE = 'queue-response';

//Middlewares
app.use(express.json());

connectQueue() //Call the function to connect with RabbitMQ

//Function that listens for messages in the queue-request queue
async function connectQueue() {
    try {

        //Create connection with MOM (RabbitMQ) server
        connection = await amqp.connect(`amqp://localhost:${process.env.PORT_SERVER_MOM}`);
        channel = await connection.createChannel();

        // We connect to 'queue-request' and if it does not exist we create it.
        await channel.assertQueue(QUEUE_REQUEST);
        // We connect with 'queue-response' and if it does not exist we create it.
        await channel.assertQueue(QUEUE_RESPONSE);

        //We consume the request queue
        await channel.consume(
            QUEUE_REQUEST,
            async (msg) => {

                const payload = msg.content.toString();
                let response = '';
                const values = payload.split('.');
                const [fun] = values;

                if (fun === 'listFiles') {
                    response = execSync('cd ../files && ls');
                } else if (fun === 'getFile') {
                    response = execSync(`find ../files -name "*${values.slice(1).join('.')}*"`);
                }

                channel.sendToQueue(msg.properties.replyTo, Buffer.from(response), {
                    correlationId: msg.properties.correlationId,
                });

                channel.ack(msg);
            },
            { noAck: false }
        );
    } catch (error) {
        console.log(error)
    }
}

app.listen(process.env.PORT, () => console.log("Server running at port " + process.env.PORT));