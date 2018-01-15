import discord
from discord.ext import commands
from os import path
import json
import pymysql

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "..", "..", "config.json"))
with open(filepath, 'r') as f:
    config = json.load(f)


def check_disabled(guildid):
    db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                         charset='utf8mb4')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM opts WHERE guildid = {guildid}')
    results = cur.fetchall()
    if results:
        for row in results:
            channels = row[1]
        db.close()
        if channels:
            return channels
        else:
            return ""
    else:
        db.close()
        return ""


def get_vote_channel(guildid):
    db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                         charset='utf8mb4')
    cur = db.cursor()
    cur.execute(f'SELECT guildid,votechannel FROM opts WHERE guildid = {guildid}')
    results = cur.fetchall()
    if results:
        channel = None
        for row in results:
            channel = row[1]
        db.close()
        if channel:
            return channel


def get_description(userid):
    db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                         charset='utf8mb4')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM profiles WHERE userid = {userid}')
    results = cur.fetchall()
    if results:
        for row in results:
            desc = row[1]
        db.close()
        if desc:
            return desc
        else:
            return "No description set."


def get_balance(userid):
    db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                         charset='utf8mb4')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM profiles WHERE userid = {userid}')
    results = cur.fetchall()
    if results:
        for row in results:
            bal = row[2]
        db.close()
        return bal
    else:
        db.close()
        return 0


def get_married(userid):
    db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                         charset='utf8mb4')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM profiles WHERE userid = {userid}')
    results = cur.fetchall()
    if results:
        for row in results:
            marriage = row[3]
        db.close()
        return marriage


def get_reps(userid):
    db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                         charset='utf8mb4')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM profiles WHERE userid = {userid}')
    results = cur.fetchall()
    if results:
        for row in results:
            reps = row[4]
        db.close()
        if reps is not None:
            return reps
        else:
            return 0
    else:
        db.close()
        return 0


def get_log_channel(guildid):
    db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                         charset='utf8mb4')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM opts WHERE guildid = {guildid}')
    results = cur.fetchall()
    if results:
        for row in results:
            logchannel = row[2]
        db.close()
        return logchannel


def get_modlog_channel(guildid):
    db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                         charset='utf8mb4')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM opts WHERE guildid = {guildid}')
    results = cur.fetchall()
    if results:
        for row in results:
            modlogchannel = row[3]
        db.close()
        return modlogchannel


def get_mute_role(guildid):
    db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                         charset='utf8mb4')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM opts WHERE guildid = {guildid}')
    results = cur.fetchall()
    if results:
        for row in results:
            muterole = row[4]
        db.close()
        return muterole


def get_join_message(guildid):
    db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                         charset='utf8mb4')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM opts WHERE guildid = {guildid}')
    results = cur.fetchall()
    if results:
        for row in results:
            joinmessage = row[5]
        db.close()
        return joinmessage


def get_leave_message(guildid):
    db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                         charset='utf8mb4')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM opts WHERE guildid = {guildid}')
    results = cur.fetchall()
    if results:
        for row in results:
            leavemessage = row[6]
        db.close()
        return leavemessage


def get_welcome_channel(guildid):
    db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                         charset='utf8mb4')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM opts WHERE guildid = {guildid}')
    results = cur.fetchall()
    if results:
        for row in results:
            welcome = row[7]
        db.close()
        return welcome
