const mongoose = require('mongoose');

const messageSchema = new mongoose.Schema({
    sender_id: {
        type: String,
        required: true
    },
    message: {
        type: String,
        required: true
    },
    timestamp: {
        type: Date,
        default: Date.now
    },
    read: {
        type: Boolean,
        default: false
    }
});

const conversationSchema = new mongoose.Schema({
    chat_id: {
        type: String,
        required: true,
        index: true 
    },
    user_id: {
        type: String,
        required: true
    },
    messages: [messageSchema], 
    createdAt: {
        type: Date,
        default: Date.now
    },
    updatedAt: {
        type: Date,
        default: Date.now
    }
});

// Middleware to update the `updatedAt` field on every save
conversationSchema.pre('save', function(next) {
    this.updatedAt = Date.now();
    next();
});

const Conversation = mongoose.model('Conversation', conversationSchema);

module.exports = Conversation;
