from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
   
    #result query from history. Total quantity of every stock
    result1=db.execute("SELECT stock,symbol,sum(qty) AS quantity FROM history WHERE history.user_id=:user_id GROUP BY stock,symbol",user_id=session["user_id"])
   
    #variable to add values of all stock shares
    sum=0
   
    for i in range(len(result1)):
        
        #Remove stocks with 0 shares from the list
        if result1[i]["quantity"]==0:
            result1.remove(result1[i])
            continue
        
        #Look for current price
        quote=lookup(result1[i]["symbol"])
        
        #If an invalid stock 
        if not quote:
            return apology("Did not find {}".format(result1[i]["symbol"]))
        
        #Convert price to USD
        x=usd(quote['price']) 
        
        #New field for current price 
        result1[i]["curr"]=x
        
        #New field for value of stock
        result1[i]["value"]=quote['price']*int(result1[i]["quantity"])
        
        sum=sum+result1[i]["value"]
        
        #value in USD
        result1[i]["value"]=usd(result1[i]["value"])
        
    #retreive cash
    result2=db.execute("SELECT * FROM users WHERE id=:uid",uid=session["user_id"])
    
    #add to sum of values
    sum=sum+result2[0]["cash"]
        
    #cash in USD
    cash=usd(result2[0]["cash"])
        
    #grand total in USD
    sum=usd(sum)
    
    #pass stock details, cash and grand total
    return render_template("index.html",result1=result1,result2=cash,sum=sum)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    
    #by submitting a form
    if request.method=="POST":
        
        #current price
        quote=lookup(request.form.get("symbol"))
        
        #if price not found
        if not quote:
            return apology("Enter a valid symbol!")
        
        #total amount
        amount=int(request.form.get("qty"))*quote['price']
        
        #retrieve available cash
        result=db.execute("SELECT cash FROM users WHERE id=:id",id=session["user_id"])
        
        #if unaffordable
        if result[0]["cash"]<amount:
            return apology("You do not have sufficient cash!")
        
        #insert into log of transaction
        db.execute("INSERT INTO history (user_id, symbol, qty, price, stock) VALUES(:user_id,:symbol,:qty,:price,:name)", user_id=session["user_id"], symbol=quote['symbol'], qty=request.form.get("qty"), price=quote['price'], name=quote['name'])
        
        #deduct amount from cash
        db.execute("UPDATE users SET cash=cash-:amount WHERE id=:user_id",amount=amount,user_id=session["user_id"])
        
        return redirect(url_for("index"))
    
    #via redirect or URL
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    
    #retrieve details for current user
    result=db.execute("SELECT * FROM history WHERE user_id=:id",id=session["user_id"])
    
    #for every row
    for i in range (len(result)):
        
        #if qty is negative it is sold
        if int(result[i]["qty"])<0:
            result[i]["action"]="sold"
            result[i]["qty"]=-1*int(result[i]["qty"])
        
        #else bought
        else:
            result[i]["action"]="bought"
        
    return render_template("history.html",result=result)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required

def quote():
    """Get stock quote."""
    
    #via form submission
    if request.method=="POST":
        
        #look for current price
        quote=lookup(request.form.get("symbol"))
        
        if not quote:
            return apology("Enter a valid symbol!")
        
        #convert price to usd
        quote['price']=usd(quote['price'])
        
        #pass the stock details
        return render_template("quoted.html",symbol=quote)
    
    #via redirect or link
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    
    #via form submission
    if request.method=="POST":
        
        # username blank
        if request.form.get("username")=="":
            return apology("Missing username!")
        
        # password blank
        if request.form.get("password1")=="":
            return apology("Missing password!")
        
        # re-enter password blank   
        if request.form.get("password2")=="":
            return apology("Missing password confirmation!")
        
        # if both passwords do not match    
        if request.form.get("password1")!= request.form.get("password2"):
            return apology("Passwords do not match!")
        
        #hash the password
        hash=pwd_context.encrypt(request.form.get("password1"))
        
        #insert the user
        result=db.execute("INSERT INTO users (username, hash) VALUES(:username,:hash)",username=request.form.get("username"), hash=hash)
        
        #username is not unique
        if not result:
            return apology(" Enter another username")
        
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
         
        #automatic log in   
        session["user_id"]=rows[0]["id"]
        
        return redirect(url_for("index"))
    
    # via redirect or link
    else:
        return render_template("register.html")
    
        
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    
    #via form submission
    if request.method=="POST":
        #list of all stock symbols for this user with shares>0
        result=db.execute("SELECT DISTINCT symbol FROM history WHERE user_id=:id AND qty>0",id=session["user_id"])
        
        found=False
        #check if user has entered a stock symbol which he/she holds
        for i in range(len(result)):
            if request.form.get("symbol")==result[i]["symbol"]:
                found=True
                break
        if not found:
            return apology("You do not own this stock!")
        
        #check that no. of shares asked to sell is not less than what he/she owns for that stock
        result=db.execute("SELECT sum(qty) AS sum, symbol FROM history WHERE user_id=:id and symbol=:s GROUP BY symbol", id=session["user_id"], s=request.form.get("symbol"))
        if result[0]["sum"]<int(request.form.get("qty")):
            return apology("You do not have so many shares of {} stock!".format(request.form.get("symbol")))
        
        #check for current price
        quote=lookup(request.form.get("symbol"))
        
        #insert new transaction in log    
        db.execute("INSERT INTO history (user_id, symbol, qty, price, stock) VALUES(:user_id,:symbol,:qty,:price,:name)", user_id=session["user_id"], symbol=quote['symbol'], qty=-int(request.form.get("qty")), price=quote['price'], name=quote['name'])
    
        #increase cash by amount received 
        db.execute("UPDATE users SET cash=cash+:amount WHERE id=:id",amount=quote['price']*int(request.form.get("qty")), id=session["user_id"])
        
        return redirect(url_for("index"))
        
    else:
        return render_template("sell.html")

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    #via form submission
    if request.method=="POST":
        
        #current password blank
        if request.form.get("current")=="":
            return apology("Enter your current password!")
        
        #retrieve stored hash
        pwd=db.execute("SELECT hash FROM users WHERE id=:id",id=session["user_id"])
        
        #match entered password with database after hashing
        if not pwd_context.verify(request.form.get("current"), pwd[0]["hash"]):
            return apology("Wrong password entered!")
        
        if request.form.get("password1")=="":
            return apology("Missing password!")
                
        if request.form.get("password2")=="":
            return apology("Missing password confirmation!")
                
        if request.form.get("password1")!= request.form.get("password2"):
            return apology("Passwords do not match!")
        
        #calculate hash        
        hash=pwd_context.encrypt(request.form.get("password1"))
        
        #update new password
        db.execute("UPDATE users SET hash=:hash WHERE id=:id",hash=hash,id=session["user_id"])
        
        return redirect(url_for("index"))
    
    else:
        return render_template("change.html")