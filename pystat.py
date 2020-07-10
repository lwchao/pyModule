#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   flow_test.py
@Version :   1.0
@Author  :   liuwenchao
@Time    :   2020/07/09 16:36:08
'''

import os
import sys
import time
import commands
import curses
import random
import signal

STAT_CUR = {}
STAT_SAV = {}

PERIOD = 5

RX_DROPS_NIC='rx_drops_nic'
VLAN_DROP='vlan_drop'
LOOPBACK_DROP='loopback_drop'
MBX_TX_DROPPED='mbx_tx_dropped'
NODESC_DROP='nodesc_drop'
RX_DROPPED='rx_dropped'

stdscr = curses.initscr()

def init_env():
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.box()

def destroy_env():
    stdscr.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()

def _exit(signum, frame):
    destroy_env()
    print("normal exit!")
    sys.exit()

signal.signal(signal.SIGINT, _exit)
signal.signal(signal.SIGTERM, _exit)



def creatEthList():
    ethlist = []

    for i in range(7, 11):
        if i == 4:
            continue
        ethlist.append('eth{}'.format(i))

    return ethlist

def getOutput(eth):
    out = commands.getoutput("ethtool -S {} | grep drop".format(eth))

    # 'rx_drops_nic': 153, 'vlan_drop': 0, 'loopback_drop': 0, 'mbx_tx_dropped': 3, 'nodesc_drop': 153, 'rx_dropped': 153
    ethcache = dict()

    out = out.split('\n')
    for o in out:
        d = o.split(':')
        if not d:
            continue
        ethcache[d[0].strip()] = int(d[1].strip())
    return ethcache

def getFlowStat(curr, prev, save):
    return "{}/{}/{}/{}".format(curr, (curr-prev)/PERIOD, curr-save, save)

def cleanData(e, data):
    d = STAT_CUR.get(e)
    if not d:
        STAT_CUR[e] = data
        STAT_SAV[e] = data
        return ''

    d1 = getFlowStat(data['rx_drops_nic'], d['rx_drops_nic'], STAT_SAV[e]['rx_drops_nic'])
    d2 = getFlowStat(data['vlan_drop'], d['vlan_drop'], STAT_SAV[e]['vlan_drop'])
    d3 = getFlowStat(data['loopback_drop'], d['loopback_drop'], STAT_SAV[e]['loopback_drop'])
    d4 = getFlowStat(data['mbx_tx_dropped'], d['mbx_tx_dropped'], STAT_SAV[e]['mbx_tx_dropped'])
    d5 = getFlowStat(data['nodesc_drop'], d['nodesc_drop'], STAT_SAV[e]['nodesc_drop'])
    d6 = getFlowStat(data['rx_dropped'], d['rx_dropped'], STAT_SAV[e]['rx_dropped'])

    STAT_CUR[e] = data
    stdscr.addstr("%10s%20s%20s%20s%20s%20s%20s\n" % (e, d1, d2, d3, d4, d5, d6))

def getEthStatistics(eth):

    stdscr.move(1,0)
    stdscr.addstr("\tEth Statistics\n")
    stdscr.addstr("\tCurrent/Speed/Sum/Initial\n")
    stdscr.addstr("\tPerid: {}s\n".format(PERIOD))
    stdscr.addstr("\n")
    stdscr.addstr("%10s%20s%20s%20s%20s%20s%20s" % ("eth", "rx_drops_nic", "vlan_drop", "loopback_drop", "mbx_tx_dropped", "nodesc_drop", "rx_dropped"))
    stdscr.refresh()
    while 1:
        for e in eth:
            out = getOutput(e)
            cleanData(e, out)

        stdscr.move(7, 0)
        stdscr.refresh()
        time.sleep(PERIOD)

def main():
    init_env()
    eth = creatEthList()
    getEthStatistics(eth)
    destroy_env()

if __name__ == "__main__":
    main()
