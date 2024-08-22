const {getChatsByUserId, getMessagesByChatId, deleteChatByChatId, markMessageAsReadById, startChatService, continueChatService} = require('../../services/conversationService');

const startChat = async (req, res) => {
    try {
        const user_id = getUser(); 
        const response_message = await startChatService(user_id);
        res.json({ message: response_message });
    } catch (error) {
        res.status(500).json({ error: 'Failed to start chat' });
    }
};

const continueChat = async (req, res) => {
    try {
        const body = req.body
        const user_id = getUser(); 
        const chat_id = getChatID(); 
        const response_message = await continueChatService(user_id, chat_id, body.userMessage);
        res.json({ message: response_message });
    } catch (error) {
        res.status(500).json({ error: 'Failed to continue chat' });
    }
};

const getLastChatsByUser = async (req, res) => {
    try {
        const user_id = req.params.user_id; 

        const chats = await getChatsByUserId(user_id);

        res.json({ chats });
    } catch (error) {
        res.status(500).json({ error: 'Failed to retrieve user chats' });
    }
};

const getLast10MessagesByChatId = async (req, res) => {
    try {
        const chat_id = req.params.chat_id;

        const messages = await getMessagesByChatId(chat_id);

        res.json({ messages });
    } catch (error) {
        res.status(500).json({ error: 'Failed to retrieve chat messages' });
    }
};


const deleteChat = async (req, res) => {
    try {
        const chat_id = req.params.chat_id;

        await deleteChatByChatId(chat_id);

        res.json({ message: 'Chat deleted successfully' });
    } catch (error) {
        res.status(500).json({ error: 'Failed to delete chat' });
    }
};

const markMessageAsRead = async (req, res) => {
    try {
        const messageId = req.params.messageId;

        await markMessageAsReadById(messageId);

        res.json({ message: 'Message marked as read' });
    } catch (error) {
        res.status(500).json({ error: 'Failed to mark message as read' });
    }
};

module.exports = {
    startChat,
    continueChat,
    getLastChatsByUser,
    getLast10MessagesByChatId,
    deleteChat,
    markMessageAsRead
};


