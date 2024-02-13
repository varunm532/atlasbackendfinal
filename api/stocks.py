import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from model.users import User, Stocks
from auth_middleware1 import token_required1
import sqlite3
from __init__ import app, db, cors, dbURI




from model.users import Stocks,User,Transactions

stocks_api = Blueprint('stocks_api', __name__,
                   url_prefix='/api/stocks')
api = Api(stocks_api)

class StocksAPI(Resource):
    class _Displaystock(Resource):
        #@token_required1("Admin")
        def get(self):
            stocks = Stocks.query.all()
            json_ready = [stock.read() for stock in stocks]
            return jsonify(json_ready)
    class _Transactionsdisplay(Resource):
        #@token_required1("Admin")
        
        def get(self):
            transaction = Transactions.query.all()
            json_ready = [transactions.read() for transactions in transaction]
            return jsonify(json_ready)
    #class _Transaction(Resource):
    #    def post(self):
    #        conn=sqlite3.connect('instance/volumes/sqlite.db')
    #        cur=conn.cursor()
    #        body = request.get_json()
    #        quantity = body.get('newquantity')
    #        symbol = body.get('symbol')
    #        update_query = "UPDATE stocks SET _quantity = ? WHERE _symbol = ?"
    #        #updatedstocks = Stocks.read() in symbol - symbols
    #        #Stocks.update(update_query, (quantity, symbol))
    #        cur.execute(update_query,(quantity,symbol))
    #        conn.commit()
    #        cur.close()
    class _Transaction1(Resource):
        def post(self):
            body = request.get_json()
            quantitytobuy = body.get('buyquantity')
            uid = body.get('uid')
            symbol = body.get('symbol')
            ##orginalquantity = body.get('avaliablequantity')
            newquantity = body.get('newquantity')
            transactiontype= 'buy'
            transactiondate = datetime.strptime(transactiondate, '%Y-%m-%d %H:%M:%S').date()
            ## update for stocks table to change the amound of stocks left
            stocks = Stocks.query.all()
            json_ready = [stock.read() for stock in stocks]
            list1 = [item for item in json_ready if item.get('symbol') == symbol]
            users = User.query.all()
            json_ready_user = [user.read() for user in users]
            list2 = [item for item in json_ready_user if item.get('uid') == uid]
            usermoney = list2[0]['stockmoney']
            currentstockmoney = list1[0]['sheesh']
            if (usermoney > currentstockmoney*quantitytobuy):
                ## updates stock quantity in stocks table
                tableid = Stocks.query.get(tableid)
                tableid.update(quantity=newquantity )
                db.session.commit()
                ## updates user money
                tableid_user = list2[0]['id']
                updatedusermoney = usermoney - currentstockmoney*quantitytobuy
                tableid_user.update(stockmoney= updatedusermoney )
                db.session.commit()
                ## creates log for transaction
                transactionamount = currentstockmoney*quantitytobuy
                ta = Transactions(uid=uid, symbol=symbol,transactiontype=transactiontype, quantity=quantitytobuy, transaction_amount=transactionamount, transaction_date=transactiondate )
                ta.create()   
                db.session.commit()
            else:
                return jsonify({'error': 'Insufficient funds'}), 400
                
            ##This is test.
            ##print("this is list1")
            ##print(str(list1[0]['quantity']))
            ##tableid = list1[0]['id']
            ##tableid = Stocks.query.get(tableid)
            ##tableid.update(quantity=newquantity )
            ##db.session.commit()
            ##
            ###chaning the total stock money
            ##users = User.query.all()
            ##json_ready_user = [user.read() for user in users]
            ##list2 = [item for item in json_ready_user if item.get('uid') == uid]
            ##tableid_user = list2[0]['id']
            ##tableid_user.update(stockmoney=newstockmoney)
            ##db.session.commit()
            ##
            ###creating transaction log
            ##ta = Transactions(uid=uid, symbol=symbol,transactiontype=transactiontype, quantity=oldquantity, transaction_amount=transactionamount, transaction_date=transactiondate )
            ##ta.create()   
            ##db.session.commit()
    class _Transactionsdisplayuser(Resource):
        #@token_required1("Admin")
        def post(self):
            body =request.get_json()
            uid = body.get('uid')
            
        def get(self):
            transaction = Transactions.query.all()
            json_ready = [transactions.read() for transactions in transaction]
            return jsonify(item for item in json_ready if item.get('uid') == uid)         
            

            
            
            
        
    api.add_resource(_Displaystock, '/stock/display')
    api.add_resource(_Transactionsdisplay, '/transaction/displayadmin')
    api.add_resource(_Transactionsdisplayuser, '/transaction/display')
    api.add_resource(_Transaction1, '/transaction')


            
        
    
        
        

