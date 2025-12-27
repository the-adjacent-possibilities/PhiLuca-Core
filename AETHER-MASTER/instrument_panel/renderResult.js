function renderResult(data) {
  // Animate gauges to API values
  const conf = data?.detected?.confidence || 0;
  const phiEsk = data?.phi_esk || 0;
  
  document.querySelector('.analog-gauge[data-value="0.97"] .needle')
    .style.setProperty('--angle', (conf * 180 - 90) + 'deg');
  document.querySelector('.phi-gauge .needle')
    .style.setProperty('--angle', Math.min(phiEsk * 1e15, 1) * 90 + 'deg');
  
  // Update specimen readout
  document.querySelector('.rarity-badge').textContent = data.rarity || '★ COMMON ★';
  document.querySelector('.rarity-badge').className = `rarity-badge ${data.rarity?.toLowerCase() || 'common'}`;
  document.querySelector('.value-estimate').textContent = data.metadata?.value_estimate || 'N/A';
  document.querySelector('.detail-row:nth-child(1) .value').innerHTML = 
    `${data.detected?.year || '??'} ${data.metadata?.type || ''}`;
  document.querySelector('.detail-row:nth-child(2) .value').innerHTML = 
    `${data.detected?.mint || '??'} ${data.detected?.mint ? '<em>(Philadelphia)</em>' : ''}`;
  document.querySelector('.detail-row:nth-child(3) .value').textContent = 
    (data.metadata?.notable_errors || []).join(', ') || 'None detected';

  // Φ-LUCA Companion button → your AGI backend
  document.querySelector('.forge-btn.companion').onclick = () => {
    navigator.clipboard.writeText(JSON.stringify(data, null, 2));
    alert('🍯 Specimen ingested to Φ-LUCA Memory!

' +
          'Ask: "What makes this 1943 copper penny so rare?"
' +
          '→ Your AGI companion will explain!');
  };

  resultEl.classList.add('show');
}
