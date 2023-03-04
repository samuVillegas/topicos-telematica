const { getConnection } = require('./mom_config');
const { uid } = require('uid');
const QUEUE_REQUEST = 'queue-request';
const QUEUE_RESPONSE = 'queue-response';

// Allows us to consume only the response of the message we sent.
function consumeOnce(channel, queue, options) {
    return new Promise((resolve) => {
        const consumerTag = options?.consumerTag || uid();

        const onMessage = (msg) => {
            if (msg.properties.correlationId === options.correlationId) {
                channel.removeListener('error', onError);
                channel.cancel(consumerTag);
                resolve(msg);
            }
        };

        const onError = (err) => {
            channel.removeListener('message', onMessage);
            reject(err);
        };

        channel.consume(queue, onMessage, { consumerTag: consumerTag }).catch(onError);
        channel.once('error', onError);
    });
}

//Method to list files
const listFiles = async () => {
    //Connect with MOM (RabbitMQ)
    const { channel } = await getConnection();

    //Send a request and wait for a response
    const correlationId = uid();
    const payload = 'listFiles.';

    //Send to request queue
    await channel.sendToQueue(QUEUE_REQUEST, Buffer.from(payload), {
        correlationId: correlationId,
        replyTo: QUEUE_RESPONSE,
    });

    //Get response from server
    const response = await consumeOnce(channel, QUEUE_RESPONSE, {
        correlationId: correlationId,
    });

    return response.content.toString();
}

//Method to obtain the files
const getFile = async (filter) => {
    //Connect with MOM (RabbitMQ)
    const { channel } = await getConnection();

    //Send a request and wait for a response
    const correlationId = uid();
    const payload = `getFile.${filter}`;

    //Send to request queue
    await channel.sendToQueue(QUEUE_REQUEST, Buffer.from(payload), {
        correlationId: correlationId,
        replyTo: QUEUE_RESPONSE,
    });

    //Get response from server
    const response = await consumeOnce(channel, QUEUE_RESPONSE, {
        correlationId: correlationId,
    });
    return response.content.toString()
}

module.exports = { listFiles, getFile }