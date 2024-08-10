const express = require('express');
const { uploadResume } = require('../controllers/resumeProcessing');
const authenticateToken = require('../middleware/authMiddleware');


const router = express.Router();

router.post('/upload', uploadResume);

module.exports = router;
