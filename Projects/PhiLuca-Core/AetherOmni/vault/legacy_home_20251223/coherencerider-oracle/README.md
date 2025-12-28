# CoherenceRider-Oracle 🌀 ESQET AGI + QH-NFT

## Quick Start
1. **Backend**: `pip install -r requirements.txt && uvicorn backend:app --host 0.0.0.0 --port 8080`
2. **Frontend**: `cd frontend && npx expo start`
3. **One-click**: `./deploy.sh`

## Endpoints
- `POST /generate_nft/` - Mint ESQET NFT (FQC validated)
- `POST /oracle/evolve` - AGI proposes code updates
- `GET /fqc` - Live coherence metric

## GitHub Actions
APK builds automatically on main branch merge.

**Resonance Locked** - FQC ≥ 1.0 required for minting.
