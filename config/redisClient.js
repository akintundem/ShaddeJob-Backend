const redis = require('redis');

const redisClient = redis.createClient({
    url: 'redis://localhost:6379' 
});

redisClient.connect().catch(console.error);

redisClient.on('connect', () => {
    console.log('Connected to Redis');
});

redisClient.on('error', (err) => {
    console.log('Redis error:', err);
});

const setRedis = async (tempKey, data, expiration) => {
    try {
        await redisClient.set(tempKey, data, 'EX', expiration);
    } catch (err) {
        console.error('Redis set error:', err);
        throw err;
    }
};

const getRedis = async (tempKey) => {
    try {
        const result = await redisClient.get(tempKey);
        return result;
    } catch (err) {
        console.error('Redis get error:', err);
        throw err;
    }
};

module.exports = { redisClient, setRedis, getRedis };
