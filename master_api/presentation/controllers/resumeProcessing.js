const { v4: uuidv4 } = require('uuid');

const { sendToQueue, receiveFromQueue } = require('../../config/rabbitMQ');

async function uploadResume(req, res) {
    try {
        console.log("beginning the resume upload.")
        const messageId = uuidv4();
        const filePath = "Mayokun_Resume.pdf";
        const message = {
            filePath: filePath,
            messageId: messageId
        };
        
        sendToQueue('send_resume_to_process_container', message);
        await receiveFromQueue(messageId, (processMessage) => {
            // we will be taking the response that correlates with the correlationID
           console.log("Recieved")
            res.json({ message: processMessage });
        });
    } catch (error) {
        res.status(500).json({ error: 'Failed to process resume' });
    }
}

module.exports = {
    uploadResume
};
