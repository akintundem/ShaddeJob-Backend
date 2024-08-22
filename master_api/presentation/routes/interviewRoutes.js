const express = require('express');
const { startChat,continueChat,getLastChatsByUser,getLast10MessagesByChatId,deleteChat,markMessageAsRead} = require('../controllers/ChatBot');

const router = express.Router();

router.get('/start', startChat)
router.get('/chat/:chat_id', continueChat);
router.get('/chats/user/:user_id', getLastChatsByUser);
router.get('/chats/:chat_id/messages', getLast10MessagesByChatId);
//route.get(another 10 chats after swiping down.)
router.delete('/chats/:chat_id', deleteChat);
router.patch('/messages/:messageId/read', markMessageAsRead);
module.exports = router;
