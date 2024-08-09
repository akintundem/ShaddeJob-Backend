// middleware/authMiddleware.js
const jwt = require('jsonwebtoken');
const redis = require('redis');

const JWT_SECRET = process.env.JWT_SECRET;

const redisClient = redis.createClient({
    host: 'localhost', 
    port: 6379
});

const authMiddleware = (req, res, next) => {
    const token = req.cookies.token;

    if (!token) {
        return res.status(401).json({ message: 'Authentication failed' });
    }

    redisClient.get(token, (err, data) => {
        if (err) {
            return res.status(500).json({ message: 'Internal server error' });
        }

        if (data === 'blacklisted') {
            return res.status(401).json({ message: 'Token is blacklisted' });
        }

        try {
            const decoded = jwt.verify(token, JWT_SECRET);
            req = decoded;
            next();
        } catch (error) {
            res.status(401).json({ message: 'Authentication failed', error });
        }
    });
};

module.exports = authMiddleware;
