from telegram import (
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import CallbackContext
from utlis.langMessages import *
from utlis.keyboards import *
from utlis.env import *
from utlis.states import *
import telegram
from eth_utils import is_address as is_eth_address
from web3 import Web3

web3 = Web3(Web3.HTTPProvider(RPC_URL))
with open('distrbuter_abi.json', 'r') as f:
    distrbuter_abi = json.load(f)
with open('bep20_abi.json', 'r') as f:
    bep20_abi = json.load(f)
with open('bdfABI.json', 'r') as f:
    bdfABI = json.load(f)


distrbuterAddress = web3.toChecksumAddress(DISTRBUTER_ADDRESS)
busdAddress = web3.toChecksumAddress(BUSD_ADDRESS)
bdfAddress = web3.toChecksumAddress(BDF_ADDRESS)

distrbuterContract = web3.eth.contract(address=distrbuterAddress, abi=distrbuter_abi)
busdContract = web3.eth.contract(address=busdAddress, abi=bep20_abi)
bdfContract = web3.eth.contract(address=bdfAddress, abi=bdfABI)


def start(update: Update, context: CallbackContext):
    try:
        address = context.user_data['address']
        update.message.reply_text(
            text=START_ALREDY_MESSAGE,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(MAIN_BUTTON)
        )
        return MAIN
    except KeyError:
        update.message.reply_text(
            text=START_MESSAGE,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(CANCEL_BUTTON)
        )
        update.message.reply_text(
            text=ENTER_WALLET,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(CANCEL_BUTTON)
        )
    return SET_ADDRESS


def Main(update: Update, context: CallbackContext):
    message = update.message.text
    if message == "💸CLAIM REWARDS":
        claimBUSD(update, context)
    elif message == "🏦BALANCE":
        balance(update, context)
    elif message == "💰Total BUSD Rewards Distributed":
        distrbuterBUSD(update, context)
    elif message == "🔥Total $BDF BURNED":
        totalBDFBurned(update, context)
    elif message == "/start":
        return start(update, context)
    elif message == "➡️SET WALLET":
        update.message.reply_text(
            text=ENTER_WALLET,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(CANCEL_BUTTON)
        )
        return SET_ADDRESS
    return MAIN


def claimBUSD(update: Update, context: CallbackContext):
    try:
        earnings = distrbuterContract.functions.shares(context.user_data['address']).call()
        text = f"""
<b>Unearned Rewards</b>
    <b>BUSD:</b> {"{:,.2f}".format(distrbuterContract.functions.getUnpaidEarnings(web3.toChecksumAddress(context.user_data['address'])).call() / 10 ** 18)}

<b>Total BUSD Earnings:</b> {"{:,.2f}".format(earnings[2] / 10 ** 18)}

You can  manually claim Unearned BUSD rewards buy Connect your Wallet (Metamask, Trust wallet, etc)  with our Dapp:

<a href="https://dashboard.busdfactory.net/">Dashboard</a>

Then click claim rewards
"""
    except KeyError:
        text = NO_WALLET
    update.message.reply_text(
        text=text,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(MAIN_BUTTON)
    )


def distrbuterBUSD(update: Update, context: CallbackContext):
    try:
        text = f"""
<b>Total BUSD Rewards Distrbuted</b>
    <b>BUSD:</b> {"{:,.2f}".format(distrbuterContract.functions.totalDistributed().call() / 10 ** 18)}
"""
    except:
        text = "Error: Please try again"
    update.message.reply_text(
        text=text,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(MAIN_BUTTON)
    )


def totalBDFBurned(update: Update, context: CallbackContext):
    try:
        totalSupply = bdfContract.functions.totalSupply().call()
        totalSupply /= 10 ** 9
        circulatingSupply = bdfContract.functions.getCirculatingSupply().call()
        circulatingSupply /= 10 ** 9
        totalburned = totalSupply - circulatingSupply
        text = f"""
<b>Total BDF Supply</b>
    <b>BDF:</b> {"{:,.2f}".format(totalSupply)}

<b>Total BDF Burned</b>
    <b>BDF:</b> {"{:,.2f}".format(totalburned)}
    <b>{"{:,.2%}".format(totalburned/totalSupply)} Of TotalSupply</b>
    
<b>BDF Circulating Supply</b>
    <b>BDF:</b> {"{:,.2f}".format(circulatingSupply)}
    <b>{"{:,.2%}".format(circulatingSupply/totalSupply)} Of TotalSupply</b>
"""
    except Exception as e:
        print(e)
        text = "Error: Please try again"
    update.message.reply_text(
        text=text,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(MAIN_BUTTON)
    )


def setWallet(update: Update, context: CallbackContext):
    address = update.message.text
    if address == "Cancel":
        update.message.reply_text(
            reply_markup=ReplyKeyboardMarkup(MAIN_BUTTON)
        )
        return MAIN
    if not is_eth_address(address):
        update.message.reply_text(
            text=INVALID_ADDRESS,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(CANCEL_BUTTON)
        )
        return SET_ADDRESS
    context.user_data['address'] = address
    text = f"""
    <b>Wallet Address</b>
    {address}
    """
    update.message.reply_text(
        text=text,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(MAIN_BUTTON)
    )
    return MAIN


def balance(update: Update, context: CallbackContext):
    try:
        earnings = distrbuterContract.functions.shares(web3.toChecksumAddress(context.user_data['address'])).call()
        text = f"""
<b>Your Balance</b>
    <b>BDF:</b> {"{:,.2f}".format(bdfContract.functions.balanceOf(web3.toChecksumAddress(context.user_data['address'])).call() / 10 ** 9)}
    <b>BUSD:</b> {"{:,.2f}".format(busdContract.functions.balanceOf(web3.toChecksumAddress(context.user_data['address'])).call() / 10 ** 18)}

<b>Total BUSD Earnings:</b> {"{:,.2f}".format(earnings[2] / 10 ** 18)}
"""

    except KeyError:
        text = NO_WALLET
    update.message.reply_text(
        text=text,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(MAIN_BUTTON)
    )


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="Please, Make Sure To Set Your Wallet Address",
        reply_markup=ReplyKeyboardMarkup(MAIN_BUTTON)
    )
    return MAIN


