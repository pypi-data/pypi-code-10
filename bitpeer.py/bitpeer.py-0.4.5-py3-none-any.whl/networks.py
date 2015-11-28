SUPPORTED_CHAINS = [ "BTC", "XTN", "NMC", "LTC", "XLT" ]


# Network magic values
MAGIC_VALUES = {
    "BTC": 0xD9B4BEF9,
    "XTN": 0x0709110B,
    "NMC": 0xFEB4BEF9,
    "LTC": 0xFBC0B6DB,
    "XLT": 0xDCB7C1FC
}


GENESIS = {
	"BTC": 0x000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f,
    "XTN": 0x000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943,
    "NMC": '',
    "LTC": '',
    "XLT": ''
}

PORTS = {
	"BTC": 8333,
    "XTN": 18333,
    "NMC": 0,
    "LTC": 0,
    "XLT": 19333
}

# Almost available peers
PEERS = {
    "BTC": [("bitcoin.sipa.be", 8333)],
    "XTN": [],
    "NMC": [],
    "LTC": [],
    "XLT": [("51.254.215.160", 19333)]
}


# Seed servers
SEEDS = {
    "BTC": [ "seed.bitcoin.sipa.be", "dnsseed.bluematt.me", "dnsseed.bitcoin.dashjr.org", "seed.bitcoinstats.com", "bitseed.xf2.org"],
    "XTN": [ "testnet-seed.alexykot.me", "testnet-seed.bitcoin.petertodd.org", "testnet-seed.bluematt.me", "testnet-seed.bitcoin.schildbach.de" ],
    "LTC": [ "dnsseed.litecointools.com", "dnsseed.litecoinpool.org", "dnsseed.ltc.xurious.com", "dnsseed.koin-project.com", "dnsseed.weminemnc.com" ],
    "XLT": [ "testnet-seed.litecointools.com", "testnet-seed.ltc.xurious.com", "dnsseed.wemine-testnet.com" ]
}



class UnsupportedChainException (Exception):
    pass

def isSupported (chain):
    return (chain.upper () in SUPPORTED_CHAINS)
