#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 17:53:50 2023

@author: snipermonke01
"""


import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as image
from matplotlib.ticker import FormatStrFormatter

raw_data = json.load(open('data.json'))

dglp_df = pd.DataFrame(raw_data['data']['dGLP']).set_index('dayStartUnix')
btc_df = pd.DataFrame(raw_data['data']['btc']).set_index('dayStartUnix')
eth_df = pd.DataFrame(raw_data['data']['eth']).set_index('dayStartUnix')
jUSDC_df = pd.DataFrame(raw_data['data']['jUSDC']).set_index('dayStartUnix')
plsGLP_df = pd.DataFrame(raw_data['data']['plsGLP']).set_index('dayStartUnix')
ptGLP_df = pd.DataFrame(raw_data['data']['ptGLP']).set_index('dayStartUnix')
mGLP_df = pd.DataFrame(raw_data['data']['mGLP']).set_index('dayStartUnix')
arb_df = pd.DataFrame(raw_data['data']['arb']).set_index('dayStartUnix')
dai_df = pd.DataFrame(raw_data['data']['dai']).set_index('dayStartUnix')
link_df = pd.DataFrame(raw_data['data']['link']).set_index('dayStartUnix')
usdc_df = pd.DataFrame(raw_data['data']['USDCe']).set_index('dayStartUnix')
usdt_df = pd.DataFrame(raw_data['data']['USDT']).set_index('dayStartUnix')

dglp_liq = dglp_df['supplyLiquidityUSD'].astype(float)/1000000
btc_liq = btc_df['supplyLiquidityUSD'].astype(float)/1000000
eth_liq = eth_df['supplyLiquidityUSD'].astype(float)/1000000
jUSDC_liq = jUSDC_df['supplyLiquidityUSD'].astype(float)/1000000
plsGLP_liq = plsGLP_df['supplyLiquidityUSD'].astype(float)/1000000
ptGLP_liq = ptGLP_df['supplyLiquidityUSD'].astype(float)/1000000
mGLP_liq = mGLP_df['supplyLiquidityUSD'].astype(float)/1000000
arb_liq = arb_df['supplyLiquidityUSD'].astype(float)/1000000
dai_liq = dai_df['supplyLiquidityUSD'].astype(float)/1000000
link_liq = link_df['supplyLiquidityUSD'].astype(float)/1000000
usdc_liq = usdc_df['supplyLiquidityUSD'].astype(float)/1000000
usdt_liq = usdt_df['supplyLiquidityUSD'].astype(float)/1000000

df_final = pd.concat([dglp_liq,
                      btc_liq,
                      eth_liq,
                      jUSDC_liq,
                      plsGLP_liq,
                      ptGLP_liq,
                      mGLP_liq,
                      arb_liq,
                      dai_liq,
                      link_liq,
                      usdc_liq,
                      usdt_liq
                      ], axis=1, sort=True)

df_final.columns = ['dGLP', 'BTC', 'ETH', 'jUSDC', 'plvGLP',
                    'ptGLP 2024', 'mGLP', 'ARB', 'DAI', 'LINK', 'USDC.e', 'USDT']
df_final.index = pd.to_datetime(df_final.index, unit='s')

dglp_borrow = dglp_df['borrowLiquidityUSD'].astype(float)/1000000
btc_borrow = btc_df['borrowLiquidityUSD'].astype(float)/1000000
eth_borrow = eth_df['borrowLiquidityUSD'].astype(float)/1000000
jUSDC_borrow = jUSDC_df['borrowLiquidityUSD'].astype(float)/1000000
plsGLP_borrow = plsGLP_df['borrowLiquidityUSD'].astype(float)/1000000
ptGLP_borrow = ptGLP_df['borrowLiquidityUSD'].astype(float)/1000000
mGLP_borrow = mGLP_df['borrowLiquidityUSD'].astype(float)/1000000
arb_borrow = arb_df['borrowLiquidityUSD'].astype(float)/1000000
dai_borrow = dai_df['borrowLiquidityUSD'].astype(float)/1000000
link_borrow = link_df['borrowLiquidityUSD'].astype(float)/1000000
usdc_borrow = usdc_df['borrowLiquidityUSD'].astype(float)/1000000
usdt_borrow = usdt_df['borrowLiquidityUSD'].astype(float)/1000000

df_borrow_final = pd.concat([dglp_borrow,
                             btc_borrow,
                             eth_borrow,
                             jUSDC_borrow,
                             plsGLP_borrow,
                             ptGLP_borrow,
                             mGLP_borrow,
                             arb_borrow,
                             dai_borrow,
                             link_borrow,
                             usdc_borrow,
                             usdt_borrow
                             ], axis=1, sort=True)

df_borrow_final.columns = ['dGLP', 'BTC', 'ETH', 'jUSDC', 'plvGLP',
                           'ptGLP 2024', 'mGLP', 'ARB', 'DAI', 'LINK', 'USDC.e', 'USDT']
df_borrow_final.index = df_final.index


plt.style.use('dark_background')
figure, figure_axes = plt.subplots(figsize=(6, 3), dpi=600)
figure_axes.plot(np.arange(0, len(df_borrow_final), 1),
                 df_borrow_final.sum(axis=1),
                 color='r',
                 linestyle='--',
                 label='Borrowed',
                 linewidth=1)
df_final.plot.bar(ax=figure_axes,
                  stacked=True)

figure_axes.set_xticks(ticks=np.arange(0, len(df_final[1::]), 1)[::30])
labels = [label.strftime("%b-%Y") for label in df_final.index[1::30]]
figure_axes.set_xticklabels(labels=labels)
figure_axes.tick_params(labelrotation=45,
                        labelsize=6)
figure_axes.yaxis.set_major_formatter(FormatStrFormatter('$%1dm'))
figure_axes.set_ylabel(ylabel='Supply Liquidity ($m)',
                       size=6)
figure_axes.set_xlabel(xlabel='Date',
                       size=6)

figure_axes.set_title("Dolomite Supply & Borrow Total",
                      ha='left',
                      loc='left',
                      fontsize=8)

im = image.imread('logo.png')
figure.figimage(im,
                1400,
                1000,
                zorder=3,
                alpha=.5)

plt.legend(ncol=2,
           loc="upper left",
           prop={'size': 5})
