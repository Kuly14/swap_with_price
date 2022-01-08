from brownie import Swap, config, network, interface
from scripts.help import get_account
from web3 import Web3



KEPT_BALANCE = Web3.toWei(150, "ether")
amounts = Web3.toWei(10, "ether")




def deploy():
	account = get_account()
	# token = Token.deploy({"from": account})
	swap = Swap.deploy(
		config["networks"][network.show_active()]["weth_token"], 
		config["networks"][network.show_active()]["dao_token"], 
		config["networks"][network.show_active()]["eth_usd_price_feed"], 
		{"from": account}
	)
	print("DEPLOYED!")


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    return tx

# def start_swap():
# 	print("Starting Swap!")
# 	account = get_account()
# 	swap = Swap[-1]
# 	weth_address = config["networks"][network.show_active()]["weth_token"]
# 	dao_address = config["networks"][network.show_active()]["dao_token"]
# 	amountToSend = Web3.toWei(0.1, "ether")
# 	approve_tx = approve_erc20(amounts, swap.address, erc20_address, account)
# 	approve_tx2 = approve_erc20()
# 	tx = swap.StartSwap(amountToSend, {"from": account})
# 	tx.wait(1)
# 	print("Swap started!")



def start_swap():
	account = get_account()
	swap = Swap[-1]
	weth_address = config["networks"][network.show_active()]["weth_token"]
	dao_address = config["networks"][network.show_active()]["dao_token"]
	weth_amount = Web3.toWei(1, "ether")
	dao_amount = Web3.toWei(100, "ether")
	amountToSendWeth = Web3.toWei(0.1, "ether")
	amountToSendDao = Web3.toWei(50, "ether")
	approve_tx_weth = approve_erc20(weth_amount, swap.address, weth_address, account)
	approve_tx_dao = approve_erc20(dao_amount, swap.address, dao_address, account)
	tx = swap.StartSwap(amountToSendWeth, amountToSendDao, {"from": account})
	tx.wait(1)


def setConstant():
	account = get_account()
	swap = Swap[-1]
	tx = swap.setConstant({"from": account})
	tx.wait(1)
	constantNum = swap.constantOfTheSwap({"from": account})
	print("Constant Set!")
	print(f"Constant is {constantNum}")


def swap():
	account = get_account()
	swap = Swap[-1]
	weth_address = config["networks"][network.show_active()]["weth_token"]
	dao_address = config["networks"][network.show_active()]["dao_token"]
	weth_amount = Web3.toWei(1, "ether")
	dao_amount = Web3.toWei(100, "ether")
	amountToSendWeth = Web3.toWei(0.1, "ether")
	amountToSendDao = Web3.toWei(50, "ether")
	approve_tx_weth = approve_erc20(weth_amount, swap.address, weth_address, account)
	approve_tx_dao = approve_erc20(dao_amount, swap.address, dao_address, account)
	tx = swap.swap(weth_address, dao_address, amountToSendWeth, {"from": account})
	tx.wait(1)
	print("SWAP SUCCESFULL!!!")



def showBalance():
	account = get_account()
	swap = Swap[-1]
	tx1, tx2 = swap.showBalance({"from": account})
	print(tx1)
	print(tx2)


def getPrice():
	account = get_account()
	swap = Swap[-1]
	weth_address = config["networks"][network.show_active()]["weth_token"]
	dao_address = config["networks"][network.show_active()]["dao_token"]
	tx = swap.showPrice(weth_address, 1, {"from": account})
	print(f"Price of 1 weth is {tx}")
	tx2 = swap.showPrice(dao_address, 1, {"from": account})
	print(f"Price of 1 DAO is {tx2}")


def withdraw():
	account = get_account()
	swap = Swap[-1]
	tx = swap.withdraw({"from": account})
	tx.wait(1)
	print("All tokens withdrawn!")




def main():
	deploy()
	start_swap()
	setConstant()
	showBalance()
	swap()
	showBalance()
	getPrice()
	withdraw()