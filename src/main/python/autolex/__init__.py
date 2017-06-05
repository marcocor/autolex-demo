from astroid.__pkginfo__ import author
import cgi
from collections import Counter
import logging
from math import log, exp
import math
from numpy import clip, mean
import os
import pyfscache
import re
from scipy import stats
import sqlite3
from sqlitedict import SqliteDict
import string
import time


__all__ = []


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Autolex(object):

    def __init__(self, storage_db, erase=False):
        if erase and os.path.isfile(storage_db):
            os.remove(storage_db)
        self.db_connection = sqlite3.connect(storage_db)
        self.db_connection.row_factory = dict_factory
        self.db = self.db_connection.cursor()
        self.db.execute('''CREATE TABLE IF NOT EXISTS verdicts (
            verdict_key INTEGER PRIMARY KEY AUTOINCREMENT,
            title,
            description,
            authority,
            verdict_id,
            date)
            ''')
        self.db.execute('''CREATE TABLE IF NOT EXISTS actus_reus (
            actus_reus_key INTEGER PRIMARY KEY AUTOINCREMENT,
            verdict,
            description,
            law,
            FOREIGN KEY(verdict) REFERENCES verdicts(verdict_key))
            ''')
        self.db.execute('''CREATE TABLE IF NOT EXISTS natural_expressions (
            verdict,
            expression,
            FOREIGN KEY(verdict) REFERENCES verdicts(verdict_key))
            ''')

    def add_verdict(self, title, authority, verdict_id, date):
        self.db.execute('''INSERT INTO verdicts(title, description, authority, verdict_id, date)
            VALUES (?, NULL, ?, ?, STRFTIME("%Y-%m-%d", ?))''',
            (title, authority, verdict_id, date))
        verdict_key = self.db.lastrowid
        self.db_connection.commit()
        return verdict_key
        
    def set_verdict_info(self, verdict_key, title, authority, verdict_id, date):
        self.db.execute('''UPDATE verdicts
            SET title = ?, authority = ?, verdict_id = ?, date = STRFTIME("%Y-%m-%d", ?)
            WHERE verdict_key = ?''',
            (title, authority, verdict_id, date, verdict_key))
        self.db_connection.commit()
        
    def set_verdict_description(self, verdict_key, description):
        self.db.execute('UPDATE verdicts SET description = ? WHERE verdict_key = ?',
                        (description, verdict_key))
        self.db_connection.commit()

    def add_actus_reus(self, verdict_key, description, law):
        self.db.execute('INSERT INTO actus_reus(verdict, description, law) VALUES (?, ?, ?)',
                        (verdict_key, description, law))
        self.db_connection.commit()

    def delete_actus_reus(self, actus_reus_key):
        return self.db.execute('''DELETE
            FROM actus_reus
            WHERE actus_reus_key = ?''', (actus_reus_key,)).fetchall()

    def add_natural_expression(self, verdict_key, expression):
        self.db.execute('INSERT INTO natural_expressions VALUES (?, ?)', (verdict_key, expression))
        self.db_connection.commit()

    def get_verdict_info(self, verdict_key):
        return self.db.execute('''SELECT verdict_key, title, authority, verdict_id, date, description
            FROM verdicts
            WHERE verdict_key = ?''', (verdict_key,)).fetchone()

    def get_actus_reus(self, verdict_key):
        return self.db.execute('''SELECT *
            FROM actus_reus
            WHERE verdict = ?''', (verdict_key,)).fetchall()

    def get_all_verdicts(self):
        return self.db.execute('SELECT verdict_key, title, authority, verdict_id, date FROM verdicts').fetchall()
