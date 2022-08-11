// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    AggregatorV3Interface internal ethUsdPriceFeed;
    address public admin;
    address payable[] public players;
    uint256 public usdEntryFee;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;

    /**
     * Network: Rinkeby
     * Aggregator: ETH/USD
     * Address: 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419
     */
    constructor(address _priceFeedAddress) public {
        // $50 minimum
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        admin = msg.sender;
        lottery_state = LOTTERY_STATE.CLOSED;
    }

    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(msg.value >= getEntranceFee(), "You need more ETH! (50 ETH)");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 adjustedPrice = getLatestPrice();
        uint256 costToEnter = (usdEntryFee * (10**18)) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public {}

    function endLottery() public {}

    modifier onlyAdmin() {
        require(msg.sender == admin);
        _;
    }

    function getLatestPrice() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        return uint256(price) * (10**10);
    }
}
