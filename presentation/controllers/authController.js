require('dotenv').config();
const {signUpUser,processUserRegistration,loginUser,logoutUser} = require('../../services/profileManagement')

const signup = async (req, res) => {
    const { email, password } = req.body;
    try{
        if(await signUpUser(email, password) === 1){
            res.status(201).json({
                redirectUrl: '/register',
                email: email
            })
        } else {
            res.status(400).json({
                redirectUrl: '/signup'
            });
        }
    }catch{
        res.status(400).json({
            redirectUrl: '/signup'
        });

    }
};

const register =  async (req, res) => {
    const { email, firstName, lastName, dob, phone, address, profilePicture, bio } = req.body;

    try {
        const response = await processUserRegistration({ email, firstName, lastName, dob, phone, address, profilePicture, bio });
        if( response === 1){
            res.status(201).json({
                redirectUrl: '/dashboard' 
            });
        }else{
            res.status(400).json({
                redirectUrl: '/register'  
            });
        }
    } catch (error) {
        res.status(400).json({redirectUrl: '/register'  });
    }
};

const login = async (req, res) => {
    const { email, password } = req.body;

    try {
        const token = await loginUser(email, password);
        res.cookie('token',
             token,
              { httpOnly: true, secure: true, sameSite: 'Strict'}
        );
        res.status(200).json({ 
            redirectUrl: '/dashboard'
            });
    } catch (error) {
        res.status(400).json({redirectUrl: '/login'});
    }
};

const logout = async (req, res) => {
    const token = req.cookies.token;
    try {
        await logoutUser(token);
        res.clearCookie('token', { httpOnly: true, secure: true, sameSite: 'Strict' });
        res.status(200).json({redirectUrl: '/'});
    } catch (error) {
        res.status(400).json({redirectUrl: '/'});
    }
};

module.exports = { signup, register, login, logout};
