import json
from web3 import Web3
import asyncio

web3 = Web3(Web3.HTTPProvider(f'https://bsc-dataseed1.binance.org/'))

async def test():
    pancake_router = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
    pancake_router_file = open('pancakeRouter.json')
    pancake_router_abi = json.load(pancake_router_file)

    pancake_factory = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'
    pancake_factory_file = open('pancakeFactory.json')
    pancake_factory_abi = json.load(pancake_factory_file)

    pancake_router_contract = web3.eth.contract(address=pancake_router, abi=pancake_router_abi)
    pancake_factory_contract = web3.eth.contract(address=pancake_factory, abi=pancake_factory_abi)

    pair_address = pancake_factory_contract.functions.getPair(web3.to_checksum_address('0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82'), web3.to_checksum_address('0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c')).call()
    pair_file = open('pair.json')
    pair_abi = json.load(pair_file)

    pair_contract = web3.eth.contract(address=pair_address, abi=pair_abi)


    """
    get reserves
    """

    # pair reserves - number of remaining tokens in pool
    # be sure noticing that you need to manually understand 
    # what is token1_reserves and token2_reserves 
    # because otherwise the price will be different from pancake
    pair_reserves = pair_contract.functions.getReserves().call()

    token1_reserves = pair_reserves[0]
    token2_reserves = pair_reserves[1]
    timestamp = pair_reserves[2]

    """
    get token addresses
    """

    token1 = pair_contract.functions.token0().call()
    token2 = pair_contract.functions.token1().call()

    # load abi
    token_file = open('tokenAbi.json')
    token_abi = json.load(token_file)

    # create contract instance
    token1_contract = web3.eth.contract(address=token1, abi=token_abi)
    token2_contract = web3.eth.contract(address=token2, abi=token_abi)

    # get symbols like BNB or USDT
    token1_symbol = token1_contract.functions.symbol().call()
    token2_symbol = token2_contract.functions.symbol().call()
    
    # get decimals - 18
    token1_decimals = token1_contract.functions.decimals().call()
    token2_decimals = token2_contract.functions.decimals().call()

    """
    swap tokens
    """
    # define amount
    amount = 1000000

    # path can be whatever 2 tokens you need
    path = [token1, token2]

    # here we have two possible variants on how to calculate amount out
    # this is the first variant 
    _amounts_out = pancake_router_contract.functions.getAmountsOut(amount, path)

    # this is the second

    # define slippage and calculating amountOut
    # making format(0) because blockchain does not support float values. Or just work around with BigNumber
    _slippage = .2
    amountOut = '{:100000000.0f}'.format(0)
    percentage = (amountOut * _slippage)/100
    amountOut = amountOut - percentage
    amountOut = amountOut.format(0)

    amountIn = '{:100000000.0f}'.format(0)

    toAddress = ""

    # this is the time after what a transaction will be canceled
    deadline = 2000000000

    # some of tokens supports custom token fee, so wee need to be sure calling swapExactTokensForETHSupportingFeeOnTransferTokens function
    support_custom_fee = True

    swap = pair_contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(amountIn, amountOut, path, toAddress, deadline) if support_custom_fee == True else pair_contract.functions.swapExactTokensForETH(amountIn, amountOut, path, toAddress, deadline)
  
    swap = pair_contract.functions.swapExactTokensForETH(amountIn, amountOut, path, toAddress, deadline)

    # then just simply sign and send transaction as I showed you in main.py



async def main():
    await test()

asyncio.run(main())