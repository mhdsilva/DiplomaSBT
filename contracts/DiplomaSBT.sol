// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract DiplomaSBT is ERC721URIStorage, Ownable {
    uint256 private _nextTokenId;

    constructor() ERC721("Certificado Academico", "CERT") Ownable(msg.sender) {}

    function issueDiploma(address student, string memory tokenURI)
        public
        onlyOwner
        returns (uint256)
    {
        uint256 tokenId = _nextTokenId++;
        _mint(student, tokenId);
        _setTokenURI(tokenId, tokenURI);
        return tokenId;
    }

    function transferFrom(address from, address to, uint256 tokenId) public override(ERC721, IERC721) {
        revert("Erro: Este diploma e intransferivel (Soulbound Token).");
    }

    function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory data) public override(ERC721, IERC721) {
        revert("Erro: Este diploma e intransferivel (Soulbound Token).");
    }
}