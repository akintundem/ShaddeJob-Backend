require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const cors = require('cors'); 
const authRoutes = require('./presentation/routes/authRoutes');
const authenticateToken = require('./presentation/middleware/auth');

// Start Web Server.
const app = express();


// Middleware setup
app.use(cors()); 
app.use(cookieParser()); 
app.use(bodyParser.json());

// Routes setup
app.use(authRoutes);

// Protected route
app.get('/dashboard', authenticateToken, (req, res) => {
    res.json({ message: `Hello ${req.user.username}, you have access to this protected route` });
});

// Server setup
const PORT = 5100;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
