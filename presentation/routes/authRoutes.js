const express = require('express');
const { signup, register, login, logout } = require('../controllers/authController');

const router = express.Router();

router.post('/signup', signup);
router.post('/register', register);
router.post('/login', login);
router.post('/logout', logout);


module.exports = router;
