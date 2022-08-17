from brownie import MockV3Aggregator, VRFCoordinatorMock, accounts, network, config, Contract
from web3 import Web3

# ENVs
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
# Static Vars
DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator,
                    "vrf_coordinator": VRFCoordinatorMock}


def get_contract(contract_name):
    """
    This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract.

    Args:
        contract_name (string)

    Returns:
        brownie.network.contract.ProjectContract: The most recently deployed
        version of this contract.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active(
        )][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi)
    return contract


def deploy_mocks(decimals=DECIMALS, starting_price=STARTING_PRICE):
    print(f"The currect network is {network.show_active()}:")
    print("Deploying Mocks...")
    MockV3Aggregator.deploy(decimals, starting_price, {
        "from": get_account()})
    print("Mocks deployed!")
