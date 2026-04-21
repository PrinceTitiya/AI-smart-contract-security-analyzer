// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AccessControl {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function withdrawAll() public {
        payable(msg.sender).transfer(address(this).balance);
    }
}
