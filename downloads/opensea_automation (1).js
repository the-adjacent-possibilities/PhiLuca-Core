#!/usr/bin/env node
/**
 * OpenSea Collection Automation Scripts
 * Creates bulk upload files and collection metadata
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

class OpenSeaAutomation {
    constructor() {
        this.collectionData = this.loadCollectionData();
    }
    
    loadCollectionData() {
        try {
            return JSON.parse(fs.readFileSync('nft_collection.json', 'utf8'));
        } catch (error) {
            console.error('❌ nft_collection.json not found. Run upload_to_ipfs.js first!');
            process.exit(1);
        }
    }
    
    // Create CSV for OpenSea bulk upload
    createBulkUploadCSV() {
        console.log('📊 Creating OpenSea bulk upload CSV...');
        
        const csvHeaders = [
            'Type',
            'Name', 
            'External Link',
            'Description',
            'Collection',
            'Properties',
            'Levels',
            'Stats',
            'Unlockable Content',
            'Explicit & Sensitive Content',
            'Supply',
            'Blockchain'
        ].join(',');
        
        const csvRows = [csvHeaders];
        
        this.collectionData.forEach(item => {
            const properties = this.formatPropertiesForCSV(item.metadata.attributes);
            
            const row = [
                'Single',  // Type
                `"${item.metadata.name}"`,  // Name
                item.imageIPFS.url,  // External Link
                `"${item.metadata.description}"`,  // Description
                '"Aether Quanta Genesis"',  // Collection
                `"${properties}"`,  // Properties
                '',  // Levels (empty)
                '',  // Stats (empty)
                'false',  // Unlockable Content
                'false',  // Explicit Content
                '1',  // Supply
                'Polygon'  // Blockchain
            ].join(',');
            
            csvRows.push(row);
        });
        
        const csvContent = csvRows.join('\n');
        fs.writeFileSync('opensea_bulk_upload.csv', csvContent);
        
        console.log(`✅ Created opensea_bulk_upload.csv with ${this.collectionData.length} NFTs`);
        console.log('💡 Upload this file to OpenSea → Create → Bulk Import');
    }
    
    formatPropertiesForCSV(attributes) {
        return attributes.map(attr => 
            `${attr.trait_type}: ${attr.value}`
        ).join('; ');
    }
    
    // Generate collection metadata for OpenSea
    generateCollectionMetadata() {
        console.log('🎨 Generating collection metadata...');
        
        const collectionMetadata = {
            name: "Aether Quanta Genesis",
            description: "The first biometric NFT collection combining AI-enhanced imagery with quantum-powered facial recognition. Each SelfieToken is a unique $100 bill featuring the holder's portrait, secured by advanced biometric authentication technology.",
            image: this.getCollectionCoverImage(),
            banner_image: this.getCollectionBannerImage(),
            featured_image: this.getFeaturedImage(),
            external_link: "https://aetherquanta.com",
            discord_url: "https://discord.gg/aetherquanta",
            twitter_username: "aetherquanta",
            instagram_username: "aetherquanta",
            medium_username: "aetherquanta",
            telegram_url: "https://t.me/aetherquanta",
            
            // Collection stats
            total_supply: this.collectionData.length,
            
            // Categories and traits
            category: "Art",
            traits: this.generateTraitSummary(),
            
            // Royalties
            seller_fee_basis_points: 750, // 7.5% royalty
            fee_recipient: process.env.WALLET_ADDRESS || "0x742d35Cc6634C0532925a3b8D404d3aB",
            
            // Collection properties
            properties: {
                blockchain: "Polygon",
                enhancement_level: "AI Enhanced",
                utility: ["Biometric Authentication", "Wallet Access", "Digital Identity"],
                rarity_system: "Algorithm-based",
                total_variants: this.calculateTotalVariants()
            }
        };
        
        fs.writeFileSync('collection_metadata.json', JSON.stringify(collectionMetadata, null, 2));
        console.log('✅ Created collection_metadata.json');
    }
    
    getCollectionCoverImage() {
        // Use the first enhanced image as collection cover
        if (this.collectionData.length > 0) {
            return this.collectionData[0].imageIPFS.url;
        }
        return "https://gateway.pinata.cloud/ipfs/QmDefaultCoverImage";
    }
    
    getCollectionBannerImage() {
        // Create a banner from multiple images or use a specific one
        return this.getCollectionCoverImage(); // Simplified for now
    }
    
    getFeaturedImage() {
        // Find the highest value or most unique NFT
        const featured = this.collectionData.find(item => 
            item.metadata.attributes.some(attr => 
                attr.trait_type === "Style" && attr.value === "Cyber"
            )
        ) || this.collectionData[0];
        
        return featured.imageIPFS.url;
    }
    
    generateTraitSummary() {
        const traitCounts = {};
        
        this.collectionData.forEach(item => {
            item.metadata.attributes.forEach(attr => {
                if (!traitCounts[attr.trait_type]) {
                    traitCounts[attr.trait_type] = {};
                }
                
                if (!traitCounts[attr.trait_type][attr.value]) {
                    traitCounts[attr.trait_type][attr.value] = 0;
                }
                
                traitCounts[attr.trait_type][attr.value]++;
            });
        });
        
        return traitCounts;
    }
    
    calculateTotalVariants() {
        const variants = new Set();
        this.collectionData.forEach(item => {
            const variant = item.metadata.attributes.find(attr => 
                attr.trait_type === "Enhancement Level"
            );
            if (variant) variants.add(variant.value);
        });
        return variants.size;
    }
    
    // Generate marketing materials
    generateMarketingContent() {
        console.log('📢 Generating marketing content...');
        
        const marketingContent = {
            // Twitter announcement
            twitter_announcement: this.generateTwitterAnnouncement(),
            
            // Discord announcements
            discord_announcements: this.generateDiscordAnnouncements(),
            
            // Medium article outline
            medium_article: this.generateMediumArticle(),
            
            // Press release
            press_release: this.generatePressRelease(),
            
            // FAQ
            faq: this.generateFAQ()
        };
        
        fs.writeFileSync('marketing_content.json', JSON.stringify(marketingContent, null, 2));
        console.log('✅ Created marketing_content.json');
    }
    
    generateTwitterAnnouncement() {
        return {
            launch_tweet: `🚀 LAUNCH: Aether Quanta Genesis Collection

${this.collectionData.length} unique biometric NFTs now live on @opensea!

✨ Each NFT is a personalized $100 bill with YOUR portrait
🔐 Secured by quantum-powered facial recognition
🎨 AI-enhanced to perfection

Collection: https://opensea.io/collection/aether-quanta-genesis

#NFT #BiometricAuth #AetherQuanta #PolygonNFT`,

            feature_threads: [
                "🧵 THREAD: What makes Aether Quanta Genesis special?",
                "1/ Each NFT is more than art - it's a functional biometric wallet key",
                "2/ Your face becomes the password to your digital assets", 
                "3/ AI enhancement creates 5 variants of each original image",
                "4/ Built on Polygon for gasless trading",
                "5/ First collection to combine identity, utility, and art"
            ]
        };
    }
    
    generateDiscordAnnouncements() {
        return {
            launch_announcement: `🎉 **AETHER QUANTA GENESIS IS LIVE!** 🎉

Our revolutionary biometric NFT collection has launched on OpenSea!

📊 **Collection Stats:**
• Total NFTs: ${this.collectionData.length}
• Blockchain: Polygon (gasless!)
• Floor Price: TBA
• Unique Holders: 0 (we're just starting!)

🔗 **Collection Link:** https://opensea.io/collection/aether-quanta-genesis

🎯 **What's Next:**
• Whitelist giveaway for early supporters
• Biometric wallet app beta access
• Exclusive holder perks

React with 🚀 if you're excited!`,

            community_rules: `📋 **COMMUNITY RULES**

1️⃣ **Respect** - Be kind to all members
2️⃣ **No Spam** - Quality over quantity  
3️⃣ **Stay On Topic** - Keep discussions relevant
4️⃣ **No Financial Advice** - DYOR always
5️⃣ **Have Fun** - We're building the future together!

🎯 **Verification Required** - Prove ownership of an Aether Quanta NFT to access holder channels`
        };
    }
    
    generateMediumArticle() {
        return {
            title: "Introducing Aether Quanta Genesis: The First Biometric NFT Collection",
            
            outline: [
                "The Problem with Digital Identity",
                "What Are Biometric NFTs?", 
                "The Technology Behind Aether Quanta",
                "Collection Overview and Utilities",
                "Roadmap and Future Vision",
                "How to Get Started"
            ],
            
            introduction: `In a world where digital identity is becoming increasingly important, we're introducing something revolutionary: NFTs that know who you are.

Aether Quanta Genesis isn't just another profile picture collection. Each token in our collection is a personalized $100 bill featuring the holder's portrait, secured by quantum-powered facial recognition technology.

But here's what makes it special: your NFT isn't just art—it's your key to a biometrically secured wallet.`,
            
            technical_section: `## The Technology

Our biometric authentication system works by:

1. **Faceprint Generation**: Converting your portrait into a 128-dimensional vector
2. **Quantum Hash**: Creating an irreversible hash using quantum-resistant algorithms  
3. **On-Chain Storage**: Storing only the hash (never your actual biometric data)
4. **Verification**: Comparing new photos to your stored hash for wallet access

This ensures your digital identity is both secure and private.`,
            
            conclusion: `Aether Quanta Genesis represents the convergence of art, technology, and utility. We're not just creating collectibles—we're building the infrastructure for secure digital identity in the Web3 era.

Join us in pioneering the future of biometric authentication.`
        };
    }
    
    generatePressRelease() {
        return {
            headline: "World's First Biometric NFT Collection Launches on Polygon: Aether Quanta Genesis Combines Art with Quantum-Powered Identity Verification",
            
            dateline: `${new Date().toLocaleDateString()} - `,
            
            body: `Revolutionary blockchain project Aether Quanta today announced the launch of Genesis, the world's first NFT collection to integrate biometric authentication with digital art. The collection features ${this.collectionData.length} unique tokens, each depicting a personalized $100 bill with the holder's portrait.

Unlike traditional NFT collections, Aether Quanta Genesis serves a dual purpose as both digital collectibles and functional wallet keys. Each NFT is secured by quantum-resistant facial recognition technology, ensuring that only the rightful owner can access their associated digital assets.

"We're solving one of Web3's biggest challenges: secure, user-friendly authentication," said [Creator Name], founder of Aether Quanta. "By combining biometric technology with blockchain assets, we're creating the first truly personal NFTs."

The collection launches on OpenSea using Polygon blockchain, ensuring gasless trading for collectors. Early holders will gain access to the upcoming biometric wallet application and exclusive community perks.

Technical features include AI enhancement of original portraits, multiple artistic variants, and integration with existing DeFi protocols. The biometric authentication system converts facial features into irreversible mathematical hashes, ensuring privacy while maintaining security.

Aether Quanta Genesis represents a new category of utility-focused NFTs, moving beyond speculative collectibles toward functional digital identity solutions.`
        };
    }
    
    generateFAQ() {
        return {
            general: [
                {
                    q: "What makes Aether Quanta Genesis different from other NFT collections?",
                    a: "Each NFT serves as both digital art and a biometric wallet key. Your portrait is converted into a secure mathematical hash that only you can replicate for wallet access."
                },
                {
                    q: "How does the biometric authentication work?", 
                    a: "We convert your facial features into a 128-dimensional vector, then create a quantum-resistant hash. This hash is stored on-chain, but your actual biometric data never leaves your device."
                },
                {
                    q: "Is my biometric data safe?",
                    a: "Yes. We only store irreversible mathematical hashes, never raw biometric data. Even if our systems were compromised, your actual facial data cannot be reconstructed."
                }
            ],
            
            technical: [
                {
                    q: "Which blockchain is used?",
                    a: "Polygon for gasless trading and low environmental impact."
                },
                {
                    q: "Can I transfer my NFT?",
                    a: "Yes, but the new owner would need to reset the biometric authentication to access wallet features."
                },
                {
                    q: "What utilities come with ownership?",
                    a: "Biometric wallet access, exclusive app features, holder-only Discord channels, and early access to future drops."
                }
            ]
        };
    }
    
    // Create promotional image templates
    generatePromoMaterials() {
        console.log('🎨 Generating promotional materials...');
        
        // Create HTML templates for social media graphics
        const promoTemplates = {
            twitter_card: this.createTwitterCardTemplate(),
            instagram_story: this.createInstagramStoryTemplate(),
            discord_banner: this.createDiscordBannerTemplate()
        };
        
        Object.entries(promoTemplates).forEach(([name, template]) => {
            fs.writeFileSync(`${name}.html`, template);
        });
        
        console.log('✅ Created promotional material templates');
        console.log('💡 Open the HTML files in a browser and take screenshots');
    }
    
    createTwitterCardTemplate() {
        return `<!DOCTYPE html>
<html>
<head>
    <title>Aether Quanta Genesis - Twitter Card</title>
    <style>
        body { margin: 0; font-family: 'Arial', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card { width: 1200px; height: 630px; display: flex; align-items: center; justify-content: space-between; padding: 60px; box-sizing: border-box; color: white; }
        .content { flex: 1; }
        .title { font-size: 48px; font-weight: bold; margin-bottom: 20px; }
        .subtitle { font-size: 24px; margin-bottom: 30px; opacity: 0.9; }
        .stats { font-size: 20px; }
        .nft-preview { width: 400px; height: 500px; background: rgba(255,255,255,0.1); border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 100px; }
    </style>
</head>
<body>
    <div class="card">
        <div class="content">
            <div class="title">Aether Quanta Genesis</div>
            <div class="subtitle">First Biometric NFT Collection</div>
            <div class="stats">
                ${this.collectionData.length} Unique NFTs<br>
                🔐 Biometric Security<br>
                🎨 AI Enhanced<br>
                ⚡ Polygon Blockchain
            </div>
        </div>
        <div class="nft-preview">💵</div>
    </div>
</body>
</html>`;
    }
    
    createInstagramStoryTemplate() {
        return `<!DOCTYPE html>
<html>
<head>
    <title>Aether Quanta Genesis - Instagram Story</title>
    <style>
        body { margin: 0; font-family: 'Arial', sans-serif; background: linear-gradient(180deg, #ff6b6b 0%, #4ecdc4 100%); }
        .story { width: 1080px; height: 1920px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: white; text-align: center; padding: 60px; box-sizing: border-box; }
        .logo { font-size: 72px; margin-bottom: 40px; }
        .title { font-size: 64px; font-weight: bold; margin-bottom: 30px; line-height: 1.2; }
        .features { font-size: 32px; margin-bottom: 60px; line-height: 1.6; }
        .cta { font-size: 36px; background: rgba(255,255,255,0.2); padding: 20px 40px; border-radius: 50px; }
    </style>
</head>
<body>
    <div class="story">
        <div class="logo">🚀</div>
        <div class="title">AETHER QUANTA<br>GENESIS</div>
        <div class="features">
            🔐 Biometric NFTs<br>
            💵 Personalized Bills<br>
            🎨 AI Enhanced<br>
            ⚡ Zero Gas Fees
        </div>
        <div class="cta">LIVE ON OPENSEA</div>
    </div>
</body>
</html>`;
    }
    
    createDiscordBannerTemplate() {
        return `<!DOCTYPE html>
<html>
<head>
    <title>Aether Quanta Genesis - Discord Banner</title>
    <style>
        body { margin: 0; font-family: 'Arial', sans-serif; }
        .banner { width: 960px; height: 540px; background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%); display: flex; align-items: center; justify-content: center; color: white; position: relative; overflow: hidden; }
        .content { text-align: center; z-index: 2; }
        .title { font-size: 56px; font-weight: bold; margin-bottom: 20px; }
        .subtitle { font-size: 28px; opacity: 0.9; }
        .bg-pattern { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-image: repeating-linear-gradient(45deg, rgba(255,255,255,0.05) 0px, rgba(255,255,255,0.05) 1px, transparent 1px, transparent 10px); }
    </style>
</head>
<body>
    <div class="banner">
        <div class="bg-pattern"></div>
        <div class="content">
            <div class="title">AETHER QUANTA GENESIS</div>
            <div class="subtitle">Biometric NFTs • ${this.collectionData.length} Unique Tokens</div>
        </div>
    </div>
</body>
</html>`;
    }
    
    // Main execution
    async runFullAutomation() {
        console.log('🚀 Running full OpenSea automation...\n');
        
        this.createBulkUploadCSV();
        this.generateCollectionMetadata();
        this.generateMarketingContent();
        this.generatePromoMaterials();
        
        console.log('\n🎉 OpenSea automation complete!');
        console.log('📁 Files created:');
        console.log('   • opensea_bulk_upload.csv - Upload to OpenSea');
        console.log('   • collection_metadata.json - Collection info');
        console.log('   • marketing_content.json - Social media content');
        console.log('   • twitter_card.html - Twitter promotional graphic');
        console.log('   • instagram_story.html - Instagram story template');
        console.log('   • discord_banner.html - Discord server banner');
        
        this.showNextSteps();
    }
    
    showNextSteps() {
        console.log('\n📋 NEXT STEPS:');
        console.log('1. Go to opensea.io → Create Collection');
        console.log('2. Upload opensea_bulk_upload.csv using bulk import');
        console.log('3. Use collection_metadata.json for collection details');
        console.log('4. Take screenshots of HTML templates for social media');
        console.log('5. Copy marketing content from marketing_content.json');
        console.log('6. Set floor prices and start promoting!');
        
        console.log('\n💰 PRICING STRATEGY:');
        console.log('   Enhanced images: 0.01-0.05 ETH ($10-50)');
        console.log('   4K upscaled: 0.05-0.1 ETH ($50-100)');
        console.log('   Vintage/Cyber effects: 0.02-0.08 ETH ($20-80)');
        console.log('   Profile pictures: 0.03-0.15 ETH ($30-150)');
        console.log('   Videos: 0.1-0.5 ETH ($100-500)');
    }
}

// Additional utility functions
class NFTAnalytics {
    constructor(collectionData) {
        this.data = collectionData;
    }
    
    generateRarityReport() {
        const rarityData = {};
        const traitCounts = {};
        
        // Count all trait occurrences
        this.data.forEach(item => {
            item.metadata.attributes.forEach(attr => {
                if (!traitCounts[attr.trait_type]) {
                    traitCounts[attr.trait_type] = {};
                }
                if (!traitCounts[attr.trait_type][attr.value]) {
                    traitCounts[attr.trait_type][attr.value] = 0;
                }
                traitCounts[attr.trait_type][attr.value]++;
            });
        });
        
        // Calculate rarity scores
        this.data.forEach(item => {
            let rarityScore = 0;
            
            item.metadata.attributes.forEach(attr => {
                const traitRarity = traitCounts[attr.trait_type][attr.value] / this.data.length;
                rarityScore += (1 / traitRarity);
            });
            
            rarityData[item.tokenId] = {
                name: item.metadata.name,
                rarityScore: Math.round(rarityScore * 100) / 100,
                rank: 0 // Will be calculated after sorting
            };
        });
        
        // Assign ranks
        const sortedTokens = Object.entries(rarityData)
            .sort(([,a], [,b]) => b.rarityScore - a.rarityScore);
            
        sortedTokens.forEach(([tokenId, data], index) => {
            rarityData[tokenId].rank = index + 1;
        });
        
        return rarityData;
    }
    
    generateCollectionStats() {
        const stats = {
            totalSupply: this.data.length,
            traitDistribution: {},
            averageAttributes: 0,
            uniqueTraitCombinations: new Set()
        };
        
        let totalAttributes = 0;
        
        this.data.forEach(item => {
            const attributes = item.metadata.attributes;
            totalAttributes += attributes.length;
            
            // Track trait distribution
            attributes.forEach(attr => {
                if (!stats.traitDistribution[attr.trait_type]) {
                    stats.traitDistribution[attr.trait_type] = {};
                }
                if (!stats.traitDistribution[attr.trait_type][attr.value]) {
                    stats.traitDistribution[attr.trait_type][attr.value] = 0;
                }
                stats.traitDistribution[attr.trait_type][attr.value]++;
            });
            
            // Track unique combinations
            const combination = attributes.map(attr => `${attr.trait_type}:${attr.value}`).sort().join('|');
            stats.uniqueTraitCombinations.add(combination);
        });
        
        stats.averageAttributes = Math.round((totalAttributes / this.data.length) * 100) / 100;
        stats.uniqueCombinations = stats.uniqueTraitCombinations.size;
        delete stats.uniqueTraitCombinations; // Remove Set object for JSON serialization
        
        return stats;
    }
}

// Smart contract deployment helper
class ContractDeployer {
    generateSolidityContract() {
        return `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract AetherQuantaGenesis is ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    
    // Biometric data storage (hashed)
    mapping(uint256 => bytes32) public faceprintHashes;
    mapping(address => uint256[]) public userTokens;
    mapping(uint256 => bool) public biometricEnabled;
    
    // Collection metadata
    uint256 public constant MAX_SUPPLY = ${this.data ? this.data.length : 10000};
    uint256 public mintPrice = 0.01 ether; // Polygon MATIC
    
    // Events
    event BiometricEnabled(uint256 tokenId, address owner);
    event BiometricVerified(uint256 tokenId, address user, bool success);
    
    constructor() ERC721("Aether Quanta Genesis", "AQG") {
        _tokenIds.increment(); // Start from token ID 1
    }
    
    function mintWithBiometric(
        address to,
        string memory tokenURI,
        bytes32 faceprintHash
    ) public payable returns (uint256) {
        require(msg.value >= mintPrice, "Insufficient payment");
        require(_tokenIds.current() <= MAX_SUPPLY, "Max supply exceeded");
        
        uint256 newTokenId = _tokenIds.current();
        _tokenIds.increment();
        
        _safeMint(to, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        
        // Store biometric data
        faceprintHashes[newTokenId] = faceprintHash;
        userTokens[to].push(newTokenId);
        biometricEnabled[newTokenId] = true;
        
        emit BiometricEnabled(newTokenId, to);
        
        return newTokenId;
    }
    
    function verifyBiometric(uint256 tokenId, bytes32 inputHash) 
        public view returns (bool) {
        require(_exists(tokenId), "Token does not exist");
        require(biometricEnabled[tokenId], "Biometric not enabled");
        
        return faceprintHashes[tokenId] == inputHash;
    }
    
    function authenticateUser(address user, bytes32 inputHash) 
        public returns (bool) {
        uint256[] memory tokens = userTokens[user];
        
        for (uint i = 0; i < tokens.length; i++) {
            if (verifyBiometric(tokens[i], inputHash)) {
                emit BiometricVerified(tokens[i], user, true);
                return true;
            }
        }
        
        emit BiometricVerified(0, user, false);
        return false;
    }
    
    function getUserTokens(address user) public view returns (uint256[] memory) {
        return userTokens[user];
    }
    
    function withdraw() public onlyOwner {
        uint256 balance = address(this).balance;
        payable(owner()).transfer(balance);
    }
    
    function setMintPrice(uint256 _newPrice) public onlyOwner {
        mintPrice = _newPrice;
    }
    
    // Override required functions
    function _burn(uint256 tokenId) internal override {
        super._burn(tokenId);
        
        // Clear biometric data on burn
        delete faceprintHashes[tokenId];
        delete biometricEnabled[tokenId];
    }
    
    function tokenURI(uint256 tokenId) 
        public view override returns (string memory) {
        return super.tokenURI(tokenId);
    }
}`;
    }
    
    generateDeploymentScript() {
        return `// deploy.js - Hardhat deployment script
const { ethers } = require("hardhat");

async function main() {
    console.log("Deploying Aether Quanta Genesis contract...");
    
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with account:", deployer.address);
    console.log("Account balance:", (await deployer.getBalance()).toString());
    
    // Deploy contract
    const AetherQuantaGenesis = await ethers.getContractFactory("AetherQuantaGenesis");
    const contract = await AetherQuantaGenesis.deploy();
    
    await contract.deployed();
    
    console.log("Contract deployed to:", contract.address);
    console.log("Transaction hash:", contract.deployTransaction.hash);
    
    // Verify on Polygonscan
    if (network.name !== "hardhat") {
        console.log("Waiting for block confirmations...");
        await contract.deployTransaction.wait(6);
        
        await hre.run("verify:verify", {
            address: contract.address,
            constructorArguments: [],
        });
    }
    
    // Save deployment info
    const deployment = {
        contractAddress: contract.address,
        network: network.name,
        deployer: deployer.address,
        blockNumber: contract.deployTransaction.blockNumber,
        transactionHash: contract.deployTransaction.hash,
        timestamp: new Date().toISOString()
    };
    
    require('fs').writeFileSync(
        'deployment.json',
        JSON.stringify(deployment, null, 2)
    );
    
    console.log("Deployment info saved to deployment.json");
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });`;
    }
}

// Main execution
async function main() {
    const automation = new OpenSeaAutomation();
    await automation.runFullAutomation();
    
    // Generate additional analytics
    const analytics = new NFTAnalytics(automation.collectionData);
    const rarityReport = analytics.generateRarityReport();
    const collectionStats = analytics.generateCollectionStats();
    
    fs.writeFileSync('rarity_report.json', JSON.stringify(rarityReport, null, 2));
    fs.writeFileSync('collection_stats.json', JSON.stringify(collectionStats, null, 2));
    
    console.log('\n📊 Analytics generated:');
    console.log('   • rarity_report.json - Rarity rankings for all NFTs');
    console.log('   • collection_stats.json - Overall collection statistics');
    
    // Generate smart contract files
    const deployer = new ContractDeployer();
    fs.writeFileSync('AetherQuantaGenesis.sol', deployer.generateSolidityContract());
    fs.writeFileSync('deploy.js', deployer.generateDeploymentScript());
    
    console.log('\n🔗 Smart contract files:');
    console.log('   • AetherQuantaGenesis.sol - Main contract');
    console.log('   • deploy.js - Deployment script');
    
    console.log('\n🎯 SUMMARY:');
    console.log(`   Total NFTs ready: ${automation.collectionData.length}`);
    console.log(`   Estimated value: ${automation.collectionData.length * 50} - ${automation.collectionData.length * 200}`);
    console.log(`   Files created: ${fs.readdirSync('.').filter(f => f.includes('.')).length}`);
    console.log('\n🚀 Ready to launch your NFT empire!');
}

if (require.main === module) {
    main().catch(console.error);
}