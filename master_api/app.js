require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const cors = require('cors'); 

// Import routes
const authRoutes = require('./presentation/routes/authRoutes');
const resumeRoutes = require('./presentation/routes/resumeRoutes')
// const coverLetterRoutes = require('./presentation/routes/coverLetterRoutes'); 
// const jobRoutes = require('./presentation/routes/jobRoutes'); 
const interviewRoutes = require('./presentation/routes/interviewRoutes'); 

// Start Web Server.
const app = express();

// Middleware setup
app.use(cors()); 
app.use(cookieParser()); 
app.use(bodyParser.json());

// Authorization: Login, Signup and Log out related routes. 
app.use(authRoutes);

// Resume Upload and Summary: This routes will deal with recieveing Resumes from Client and Processing. 
app.use(resumeRoutes);

// Cover Letter Generation: This routes will deal with recieveing Resumes from Client and Processing. 
// app.use(coverLetterRoutes);

// Job Posting Management.
// app.use(jobRoutes);

// Interview Preparation. 
app.use(interviewRoutes);

const PORT = 5100;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
