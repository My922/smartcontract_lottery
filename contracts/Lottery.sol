// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    AggregatorV3Interface internal ethUsdPriceFeed;
    address public admin;
    address payable[] public players;
    uint256 public usdEntryFee;

    /**
     * Network: Rinkeby
     * Aggregator: ETH/USD
     * Address: 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419
     */
    constructor() public {
        // $50 minimum
        // require(condition);
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(
            0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419
        );
        admin = msg.sender;
    }

    function enter() public {
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {}

    function startLottery() public {}

    function endLottery() public {}

    modifier onlyAdmin() {
        require(msg.sender == admin);
        _;
    }

    function getLatestPrice() public view returns (int256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        return price;
    }
}
