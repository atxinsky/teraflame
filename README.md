# BTC MACD ATR Trading Strategy

This project implements a Bitcoin trading strategy using the Freqtrade framework. The strategy is based on MACD signals combined with EMA confirmation and ATR-based exit conditions.

## Strategy Overview

### Entry Conditions
- Price must be above the EMA144
- MACD must be above the zero line
- MACD must be in a golden cross state (MACD line crosses above signal line)

### Exit Conditions
- MACD death cross (MACD line crosses below signal line)
- ATR-based take profit hit
- ATR-based stop loss hit

### Position Sizing
- Uses 30% of capital for each trade (adjustable)
- Uses 6x leverage (adjustable)
- Can use compound interest model if capital grows beyond initial amount

### Risk Management
- Dynamic ATR-based take profit and stop loss
- Isolated margin mode for futures trading
- Customizable leverage and position sizing

## Setup Instructions

### Prerequisites
- Python 3.8+
- Freqtrade installed (`pip install freqtrade`)

### Installation

1. Clone this repository
2. Create necessary directories:
   ```
   mkdir -p user_data/data/csv
   mkdir -p user_data/strategies
   ```
3. Copy the strategy file:
   ```
   cp btc_macd_atr_strategy.py user_data/strategies/
