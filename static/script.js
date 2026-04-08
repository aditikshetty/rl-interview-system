const API_URL = "";

async function startInterview() {
    try {
        const response = await fetch(`${API_URL}/reset`, { method: "POST" });
        const data = await response.json();
        
        updateUI(data.state);
        document.getElementById("reward-val").innerText = "0.00";
        document.getElementById("status-val").innerText = "Environment Reset. Starting Session...";
        document.getElementById("start-btn").disabled = true;
        document.getElementById("next-btn").disabled = false;
        
        await nextQuestion();
    } catch (error) {
        console.error("Error starting interview:", error);
        document.getElementById("status-val").innerText = "Error connecting to server.";
    }
}

async function nextQuestion() {
    try {
        document.getElementById("next-btn").disabled = true;
        document.getElementById("status-val").innerText = "Evaluating AI response & Generating Question...";
        document.getElementById("question-text").innerText = "Generating next technical question using Hugging Face LLM...";
        
        const response = await fetch(`${API_URL}/step`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: 0 })
        });
        
        const data = await response.json();
        
        updateUI(data.state);
        
        const rewardSpan = document.getElementById("reward-val");
        rewardSpan.innerText = data.reward.toFixed(4);
        rewardSpan.style.color = data.reward >= 0 ? "var(--success)" : "var(--danger)";
        
        document.getElementById("question-text").innerText = data.question;
        document.getElementById("q-number").innerText = `(${data.state.questions_asked}/8)`;
        
        if (data.info && data.info.difficulty) {
            const badge = document.getElementById("difficulty-badge");
            badge.innerText = data.info.difficulty.toUpperCase();
            badge.className = `badge ${data.info.difficulty}`;
        }
        
        if (data.done) {
            document.getElementById("status-val").innerText = "Interview Session Completed!";
            document.getElementById("next-btn").disabled = true;
            document.getElementById("start-btn").disabled = false;
            document.getElementById("start-btn").innerText = "Start New Session";
            document.getElementById("difficulty-badge").innerText = "DONE";
            document.getElementById("difficulty-badge").className = "badge";
        } else {
            document.getElementById("status-val").innerText = "Awaiting Action...";
            document.getElementById("next-btn").disabled = false;
        }
        
    } catch (error) {
        console.error("Error fetching next question:", error);
        document.getElementById("status-val").innerText = "Error communicating with server.";
        document.getElementById("next-btn").disabled = false;
    }
}

function updateUI(state) {
    const fields = [
        { id: "tech", val: state.technical_score },
        { id: "comm", val: state.communication_score },
        { id: "conf", val: state.confidence_score },
        { id: "fatigue", val: state.fatigue }
    ];
    
    fields.forEach(f => {
        const percentage = Math.min(100, Math.max(0, f.val * 100));
        const bar = document.getElementById(`${f.id}-bar`);
        bar.style.width = `${percentage}%`;
        
        // Dynamic colors for values
        if (f.id !== "fatigue") {
            if (f.val > 0.7) bar.style.backgroundColor = "var(--success)";
            else if (f.val > 0.4) bar.style.backgroundColor = "var(--primary)";
            else bar.style.backgroundColor = "var(--warning)";
        } else {
            if (f.val > 0.7) bar.style.backgroundColor = "var(--danger)";
            else if (f.val > 0.4) bar.style.backgroundColor = "var(--warning)";
            else bar.style.backgroundColor = "var(--success)";
        }

        document.getElementById(`${f.id}-val`).innerText = f.val.toFixed(2);
    });
}
