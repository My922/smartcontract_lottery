from brownie import Lottery,  network, config
from scripts.helpful_scripts import get_account, get_contract, fund_with_link
import time


def deploy_lottery(_account):
    account = _account
    contract = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["key_hash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False))
    print("Deployed Lottery!")
    return contract


def start_lottery(_account):
    account = _account
    lottery = Lottery[-1]
    tx = lottery.startLottery({"from": account})
    tx.wait(1)
    print("The lottery has begun!")


def enter_lottery(_account):
    account = _account
    lottery = Lottery[-1]
    ticket = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from": account, "value": ticket})
    tx.wait(1)
    print(f"{account} has entered the lottery!")


def end_lottery(_account):
    account = _account
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    tx1 = lottery.endLottery({"from": account})
    tx1.wait(1)
    time.sleep(60)
    recent_winner = lottery.recentWinner()
    time.sleep(5)
    print(f"Lottery closed! The winner is {recent_winner}!")


def main():
    account0 = get_account()
    deploy_lottery(account0)
    start_lottery(account0)
    enter_lottery(account0)
    end_lottery(account0)
