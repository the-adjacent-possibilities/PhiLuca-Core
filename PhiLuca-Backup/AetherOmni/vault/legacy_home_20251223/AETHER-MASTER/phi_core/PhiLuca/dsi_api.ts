export interface LHCSimRequest {
  sqrt_s: number;
  n_events: number;
  lambda_sterile: number;
  C_alpha_scar: number;
}

export interface LHCSimResponse {
  status: string;
  mean_phi_esk: number;
  instability_rate: number;
  high_pt_jets: number;
  verdict: string;
}

export async function simulateLHC(request: LHCSimRequest): Promise<LHCSimResponse> {
  const response = await fetch('/api/simulate-lhc', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  if (!response.ok) throw new Error(`API failed: ${response.status}`);
  return response.json();
}
