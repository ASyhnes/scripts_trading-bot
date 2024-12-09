import logging
import asyncio
from datetime import datetime
import subprocess
import pandas as pd
import ta
from pydantic import BaseModel
import ccxt.async_support as ccxt

# Configuration de logging
log_file = "/home/syhnes/Bot_hyperliquid/bot_log.txt"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Installer les dépendances au besoin
subprocess.run("pip install ccxt pandas pydantic ta", shell=True, check=True)

# Modèle de position
class Position(BaseModel):
    pair: str
    side: str
    size: float
    usd_size: float
    entry_price: float
    current_price: float
    unrealized_pnl: float
    liquidation_price: float | None = None
    margin_mode: str
    leverage: int
    hedge_mode: bool

# Classe principale pour Hyperliquid
class PerpHyperliquid:
    def __init__(self, public_adress=None, private_key=None):
        self.public_adress = public_adress
        self.private_key = private_key
        self._session = ccxt.hyperliquid({"walletAddress": public_adress, "privateKey": private_key})
        self.market = {}

    async def load_markets(self):
        data = await self._session.publicPostInfo(params={"type": "metaAndAssetCtxs"})
        for market in data[0]["universe"]:
            self.market[market["name"] + "/USD"] = market

    async def get_open_positions(self, pairs=[]):
        data = await self._session.publicPostInfo(params={"type": "clearinghouseState", "user": self.public_adress})
        positions_data = data["assetPositions"]
        positions = []
        for position_data in positions_data:
            position = position_data["position"]
            liquidation_price = position.get("liquidationPx", None)
            if liquidation_price is not None:
                liquidation_price = float(liquidation_price)
            positions.append(Position(
                pair=position["coin"] + "/USD",
                side="long" if float(position["szi"]) > 0 else "short",
                size=abs(float(position["szi"])),
                usd_size=float(position["positionValue"]),
                entry_price=float(position["entryPx"]),
                current_price=float(position["positionValue"]) / abs(float(position["szi"])),
                unrealized_pnl=float(position["unrealizedPnl"]),
                liquidation_price=liquidation_price,
                margin_mode=position["leverage"]["type"],
                leverage=int(position["leverage"]["value"]),
                hedge_mode=position_data["type"] != "oneWay",
            ))
        return positions

    async def place_order(self, pair, side, price, size, type="limit", reduce=False):
        try:
            await self._session.create_order(pair, type, side, size, price, {'reduce': reduce})
        except Exception as e:
            logging.error(f"Erreur lors du placement de l'ordre : {e}")
            return None
        return {"pair": pair, "side": side, "price": price, "size": size, "type": type, "reduce": reduce}

    async def close(self):
        await self._session.close()

# Script principal
async def main():
    logging.info("Début de l'exécution du script.")
    try:
        # Configuration de l'API
        ex = PerpHyperliquid(
            public_adress="0x97E2064BE52864d477644D596b7953bF631246f4",
            private_key="0x008d93c6bb4792cd69e380122722fbc067c4a9003e09a2908cf9fc69614b4f6e"
        )

        await ex.load_markets()

        # Charger les données du marché
        df = await ex._session.fetch_ohlcv("BTC/USD", timeframe="4h", limit=100)
        df = pd.DataFrame(df, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["rsi"] = ta.momentum.rsi(df["close"], 14)

        usd = {"total": 1000}  # Simule une balance pour tester
        positions = await ex.get_open_positions(pairs=["BTC/USD"])

        btc_price = df.iloc[-1]["close"]
        rsi = df.iloc[-2]["rsi"]

        if len(positions) > 0:
            if rsi < 60:
                order = await ex.place_order("BTC/USD", "sell", None, positions[0].size, "market", True)
                logging.info(f"Ordre passé : {order}")
            else:
                logging.info("Pas d'ordre : RSI >= 60.")
        elif len(positions) == 0:
            if rsi > 60:
                order = await ex.place_order("BTC/USD", "buy", None, (usd["total"] * 0.15) / btc_price, "market", False)
                logging.info(f"Ordre passé : {order}")
            else:
                logging.info("Pas d'ordre : RSI <= 60.")

        logging.info("Exécution terminée avec succès.")
    except Exception as e:
        logging.error(f"Erreur lors de l'exécution : {e}")
    finally:
        await ex.close()

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
