#!/usr/bin/env node
const express = require('express');
const { ethers } = require('ethers');
const cors = require('cors');
const app = express();
app.use(express.json({limit:'10mb'}));
app.use(cors());

const PRIVATE_KEY = process.env.SIGNER_KEY || '0x...';
const CONTRACT_ADDR = '0x...'; // Deployed ESQET-QH-NFT
const wallet = new ethers.Wallet(PRIVATE_KEY, ethers.getDefaultProvider('polygon'));

app.post('/sign-voucher', async (req, res) => {
    const { tokenId, price, minterAddress, metadata } = req.body;
    const domain = { name: 'QuantumHolographicNFT', version: '1', 
                   chainId: 137, verifyingContract: CONTRACT_ADDR };
    const types = { LazyMintVoucher: [
        {name:'tokenId',type:'uint256'}, {name:'price',type:'uint256'},
        {name:'minterAddress',type:'address'}, {name:'tokenURI',type:'string'}
    ]};
    const voucher = { tokenId, price: ethers.parseEther(price.toString()), 
                     minterAddress, tokenURI: `ipfs://Qm${tokenId}` };
    const sig = await wallet.signTypedData(domain, types, voucher);
    res.json({ voucher, signature: sig });
});

app.listen(3000, () => console.log('🪙 QH-NFT @ localhost:3000'));
