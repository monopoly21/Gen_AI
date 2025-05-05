import json
from datamodel import OrderDepth, TradingState, Order
from typing import List

class Trader:

    def run(self, state: TradingState):
    # Load persistent data for SQUID_INK's moving average calculations
        try:
            data = json.loads(state.traderData)
        except Exception:
            data = {}
        if "squid_prices" not in data:
            data["squid_prices"] = []

        result = {}
        # Known position limits
        pos_limits = {
            "RAINFOREST_RESIN": 50,
            "KELP": 50,
            "SQUID_INK": 50
        }

        for product, order_depth in state.order_depths.items():
            orders: List[Order] = []
            current_pos = state.position.get(product, 0)

            # Determine best bid and ask (with quantities)
            best_bid, best_bid_qty = None, 0
            best_ask, best_ask_qty = None, 0
            if order_depth.buy_orders:
                best_bid = max(order_depth.buy_orders.keys())
                best_bid_qty = order_depth.buy_orders[best_bid]
            if order_depth.sell_orders:
                best_ask = min(order_depth.sell_orders.keys())
                best_ask_qty = order_depth.sell_orders[best_ask]  # Note: negative quantity

            # ================================
            # RAINFOREST_RESIN: Stable but high-value asset
            # ================================
            if product == "RAINFOREST_RESIN":
                # Calculate mid-price from the order book (fallback to 10000 if needed)
                if best_bid is not None and best_ask is not None:
                    mid_price = (best_bid + best_ask) / 2
                elif best_bid is not None:
                    mid_price = best_bid
                elif best_ask is not None:
                    mid_price = best_ask
                else:
                    mid_price = 10000
                fair_value = mid_price

                # Check that spread is sufficient (e.g., at least 5 units for profit)
                if best_bid is not None and best_ask is not None and (best_ask - best_bid) >= 5:
                    # If the ask is below fair_value and room exists to go long, buy.
                    if best_ask < fair_value:
                        qty_possible = pos_limits[product] - current_pos
                        qty_to_buy = min(-best_ask_qty, qty_possible)
                        if qty_to_buy > 0:
                            orders.append(Order(product, best_ask, qty_to_buy))
                    # If bid is above fair_value and room exists to go short, sell.
                    if best_bid > fair_value:
                        qty_possible = pos_limits[product] + current_pos
                        qty_to_sell = min(best_bid_qty, qty_possible)
                        if qty_to_sell > 0:
                            orders.append(Order(product, best_bid, -qty_to_sell))

            # ================================
            # KELP: Moderately volatile asset; adaptive mid-price trading
            # ================================
            elif product == "KELP":
                if best_bid is not None and best_ask is not None:
                    mid_price = (best_bid + best_ask) / 2
                else:
                    mid_price = 2030  # Fallback value
                fair_value = mid_price
                max_trade_size = 10

                if best_ask is not None and best_ask < fair_value:
                    qty_possible = pos_limits[product] - current_pos
                    qty_to_buy = min(-best_ask_qty, max_trade_size, qty_possible)
                    if qty_to_buy > 0:
                        orders.append(Order(product, best_ask, qty_to_buy))
                if best_bid is not None and best_bid > fair_value:
                    qty_possible = pos_limits[product] + current_pos
                    qty_to_sell = min(best_bid_qty, max_trade_size, qty_possible)
                    if qty_to_sell > 0:
                        orders.append(Order(product, best_bid, -qty_to_sell))

            # ================================
            # SQUID_INK: Highly volatile; use moving average for mean-reversion
            # ================================
            elif product == "SQUID_INK":
                if best_bid is not None and best_ask is not None:
                    mid_price = (best_bid + best_ask) / 2
                elif best_bid is not None:
                    mid_price = best_bid
                elif best_ask is not None:
                    mid_price = best_ask
                else:
                    mid_price = 1960  # Fallback based on observed values

                # Update moving average using last 10 observations
                data["squid_prices"].append(mid_price)
                if len(data["squid_prices"]) > 10:
                    data["squid_prices"] = data["squid_prices"][-10:]
                moving_average = sum(data["squid_prices"]) / len(data["squid_prices"])
                # Use a threshold that could be tuned; here 2% deviation triggers trade
                threshold = 0.02 * moving_average

                if best_ask is not None and (moving_average - best_ask) > threshold:
                    qty_possible = pos_limits[product] - current_pos
                    trade_size = min(-best_ask_qty, max(1, pos_limits[product] // 2), qty_possible)
                    if trade_size > 0:
                        orders.append(Order(product, best_ask, trade_size))
                if best_bid is not None and (best_bid - moving_average) > threshold:
                    qty_possible = pos_limits[product] + current_pos
                    trade_size = min(best_bid_qty, max(1, pos_limits[product] // 2), qty_possible)
                    if trade_size > 0:
                        orders.append(Order(product, best_bid, -trade_size))

            result[product] = orders

        conversions = 0  # No conversion actions in this round
        traderData = json.dumps(data)
        return result, conversions, traderData
