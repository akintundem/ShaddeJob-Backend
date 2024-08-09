const { setRedis, getRedis, redisClient } = require('./config/redisClient');

console.log("hello");

(async () => {
    try {
        // Set a key-value pair in Redis
        await setRedis('testKey', 'testValue');
        console.log('Value set successfully.');

        // Get the value from Redis
        const value = await getRedis('testKey');
        console.log(`Retrieved value for 'testKey': ${value}`);

        // Test for a non-existing key
        const nonExistingValue = await getRedis('nonExistingKey');
        console.log(`Retrieved value for 'nonExistingKey': ${nonExistingValue}`);

        // Clean up
        await redisClient.del('testKey');
        console.log('Key deleted successfully.');
    } catch (err) {
        console.error('Error during Redis operations:', err);
    } finally {
        // Ensure Redis connection is closed properly after all operations
        redisClient.quit().catch(err => console.error('Error closing Redis client:', err));
    }
})();