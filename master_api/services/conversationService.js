const Conversation = require('../models/Conversation');
const { v4: uuidv4 } = require('uuid');
const { sendToQueue, receiveFromQueue } = require('../../config/rabbitMQ');

const startChatService = async (user_id) => {
    const messageId = uuidv4();
    const action = "StartChat";
    const message = {
        action: action,
        messageId: messageId,
        user_id: user_id
    };

    sendToQueue('Interview_Chat', message);

    const processMessage = await receiveFromQueue(messageId);

    let response_message = {
        action: "Stop",
        chat_id: ""
    };

    if (processMessage.action === "Chat_Started") {
        response_message.chat_id = processMessage.chat_id;
    }

    return response_message;
};

const continueChatService = async (user_id, chat_id, userMessage) => {
    await saveUserMessage(user_id, chat_id, userMessage);
    const messageId = uuidv4();
    const action = "ContinueChat";
    const message = {
        action: action,
        messageId: messageId,
        user_id: user_id,
        chat_id: chat_id
    };

    sendToQueue('Interview_Chat', message);

    const processMessage = await receiveFromQueue(messageId);

    let response_message = {
        action: "Stop",
        chat_id: "",
        bot_response: ""
    };

    if (processMessage.action === "Chat_Started") {
        response_message.chat_id = processMessage.chat_id;
        response_message.bot_response = await pullLastMessage(); 
    }

    return response_message;
};

const saveUserMessage = async (user_id, chat_id, userMessage) => {
    try {
        let conversation = await Conversation.findOne({ chat_id, user_id });

        if (!conversation) {
            conversation = new Conversation({
                chat_id,
                user_id,
                messages: []
            });
        }

        conversation.messages.push({
            sender_id: user_id,
            message: userMessage,
            sender: 'user'
        });

        await conversation.save();
    } catch (error) {
        console.error('Error saving user message:', error);
        throw error;
    }
};

const pullLastMessage = async (chat_id) => {
    try {
        const lastMessage = await Conversation.findOne(
            { chat_id, 'messages.sender': 'bot' },
            { 'messages.$': 1 } 
        ).sort({ 'messages.timestamp': -1 });

        return lastMessage && lastMessage.messages[0] ? lastMessage.messages[0].message : "";
    } catch (error) {
        console.error('Error retrieving last message:', error);
        throw error;
    }
};

const getChatsByUserId = async (user_id) => {
    return await Conversation.find({ user_id })
        .sort({ timestamp: -1 })
        .distinct('chat_id')
        .limit(10);
};

const getMessagesByChatId = async (chat_id) => {
    return await Conversation.find({ chat_id })
        .sort({ timestamp: -1 })
        .limit(10);
};

const deleteChatByChatId = async (chat_id) => {
    return await Conversation.deleteMany({ chat_id });
};

const markMessageAsReadById = async (messageId) => {
    return await Conversation.findByIdAndUpdate(messageId, { read: true });
};

module.exports = {
    getChatsByUserId,
    getMessagesByChatId,
    deleteChatByChatId,
    markMessageAsReadById,
    startChatService,
    continueChatService
};
