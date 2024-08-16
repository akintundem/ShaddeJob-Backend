const express = require('express');
const questionGenerator = require('../controllers/questionGenerator');

const router = express.Router();

router.get('/question', questionGenerator)


module.exports = router;
