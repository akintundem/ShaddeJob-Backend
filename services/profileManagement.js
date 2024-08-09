const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const path = require('path');
const fs = require('fs');
const User = require('../models/User');
const {setRedis,getRedis} = require('../config/redisClient');
const mongoose = require('../config/mongoose'); 


const JWT_SECRET = process.env.JWT_SECRET; // Ensure this environment variable is set

const processProfilePicture = async (profilePicture) => {
    return new Promise((resolve, reject) => {
        const uploadDir = path.join(__dirname, '../uploads');

        if (!fs.existsSync(uploadDir)) {
            fs.mkdirSync(uploadDir, { recursive: true });
        }

        const fileName = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}.png`;
        const filePath = path.join(uploadDir, fileName);

        let imageData;
        if (profilePicture.startsWith('data:image')) {
            const base64Data = profilePicture.split(',')[1];
            imageData = Buffer.from(base64Data, 'base64');
        } else {
            imageData = profilePicture;
        }

        fs.writeFile(filePath, imageData, (err) => {
            if (err) {
                return reject(err);
            }
            resolve(filePath);
        });
    });
};

const signUpUser = async (email, password) => {
    try {
        const saltRounds = parseInt(process.env.BCRYPT_SALT, 10);
        const hashedPassword = await bcrypt.hash(password, saltRounds);

        const redisKey = `signup:${email}`;
        const redisValue = JSON.stringify({
            email,
            password: hashedPassword
        });

        await setRedis(redisKey, redisValue, 300);
        return 1; // Successful.
    } catch (err) {
        console.error('Error signing up user:', err);
        return 0; // Failure.
    }
};


const processUserRegistration = async ({ email, firstName, lastName, dob, phone, address, profilePicture, bio }) => {
    try {
        // const processedProfilePicture = await processProfilePicture(profilePicture);
        const processedProfilePicture = '/none'
        const tempKey = `signup:${email}`;

        const result = await getRedis(tempKey);
        if (!result) {
            console.log('No user data found in Redis.');
            return 0; // Failure.
        }

        const userData = JSON.parse(result);
        userData.email = 'kik@k.com'
        userData.firstName = firstName;
        userData.lastName = lastName;
        userData.dob = dob;
        userData.phone = phone;
        userData.address = address;
        userData.profilePicture = processedProfilePicture;
        userData.bio = bio;

        const user = new User(userData);
        await user.save();
        return 1; // Successful.
    } catch (err) {
        console.error('Error processing user registration:', err);
        return 0; // Failure.
    }
};


const loginUser = async (email, password) => {
    const user = await User.findOne({ email });

    if (!user) {
        throw new Error('User not found');
    }

    const isMatch = await bcrypt.compare(password, user.password);

    if (!isMatch) {
        throw new Error('Invalid credentials');
    }

    const token = jwt.sign(
        { email: user.email }, 
        JWT_SECRET, 
        { expiresIn: '1h' } 
    );
    return token;
};

const logoutUser = async (token) => {
    const decoded = jwt.verify(token, JWT_SECRET);
    const expiration = decoded.exp;

    await setRedis(token, 'blacklisted', expiration);
};
module.exports = {
    signUpUser,
    processUserRegistration,
    loginUser,
    logoutUser
};
