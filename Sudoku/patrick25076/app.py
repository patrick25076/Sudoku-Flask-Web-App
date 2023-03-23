import os
from flask import Flask, flash, redirect, render_template, request, session,jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import random
import numpy as np
import webbrowser



app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
board3 =[  [9, 6, 3, 1, 7, 4, 2, 5, 8],
  [1, 7, 8, 3, 2, 5, 6, 4, 9],
  [2, 5, 4, 6, 8, 9, 7, 3, 1],
  [8, 2, 1, 4, 3, 7, 5, 9, 6],
  [4, 9, 6, 8, 5, 2, 3, 1, 7],
  [7, 3, 5, 9, 6, 1, 8, 2, 4],
  [5, 8, 9, 7, 1, 3, 4, 6, 2],
  [3, 1, 7, 2, 4, 6, 9, 8, 5],
  [6, 4, 2, 5, 9, 8, 1, 7, 3]
    ]
matrices = [np.matrix(board), np.matrix(board3)]

def check(board):
    for i in range(9):
        for j in range(9):
            if board[i][j]==0:
                return False
    return True
def isvalid(board,row,col,num):
    for x in range(9):
        if board[row][x]==num:
            return False
        if board[x][col]==num:
            return False
    startcol= col-col%3
    startrow=row-row%3
    for x in range(3):
        for y in range(3):
            if board[startrow+x][startcol+y]==num:
                return False
    return True

def randomize(board):
    for i in range(random.randint(2,5)):
        for j in range(random.randint(1,6)):
            val=random.randint(1,9)
            if isvalid(board,i,j,val):
                board[i][j]=val


def solve(board,row,col):
    if col==9:
        if row==8:
            return True
        col=0
        row+=1
    if board[row][col]>0:
        return solve(board,row,col+1)
    for x in range(1,10):
        if isvalid(board,row,col,x):
            board[row][col]=x
            if solve(board,row,col+1):
                return True
        board[row][col]=0
    return False

def modify(board):
    sudoku={}
    c=0
    for i in range(9):
        for j in range(9):
            sudoku[c]=board[i][j]
            c=c+1
    return sudoku
@app.route('/generatesudoku' , methods=['POST'])

def create(board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]):
    for matrix in matrices:
        array1 = np.array(board)
        array2 = np.array(matrix)
        if np.array_equal(array1, array2):
            empty_board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
            return create(empty_board)
    randomize(board)
    solve(board,0,0)
    if check(board)==False:
        exception=modify(board3)
        return jsonify(exception)
    matrices.append(np.matrix(board))
    board4=modify(board)
    return jsonify(board4)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/play")
def play():
    return render_template("play.html",board=board)

@app.route("/rules")
def rules():
    return render_template("rules.html")


if __name__ == "__main__":
    app.run()