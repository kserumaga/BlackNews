document.addEventListener('DOMContentLoaded', () => {
    // Toggle AI Chat
    document.querySelector('.assistant-toggle').addEventListener('click', () => {
        document.querySelector('.chat-interface').classList.toggle('hidden');
    });

    // Article Question Handler
    document.querySelectorAll('.ask-ai').forEach(button => {
        button.addEventListener('click', async (e) => {
            const articleId = e.target.dataset.articleId;
            const response = await fetch(`/ai/question/${articleId}`);
            const data = await response.json();
            // Handle AI response
        });
    });
});
