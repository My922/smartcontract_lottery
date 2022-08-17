from scripts.helpful_scripts import Lottery, get_account, get_contract


def deploy_lottery():
    account = get_account(id="my_account")
    contract = Lottery.deploy(get_contract("eth_usd_price_feed").address)


def main():
    deploy_lottery()
