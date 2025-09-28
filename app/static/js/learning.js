// static/js/learning.js

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const contentArea = document.getElementById('content-area');
    const stepDataContainer = document.getElementById('step-data-container');
    const stepData = JSON.parse(stepDataContainer.dataset.step);

    const codeEditorContainer = document.getElementById('code-editor-container');
    const codeEditor = document.getElementById('code-editor');
    const codeOutput = document.getElementById('code-output');
    const runCodeBtn = document.getElementById('run-code-btn');
    
    const typingIndicator = document.getElementById('typing-indicator');


    // Auto-scroll chatbox ke bawah jika ada
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function addMessage(sender, message) {
        const p = document.createElement('p');
        p.innerHTML = `<strong>${sender}:</strong> ${message.replace(/\n/g, '<br>')}`;
        chatBox.appendChild(p);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Fungsi global untuk tombol 'Lanjut' yang dibuat oleh server
    window.handleNextStep = async (next_url = null) => {
        if (next_url) {
            window.location.href = next_url;
        } else {
            await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'next_step' })
            });
            window.location.reload(); // Selalu reload untuk memuat state baru
        }
    };
    
    function showNextStepButton(next_url = null) {
        const oldButton = document.getElementById('next-step-btn');
        if (oldButton) oldButton.remove();
        
        const nextButton = document.createElement('button');
        nextButton.id = 'next-step-btn';
        nextButton.textContent = next_url ? 'Mulai Quiz' : 'Lanjut';
        
        // Panggil fungsi global saat diklik
        nextButton.onclick = () => window.handleNextStep(next_url);
        
        contentArea.appendChild(nextButton);
    }

    if (runCodeBtn) {
        runCodeBtn.addEventListener('click', async () => {
            const modifiedCode = document.getElementById('code-editor').value;
            codeOutput.textContent = 'Menjalankan...';
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: modifiedCode, action: 'run_code' })
            });
            const data = await response.json();
            codeOutput.textContent = data.reply;
        });
    }

    if (chatForm) {
        userInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                chatForm.dispatchEvent(new Event('submit', { cancelable: true }));
            }
        });

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = userInput.value.trim();
            if (!message) return;
            
            addMessage('Anda', message);
            userInput.value = '';

            // ===== 2. TAMPILKAN INDIKATOR SEBELUM FETCH =====
            typingIndicator.style.display = 'flex';
            chatBox.scrollTop = chatBox.scrollHeight; // Scroll lagi agar indikator terlihat

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message, action: 'chat' })
                });

                // ===== 3. SEMBUNYIKAN INDIKATOR SETELAH DAPAT RESPON =====
                typingIndicator.style.display = 'none';
                
                const data = await response.json();
                addMessage('SocraMind', data.reply);
                
                if (data.show_next_button) {
                    userInput.disabled = true;
                    showNextStepButton(data.next_action_url);
                }
            } catch (error) {
                // ===== 4. SEMBUNYIKAN JUGA JIKA TERJADI ERROR =====
                typingIndicator.style.display = 'none';
                console.error("Error saat fetch:", error);
                addMessage('Error', 'Gagal terhubung ke server.');
            }
        });
    }

    // Cek apakah tombol lanjut perlu dibuat saat refresh
    const showNextButtonOnLoad = document.documentElement.getAttribute('data-show-next-button') === 'True';
    if (showNextButtonOnLoad) {
        showNextStepButton();
        if(userInput) userInput.disabled = true;
    }
});