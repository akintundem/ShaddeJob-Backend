const amqp = require('amqplib');

const RABBITMQ_URL = 'amqp://rabbitmq:5672';

let connections = {};
let channels = {};

const getConnection = async () => {
    if (!connections.default) {
        connections.default = await amqp.connect(RABBITMQ_URL);
    }
    return connections.default;
};

const getChannel = async (queue) => {
    if (!channels[queue]) {
        const conn = await getConnection();
        channels[queue] = await conn.createChannel();
        await channels[queue].assertQueue(queue, { durable: true });
    }
    return channels[queue];
};

const sendToQueue = async (queue, message) => {
    try {
        const channel = await getChannel(queue);
        channel.sendToQueue(queue, Buffer.from(message), { persistent: true });
    } catch (err) {
        console.error(err);
    }
};

const receiveFromQueue = async (queue, callback) => {
    try {
        const channel = await getChannel(queue);
        channel.consume(queue, (msg) => {
            if (msg !== null) {
                const message = msg.content.toString();
                callback(message);
                channel.ack(msg);
            }
        });
    } catch (err) {
        console.error(err);
    }
};

module.exports = {
    sendToQueue,
    receiveFromQueue
};
