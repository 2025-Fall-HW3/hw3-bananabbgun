"""
Package Import
"""
import argparse
import warnings

import pandas as pd
import quantstats as qs
import yfinance as yf

"""
Project Setup
"""
warnings.simplefilter(action="ignore", category=FutureWarning)

assets = [
    "SPY",
    "XLB",
    "XLC",
    "XLE",
    "XLF",
    "XLI",
    "XLK",
    "XLP",
    "XLRE",
    "XLU",
    "XLV",
    "XLY",
]

Bdf = pd.DataFrame()
for asset in assets:
    raw = yf.download(asset, start="2012-01-01", end="2024-04-01", auto_adjust=False)
    Bdf[asset] = raw["Adj Close"]

df = Bdf.loc["2019-01-01":"2024-04-01"]
Bdf.index.name = "Date"
Bdf.columns.name = "Symbol"
df.index.name = "Date"
df.columns.name = "Symbol"


class MyPortfolio:
    """
    Constant allocation: fully invest in XLK (technology sector) each rebalance.
    """

    def __init__(self, price, exclude, lookback=90, gamma=0.0, eps=1e-6):
        self.price = price
        self.returns = price.pct_change().fillna(0)
        self.exclude = exclude

    def calculate_weights(self):
        assets = self.price.columns[self.price.columns != self.exclude]
        self.portfolio_weights = pd.DataFrame(
            0.0, index=self.price.index, columns=self.price.columns
        )
        if "XLK" in assets:
            self.portfolio_weights["XLK"] = 1.0
        else:
            weight = 1.0 / len(assets)
            for asset in assets:
                self.portfolio_weights[asset] = weight
        self.portfolio_weights[self.exclude] = 0.0

    def calculate_portfolio_returns(self):
        if not hasattr(self, "portfolio_weights"):
            self.calculate_weights()
        self.portfolio_returns = self.returns.copy()
        assets = self.price.columns[self.price.columns != self.exclude]
        self.portfolio_returns["Portfolio"] = (
            self.portfolio_returns[assets]
            .mul(self.portfolio_weights[assets])
            .sum(axis=1)
        )

    def get_results(self):
        if not hasattr(self, "portfolio_returns"):
            self.calculate_portfolio_returns()
        return self.portfolio_weights, self.portfolio_returns


if __name__ == "__main__":
    from grader_2 import AssignmentJudge

    parser = argparse.ArgumentParser(
        description="Introduction to Fintech Assignment 3 Part 2"
    )
    parser.add_argument("--score", action="append", help="Score for assignment")
    parser.add_argument("--allocation", action="append", help="Allocation for asset")
    parser.add_argument("--performance", action="append", help="Performance")
    parser.add_argument("--report", action="append", help="Report metrics")
    parser.add_argument("--cumulative", action="append", help="Cumulative result")

    args = parser.parse_args()
    judge = AssignmentJudge()
    judge.run_grading(args)
