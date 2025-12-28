#!/usr/bin/env node
const express = require('express');
const cors = require('cors');
const app = express();
app.use(express.json());
app.use(cors());

const PHI = (1 + Math.sqrt(5)) / 2;

app.post('/sign-voucher', (req, res) => {
    const { tokenId, metadata } = req.body;
    const fqc = 1 + PHI * Math.PI * 0.3903 * 0.5;
    const signature = `0x${Buffer.from(JSON.stringify({tokenId, fqc})).toString('hex')}`;
    
    res.json({
        voucher: { tokenId, price: (150 * Math.pow(PHI, 4)).toFixed(2), tokenURI: `ipfs://Qm${tokenId}` },
        signature,
        fqc: fqc.toFixed(4)
    });
});

app.listen(3000, () => console.log('🪙 ESQET NFT Server: http://localhost:3000'));
