const jwt = require('jsonwebtoken');
const { getRedis } = require('..//../config/redisClient');

const JWT_SECRET = process.env.JWT_SECRET;

const authMiddleware = async (req, res, next) => {
    const token = req.cookies.token;

    if (!token) {
        return res.status(401).json({ message: 'Authentication failed' });
    }

    try {
        const data = await getRedis(token);

        if (data === 'blacklisted') {
            return res.status(401).json({ message: 'Token is blacklisted' });
        }

        const decoded = jwt.verify(token, JWT_SECRET);
        req.user = decoded; 
        next();
    } catch (error) {
        res.status(401).json({ message: 'Authentication failed', error });
    }
};

module.exports = authMiddleware;
