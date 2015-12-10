SUPPORTED_CHAINS = [ "BTC", "XTN", "NMC", "LTC", "XLT", "DOGE", "XDN" ]


# Network magic values
MAGIC_VALUES = {
	"BTC": 0xD9B4BEF9,
	"XTN": 0x0709110B,
	"NMC": 0xFEB4BEF9,
	"LTC": 0xFBC0B6DB,
	"XLT": 0xDCB7C1FC,
	"DOGE": 0xC0C0C0C0,
	"XDN": 0xDCB7C1FC
}

# Genesis blocks
GENESIS = {
	"BTC": 0x000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f,
	"XTN": 0x000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943,
	"NMC": 0x000000000062b72c5e2ceb45fbc8587e807c155b0da735e6483dfba2f0a9c770,
	"LTC": 0x12a765e31ffd4059bada1e25190f6e98c99d9714d334efa41a195a7e7e04bfe2,
	"XLT": 0xf5ae71e26c74beacc88382716aced69cddf3dffff24f384e1808905e0188f68f,
	"DOGE": 0x1a91e3dace36e2be3bf030a65679fe821aa1d6ef92e7c9902eb318182c355691,
	"XDN": 0xbb0a78264637406b6360aad926284d544d7049f45189db5664f3c4d07350559e
}

# Default ports
PORTS = {
	"BTC": 8333,
	"XTN": 18333,
	"NMC": 8334,
	"LTC": 9333,
	"XLT": 19333,
	"DOGE": 22556,
	"XDN": 44556
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
	"XLT": [ "testnet-seed.litecointools.com", "testnet-seed.ltc.xurious.com", "dnsseed.wemine-testnet.com" ],
	"NMC": [ "namecoindnsseed.digi-masters.com", "namecoindnsseed.digi-masters.uk", "seed.namecoin.domob.eu", "nmc.seed.quisquis.de", "dnsseed.namecoin.webbtc.com" ],
	"DOGE": [ "seed.dogecoin.com", "seed.multidoge.org", "seed2.multidoge.org", "seed.doger.dogecoin.com" ],
	"XDN": [ "testseed.jrn.me.uk" ]
}




class UnsupportedChainException (Exception):
	pass

def isSupported (chain):
	return (chain.upper () in SUPPORTED_CHAINS)
