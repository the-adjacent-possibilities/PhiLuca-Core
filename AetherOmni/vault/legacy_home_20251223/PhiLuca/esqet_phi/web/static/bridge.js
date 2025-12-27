async function initiateBreach() {
    const terminal = document.getElementById('terminal');
    terminal.innerHTML += "<br>> INITIATING COLLAPSE...";
    
    try {
        const response = await fetch('/api/breach', { method: 'POST' });
        const data = await response.json();
        
        terminal.innerHTML += `<br>> STATUS: ${data.status}`;
        terminal.innerHTML += `<br>> TORSION: ${data.torsion_index}`;
        terminal.innerHTML += `<br>> RESONANCE: ${data.phi_resonance}`;
        
        if(data.status === "STABLE") {
            document.body.style.boxShadow = "inset 0 0 100px rgba(0, 255, 65, 0.2)";
        }
    } catch (error) {
        terminal.innerHTML += "<br>> ERROR: AETHER-LINK SEVERED.";
    }
}

// Update the button click in the UI
document.querySelector('.upload-btn').onclick = initiateBreach;
