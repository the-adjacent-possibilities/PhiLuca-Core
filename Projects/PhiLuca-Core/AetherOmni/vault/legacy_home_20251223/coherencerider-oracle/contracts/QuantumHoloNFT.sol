// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC721A/ERC721A.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract QuantumHoloNFT is ERC721A, Ownable {
    mapping(uint256 => string) public tokenURI;
    
    constructor() ERC721A("QuantumHoloNFT", "QHNT") Ownable(msg.sender) {}
    
    function mint(address to, uint256 tokenId, string memory uri) external onlyOwner {
        _safeMint(to, tokenId);
        tokenURI[tokenId] = uri;
    }
    
    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
        return tokenURI[tokenId];
    }
}
