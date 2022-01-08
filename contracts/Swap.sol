// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";



contract Swap {


	uint public constantOfTheSwap = 0;
	IERC20 public daoToken;
	IERC20 public wethToken;
	AggregatorV3Interface internal priceFeed;
	address daoTokenAddress;
	address wethTokenAddress;
	uint public startingBalanceOfWeth = 0;
	uint public startingBalanceOfDao = 0;


	// This mapping will track 
	mapping(address => uint) public tokenBalance;


	constructor(address _wethTokenAddress, address _daoTokenAddress, address _aggregatorV3Interface) public {
		priceFeed = AggregatorV3Interface(_aggregatorV3Interface);
		daoToken = IERC20(_daoTokenAddress);
		wethToken = IERC20(_wethTokenAddress);
		daoTokenAddress = _daoTokenAddress;
		wethTokenAddress = _wethTokenAddress;
	}

	function StartSwap(uint _amount, uint _daoAmount) public {
		wethToken.transferFrom(msg.sender, address(this), _amount);
		daoToken.transferFrom(msg.sender, address(this), _daoAmount);
		tokenBalance[daoTokenAddress] = daoToken.balanceOf(address(this));
		tokenBalance[wethTokenAddress] = wethToken.balanceOf(address(this));
	}


	function setConstant() public {
		constantOfTheSwap = tokenBalance[daoTokenAddress] * tokenBalance[wethTokenAddress];
	}	



	function swap(address _token, address _tokenToSendBack, uint _amount) public {

		IERC20(_token).transferFrom(msg.sender, address(this), _amount);
		tokenBalance[_token] = tokenBalance[_token] + _amount;
		uint howMuchShouldBeInThePool = constantOfTheSwap / tokenBalance[_token];
		uint toSend = tokenBalance[_tokenToSendBack] - howMuchShouldBeInThePool;
		// tokenBalance[_token] = tokenBalance[_token] - howMuchShouldBeInThePool;

		if (_token == daoTokenAddress) {
			wethToken.transfer(msg.sender, toSend);
		}
		else if (_token == wethTokenAddress) {
			daoToken.transfer(msg.sender, toSend);
		}
		tokenBalance[_tokenToSendBack] = tokenBalance[_tokenToSendBack] - howMuchShouldBeInThePool;
	}


	function showBalance() public view returns (uint, uint) {
		uint one = tokenBalance[wethTokenAddress];
		uint two = tokenBalance[daoTokenAddress];
		return (one, two);
	}


	function getPrice() public view returns (uint) {
		(,int price,,,) = priceFeed.latestRoundData();
		// This will return price in wei of eth
		uint adjustedPrice = uint(price) * 10**10;
		return adjustedPrice;
	}


	function showPrice(address _token, uint _amount) public view returns (uint) {
		if (_token == wethTokenAddress) {
			uint latestPrice = getPrice();
			uint usersAmount = _amount * latestPrice;
			return usersAmount;
		}
		else if (_token == daoTokenAddress) {
			uint latestPrice = getPrice();
			uint ethInContract = tokenBalance[wethTokenAddress];
			uint daoInContract = tokenBalance[daoTokenAddress];
			uint totalPriceOfEthInContract = latestPrice * ethInContract;
			uint daoPrice = totalPriceOfEthInContract / daoInContract;
			uint finalPrice = _amount * daoPrice;
			return finalPrice;
		}
	}


	function withdraw() public {
		uint balanceOfContractWeth = wethToken.balanceOf(address(this));
		uint balanceOfContractDao = daoToken.balanceOf(address(this));
        wethToken.transfer(msg.sender, balanceOfContractWeth);
        daoToken.transfer(msg.sender, balanceOfContractDao);
    }
} 