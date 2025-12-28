// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC721A/ERC721A.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/cryptography/draft-EIP712.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

contract ESQETQHNFT is ERC721A, Ownable, EIP712 {
    using ECDSA for bytes32;
    address public signerAddress;
    struct LazyMintVoucher { uint256 tokenId; uint256 price; address minterAddress; string tokenURI; }
    mapping(uint256 => uint256) public tokenPrice;
    mapping(uint256 => string) public tokenURI;
    
    constructor(address _signer) ERC721A("ESQET QH-NFT","QHNT") 
        EIP712("QuantumHolographicNFT","1") Ownable(msg.sender) { signerAddress = _signer; }
    
    function lazyMint(LazyMintVoucher calldata voucher, bytes calldata signature) external payable {
        require(_verifyVoucher(voucher, signature) == signerAddress, "Invalid sig");
        require(msg.value >= voucher.price, "Low payment");
        require(!_exists(voucher.tokenId));
        _safeMint(msg.sender, voucher.tokenId);
        tokenPrice[voucher.tokenId] = voucher.price;
        tokenURI[voucher.tokenId] = voucher.tokenURI;
    }
    
    function _verifyVoucher(LazyMintVoucher calldata v, bytes calldata sig) internal view returns (address) {
        bytes32 structHash = keccak256(abi.encode(keccak256("LazyMintVoucher(uint256 tokenId,uint256 price,address minterAddress,string tokenURI)"), v.tokenId, v.price, v.minterAddress, keccak256(bytes(v.tokenURI))));
        return ECDSA.recover(_hashTypedDataV4(structHash), sig);
    }
}
