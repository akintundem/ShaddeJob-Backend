const { sendToQueue, receiveFromQueue } = require('../../config/rabbitMQ');

async function uploadResume(req, res) {
    try {
        console.log("beginning the resume upload.")
        const filePath = "Hello World";
        sendToQueue('send_resume_to_process_container', filePath);
        await receiveFromQueue('recv_resume_processed_from_container', (processMessage) => {
            res.json({ message: 'Resume uploaded and processing started' });
        });
    } catch (error) {
        res.status(500).json({ error: 'Failed to process resume' });
    }
}

module.exports = {
    uploadResume
};
