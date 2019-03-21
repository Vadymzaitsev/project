import os
import datetime
import time
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for  # libraries
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint
from math import sqrt
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///math.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():  # almost empty function

    return render_template("index.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    story = db.execute("SELECT * FROM history WHERE user_id = :user_id", user_id=session["user_id"])
    for row in story:

        row["dates"] = time.ctime(row["dates"])
    return render_template("history.html", story=story)  # returns table


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE name = :name",
                          name=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return render_template("index.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/equation", methods=["GET", "POST"])
@login_required
def equation():
    if request.method == "POST":  # where it all began
        equat = request.form.get("equation")
        equation = equat
        equat = list(equat.split(" "))
        print(equat)
        guess1 = request.form.get("guess1")
        guess2 = request.form.get("guess2")
        if not equat:  # check
            return apology("Write at least equation you want to solve", 418)
        if not guess1:
            guess1 = 0
        if not guess2:
            guess2 = 0
        left = []

        right = []
        for i in range(len(equat)):
            if equat[i] == "=":
                for j in range(i):
                    left.append(equat[j])  # sorting to left and right

                for f in range(i+1, len(equat)):
                    right.append(equat[f])
                break
        print(left)
        print(right)
        if left[0][1:] == "**2":  # done
            a = 1
            if left[1][1].isalpha():
                b = (1 if left[1][0] == "+" else -1)
            elif left[1][2].isalpha():  # quadratic
                b = float(left[1][:2])
            elif left[1][3].isalpha():
                b = float(left[1][:3])
            c = float(left[2])
            D = b ** 2 - 4 * a * c
            if D == 0:
                x1 = -b / (2 * a)
                x2 = x1
                dates = datetime.datetime.now().timestamp()
                db.execute("INSERT INTO history (dates, answers, guessed, equation, user_id) VALUES (:dates, :answers, :guessed, :equation, :user_id)",
                                                                                                                                            dates=dates, answers=str("%s, %s" % (x1, x2)), guessed=str("%s, %s" % (guess1, guess2)), equation=equation, user_id=session["user_id"])

                return render_template("answers.html", x1=x1, x2=x2, guess1=guess1, guess2=guess2)
            elif D < 0:
                x1 = "nothing"  # wasted
                x2 = x1
                dates = datetime.datetime.now().timestamp()
                db.execute("INSERT INTO history (dates, answers, guessed, equation, user_id) VALUES (:dates, :answers, :guessed, :equation, :user_id)",
                                                                                                                                            dates=dates, answers=str("%s, %s" % (x1, x2)), guessed=str("%s, %s" % (guess1, guess2)), equation=equation, user_id=session["user_id"])

                return render_template("answers.html", x1=x1, x2=x2, guess1=guess1, guess2=guess2)
            else:
                x1 = (-b + sqrt(D)) / (2 * a)
                x2 = (-b - sqrt(D)) / (2 * a)  # normal situation
                dates = datetime.datetime.now().timestamp()
                db.execute("INSERT INTO history (dates, answers, guessed, equation, user_id) VALUES (:dates, :answers, :guessed, :equation, :user_id)",
                                                                                                                                            dates=dates, answers=str("%s, %s" % (x1, x2)), guessed=str("%s, %s" % (guess1, guess2)), equation=equation, user_id=session["user_id"])


                return render_template("answers.html", x1=x1, x2=x2, guess1=guess1, guess2=guess2)  # done

        elif left[0][2:] == "**2":
            a = float(left[0][:1])
            if left[1][1].isalpha():
                b = (1 if left[1][0] == "+" else -1)
            elif left[1][2].isalpha():  # almost same
                b = float(left[1][:2])
            elif left[1][3].isalpha():
                b = float(left[1][:3])
            c = float(left[2])
            D = b ** 2 - 4 * a * c
            if D == 0:
                x1 = -b / (2 * a)
                x2 = x1
                dates = datetime.datetime.now().timestamp()
                db.execute("INSERT INTO history (dates, answers, guessed, equation, user_id) VALUES (:dates, :answers, :guessed, :equation, :user_id)",
                                                                                                                                            dates=dates, answers=str("%s, %s" % (x1, x2)), guessed=str("%s, %s" % (guess1, guess2)), equation=equation, user_id=session["user_id"])

                return render_template("answers.html", x1=x1, x2=x2, guess1=guess1,guess2=guess2)
            elif D < 0:
                print("no answer")
                x1 = "nothing"  # same
                x2 = x1
                dates = datetime.datetime.now().timestamp()
                db.execute("INSERT INTO history (dates, answers, guessed, equation, user_id) VALUES (:dates, :answers, :guessed, :equation, :user_id)",
                                                                                                                                            dates=dates, answers=str("%s, %s" % (x1, x2)), guessed=str("%s, %s" % (guess1, guess2)), equation=equation, user_id=session["user_id"])

                return render_template("answers.html", x1 = x1, x2=x2, guess1=guess1, guess2=guess2)
            else:
                x1 = (-b + sqrt(D)) / (2 * a)  # same
                x2 = (-b - sqrt(D)) / (2 * a)
                dates = datetime.datetime.now().timestamp()
                db.execute("INSERT INTO history (dates, answers, guessed, equation, user_id) VALUES (:dates, :answers, :guessed, :equation, :user_id)",
                                                                                                                                            dates=dates, answers=str("%s, %s" % (x1, x2)), guessed=str("%s, %s" % (guess1, guess2)), equation=equation, user_id=session["user_id"])

                return render_template("answers.html", x1=x1, x2=x2, guess1=guess1, guess2=guess2)
                # done
        i = -1
        brack = 0
        while i != len(left):
            if i+1 == len(left):
                break
            i += 1
            alphacount = 0

            for j in range(len(left[i])):

                # print(i,j, left[i][j])
                if left[i][j].isalpha():
                    alphacount += 1

                elif left[i][j] == "(":
                    brack = 1
                    index = i

                    if left[index][-2] == "*" or left[index][-2] == "-":
                        if left[index][-2] == "-":
                            number = -1
                        else:
                            number = float(left[index][:-2])

                        while True:  # infinite loop
                            print("221", i, j)

                            if j + 1 == len(left[i]):
                                j = 0
                                i += 1
                            else:
                                j += 1
                            if left[index][-2] == "*":
                                alcount = 0
                                for d in range(len(left[i])):
                                    if left[i][d].isalpha():
                                        letter = left[i][d]
                                        alcount += 1
                                    if d == len(left[i]):
                                        if len(left[i][d]) == 1:
                                            if alcount == 1:

                                                el = str("%d%s" % (number, letter))
                                                if number > 0:
                                                    el = str("+%d%s" % (number, letter))  # slikajfodi
                                                del left[i]
                                                left.append(el)

                                            else:
                                                el = -number
                                                if el > 0:
                                                    el = str("+%d" % el)  # slikajfudi
                                                del left[i]
                                                right.append(el)

                                        else:
                                            if alcount == 1:
                                                el = number * float(left[i][:-1])
                                                if el > 0:
                                                    el = str("+%d%s" % (el, letter))
                                                elif el < 0:
                                                    el = str("%d%s" % (el, letter))
                                                left.append(el)
                                                del left[i]
                                            else:
                                                el = -number * float(left[i])  # slikajfudu

                                                if el > 0:
                                                    el = str("+%d" % el)
                                                elif el < 0:
                                                    el = str("%d" % el)
                                                right.append(el)
                                                del left[i]
                                if left[i] == ")":
                                    continue_index = i
                                    print("273")
                                    del left[index]
                                    break
                            # print("here")
                            elif left[index][-2] == "-":
                                for minus in range(index, len(left)):
                                    if len(left[minus]) == 1:
                                        left[minus] = str("-%s" % left[minus])

                                    else:
                                        if left[minus][0] == "-":
                                            left[minus] = str("+%s" % left[minus][1:])
                                        else:
                                            left[minus] = str("-%s" % left[minus][1:])  # sloakajfudu
                                    if left[minus] == ")":
                                        continue_index = i - 1
                                        del left[index]
                                        break
                    else:
                        return 1

            if alphacount == 0:
                if brack == 1:
                    i = continue_index
                if len(left[i]) > 1:
                    if left[i][0] == "+" or left[i][0] == "-" or left[i][0].isdigit():
                        for f in range(1, len(left[i])):
                            if not left[i][f].isdigit() and left[i][f] == "/":
                                if left[i][f-1] == "/" or left[i][f-1] == "*":
                                    break
                                else:
                                    return 1
                        if left[i][0] == "+":
                            left[i] = "-"+left[i][1:]  # changing position
                        elif left[i][0] == "-":
                            left[i] = "+"+left[i][1:]
                        else:
                            left[i] = "-"+left[i]
                        right.append(left[i])
                        del left[i]
                else:
                    left[i] = "-"+left[i]
                    right.append(left[i])  # efaw
                    del left[i]

        i = -1
        brack = 0
        while i != len(right):
            print("298")
            print(right[i])
            alphacount = 0  # efwf
            if i+1 == len(right):
                break
            i += 1

            for j in range(len(right[i])):
                if right[i][j].isalpha():
                    alphacount += 1

                elif right[i][j] == "(":  # efwf
                    brack = 1
                    index = i

                    if right[index][-2] == "*" or right[index][-2] == "-":
                        number = float(right[index][:-2])
                        while True:
                            j += 1
                            if j == len(right[i]):
                                j = 0
                                i += 1

                            if right[index][-2] == "*":  # efwf
                                alcount = 0
                                for d in range(len(right[i])):
                                    if right[i][d].isalpha():
                                        letter = right[i][d]  # efwf
                                        alcount += 1
                                    if d == len(right[i]):
                                        if len(right[i][d]) == 1:
                                            if alcount == 1:
                                                el = -number
                                                el = str("%d%s" % (el, letter))
                                                if el > 0:
                                                    el = str("+%d" % el)  # efwf
                                                elif el < 0:
                                                    el = str("-%d" % el)
                                                left.append(el)
                                                del right[i]
                                            else:
                                                el = number
                                                if el > 0:
                                                    el = str("+%d" % el)  # efwf
                                                elif el < 0:
                                                    el = str("-%d" % el)
                                                right.append(el)
                                                del right[i]

                                        else:
                                            if alcount == 1:
                                                el = -number * float(left[i][:-1])  # efwf
                                                el = str("%d%s" % (el, letter))
                                                if el > 0:
                                                    el = str("+%d" % el)
                                                elif el < 0:
                                                    el = str("%d" % el)
                                                left.append(el)
                                                del right[i]

                                            else:
                                                el = number * float(left[i])  # efwf

                                                if el > 0:
                                                    el = str("+%d" % el)
                                                elif el < 0:
                                                    el = str("%d" % el)
                                                right.append(el)
                                                del right[i]
                                if right[i][j] == ")":  # efwf
                                    continue_index = i
                                    del right[index]
                                    break
                            elif index[-2] == "-":
                                for minus in range(index, len(right)):
                                    if len(right[minus]) == 1:
                                        right[minus] = str("-%d" % right[minus])

                                    else:  # efwf
                                        if minus[0] == "-":
                                            right[minus] = str("+%d" % right[minus])
                                        else:  # efwf
                                            right[minus] = str("-%d" % right[minus])  # efwf
                                    if right[minus] == ")":
                                        continue_index = i
                                        del right[index]
                                        break  # efwf
                    else:
                        return 1

            if alphacount == 1:  # efwf
                if brack == 1:
                    i = continue_index  # efwf
                if len(right[i]) > 1:
                    if right[i][0] == "+" or right[i][0] == "-" or right[i][0].isdigit() or right[i][0] == "*" or right[i][0] == "/":  # efwf
                        for f in range(1, len(right[i])):
                            if not right[i][f].isdigit() and right[i][f] == "/":
                                if right[i][f-1] == "/" or right[i][f-1] == "*":
                                    break  # efwf
                                else:
                                    return 1
                        if right[i][0] == "+":
                            right[i][0] = "-"
                        elif right[i][0] == "-":
                            right[i][0] = "+"
                        else:
                            right[i] = "-"+right[i][0]
                        left.append(right[i])
                        del right[i]
                else:
                    right[i] = str("-%s" % right[i])
                    left.append(right[i])  # efwf
                    del right[i]
        print(left)
        print(right)
        sum_left = 0
        sum_right = 0
        for left_el in left:
            print(left_el)
            if len(left_el) == 1:
                sum_left += 1
            elif len(left_el) == 2:  # efwf
                if left_el[0] == "-":
                    sum_left += -1
                elif left_el[0] == "+":

                    sum_left += 1
                else:
                    sum_left += float(left_el[0])
            else:
                sum_left += float(left_el[:-1])  # efwf
        print(sum_left)

        for right_el in right:
            sum_right += float(right_el)
        print(sum_right)
        x1 = sum_right / sum_left
        x2 = x1
        print(x1)

        dates = datetime.datetime.now().timestamp()  # efwf
        db.execute("INSERT INTO history (dates, answers, guessed, equation, user_id) VALUES (:dates, :answers, :guessed, :equation, :user_id)",
                                                                                                                                    dates=dates, answers=str("%s, %s" % (x1, x2)), guessed=str("%s, %s" % (guess1, guess2)), equation=equation, user_id=session["user_id"])

        return render_template("answers.html", x1=x1, x2=x2, guess1=guess1, guess2=guess2)
    else:
        return render_template("equation.html")  # efwf


"""
@app.route("/equation", methods=["GET", "POST"])
@login_required
def system():
    if request.method == "POST":
        equation1 = request.form.get("equation1")
        if not equation1:
            return apology("your system is not full", 403)
        equation2 = request.form.get("equation2")
        if not equation2:
            return apology("your system is not full", 403)

        guess_x = request.form.get("guess_x")
        guess_y = request.form.get("guess_y")
        equat1 = equation1
        equation1 = equation1.split(" ")

        equat2 = equation2
        equation2 = equation2.split(" ")
        left1 = []
        left2 = []
        right1 = []
        right2 = []
        for i in range(len(equation1)):
            if equation1[i] == "=":
                for j in range(i):
                    left1.append(equation1[j])
                for j in range(i+1, len (equation1)):
                    right1.append(equation1[j])

        for i in range(len(equation2)):
            if equation2[i] == "=":
                for j in range(i):
                    left2.append(equation2[j])
                for j in range(i+1, len (equation2)):
                    right2.append(equation2[j])
        letter = 0
        if len(left1) < len(left2):
            for i in range(len(left1)):
                for j in left1[i]:
                    if j.isalpha():
                        if len(left1[i]) == 1 or len(left1[i]) == 2 :
                            letter = j
                            if i > 0 :
                                for before in range(i):
                                    if len(left1[before]) == 1:

                                        left1[before] = str("-%s" % left1[before])
                                        right1.append(left1[before])
                                        del left1[before]
                                    else:
                                        if left1[before][0] == "+":
                                            left1[before] = str("-%s" % left1[before][1:])
                                            right1.append(left1[before])
                                            del left1[before]
                                        elif left1[before][0] == "-":
                                            left1[before] = str("+%s" % left1[before][1:])
                                            right1.append(left1[before])
                                            del left1[before]

                                        elif left1[before][0].isdigit():
                                            left1[before] = str("-%s" % left1[before])
                                            right1.append(left1[before])
                                for after in range(i+1, len(left1)):
                                    if len(left1[after]) == 1:

                                        left1[before] = str("-%s" % left1[before])
                                        right1.append(left1[before])
                                        del left1[before]
                                    else:
                                        if left1[before][0] == "+":
                                            left1[before] = str("-%s" % left1[before][1:])
                                            right1.append(left1[before])
                                            del left1[before]
                                        elif left1[before][0] == "-":
                                            left1[before] = str("+%s" % left1[before][1:])
                                            right1.append(left1[before])
                                            del left1[before]

                                        elif left1[before][0].isdigit():
                                            left1[before] = str("-%s" % left1[before])
                                            right1.append(left1[before])
                            if letter[0] == "-":
                                if right1[0][0].isdigit() or right1[0][0].isalpha():
                                    right1[0] = str("-%s" % right1[0])
                                    pas = 1

                                for i in range(len(right1)):
                                    if i == 0 :
                                        continue
                                    if right1[i][0] == "+":
                                        right1[i] = str("-%s" % right1[i][1:])
                                    elif right1[i][0]=="-":
                                        right1[i] = str("+%s" % right1[i][1:])

                                another_key = right1

            for elem_big in range(len(left2)):
                for el_small in range(len(elem_big)):
                    if left2[elem_big][el_small] == letter:
                        del left2[elem_big][el_small]
                        if len(left2[elem_big]) == 1:
                            another_key[0] = str("+%s" % another_key)
                            for i in another_key:
                                alcount = 0
                                left2.append(i)
                                for j in i:
                                    if j.isalpha():
                                        alcount = 1
                                if alcount == 0:
                                    if len(i) == 1:
                                        i = str("-%s" % i)
                                    else:
                                        if i[0] == "+":
                                            i = str("-%s" % i[1:])
                                        elif i[0] == "-":
                                            i = str("+%s" % i[1:])
                                        else:
                                            i=str("-%s" % i)
                                    right2.append(i)
                                    del i

                        else:
                            if left2[elem_big][-2].isdigit():
                                number = float(left2[elem_big][:-1])
                                alcount = 0
                                for d in range(len(left2[elem_big])):
                                    if left2[elem_big][d].isalpha():

                                        alcount+=1
                                    if d == len(left2[elem_big]):
                                        if len(left2[elem_big][d]) == 1:
                                            if alcount == 1:

                                                el = str("%d%s" %(number, letter))
                                                if number > 0:
                                                    el = str("+%d%s" %(number, letter))
                                                del left2[elem_big]
                                                left2.append(el)

                                            else:
                                                el = -number
                                                if el > 0:
                                                    el = str("+%d" % el)
                                                del left2[elem_big]
                                                right2.append(el)


                                        else:
                                            if alcount == 1:
                                                el = number * float(left[i][:-1])
                                                if el > 0:
                                                    el = str("+%d%s" % (el, letter))
                                                elif el < 0:
                                                    el = str("%d%s" % (el, letter))
                                                left.append(el)
                                                del left[i]
                                            else:
                                                el = -number * float(left[i])

                                                if el > 0:
                                                    el = str("+%d" % el)
                                                elif el < 0:
                                                    el = str("%d" % el)
                                                right.append(el)
                                                del left[i]
                                if left[i][j] == ")":
                                    continue_index = i
                                    break
                            #print("here")
                            elif index[-2] == "-":
                                for minus in range(index,len(left)):
                                    if len(left[minus]) == 1:
                                        left[minus] = str("-%d" % left[minus])

                                    else:
                                        if minus[0] == "-":
                                            left[minus] = str("+%d" % left[minus])
                                        else:
                                            left[minus] = str("-%d" % left[minus])
                                    if left[minus] == ")":
                                        continue_index = i
                                        break




        else: #TODO
            for i in range(len(left1)):
                for j in left1[i]:
                    if j.isalpha():
                        if len(left1[i]) == 1 or len(left1[i]) == 2:
                            letter = j
                            if i > 0 :
                                for before in range(i):
                                    if len(left1[before]) == 1:

                                        left1[before] = str("-%s" % left1[before])
                                        right1.append(left1[before])
                                        del left1[before]
                                    else:
                                        if left1[before][0] == "+":
                                            left1[before] = str("-%s" % left1[before][1:])
                                            right1.append(left1[before])
                                            del left1[before]
                                        elif left1[before][0] == "-":
                                            left1[before] = str("+%s" % left1[before][1:])
                                            right1.append(left1[before])
                                            del left1[before]

                                        elif left1[before][0].isdigit():
                                            left1[before] = str("-%s" % left1[before])
                                            right1.append(left1[before])
                                for after in range(i+1, len(left1)):
                                    if len(left1[after]) == 1:

                                        left1[before] = str("-%s" % left1[before])
                                        right1.append(left1[before])
                                        del left1[before]
                                    else:
                                        if left1[before][0] == "+":
                                            left1[before] = str("-%s" % left1[before][1:])
                                            right1.append(left1[before])
                                            del left1[before]
                                        elif left1[before][0] == "-":
                                            left1[before] = str("+%s" % left1[before][1:])
                                            right1.append(left1[before])
                                            del left1[before]

                                        elif left1[before][0].isdigit():
                                            left1[before] = str("-%s" % left1[before])
                                            right1.append(left1[before])
                            if letter[0] == "-":
                                if right1[0][0].isdigit() or right1[0][0].isalpha():
                                    right1[0] = str("-%s" % right1[0])
                                    pas = 1

                                for i in range(len(right1)):
                                    if i == 0 :
                                        continue
                                    if right1[i][0] == "+":
                                        right1[i] = str("-%s" % right1[i][1:])
                                    elif right1[i][0]=="-":
                                        right1[i] = str("+%s" % right1[i][1:])



    else:
        return render_template("system.html")
"""


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form.get("username")  # efwf
        if name == None:
            return apology("must provide username", 403)

        password = request.form.get("password")
        if password == None:
            return apology("must provide password", 403)  # efwf
        elif len(password) < 6:
            return apology("password has to be bigger or equal to 6")

        confirmation = request.form.get("confirmation")
        if confirmation == None:
            return apology("must confirm your password", 403)
        elif confirmation != password:  # efwf
            return apology("Yer a teapot User", 418)

        hashed = generate_password_hash(password)
        print(name)
        print(hashed)  # efwf
        row = db.execute("INSERT INTO users (name, password) VALUES (:name, :password)", name=name, password=hashed)
        print(row)
        if not row:
            return apology("username already exist")
            # при проверке на существующее имя должно быть все немного иначе, нужно сделать запрос с отбором только по имени до создания нового пользоватьеля и тогда вывести эту ошибку

        session["user_id"] = row

        return render_template("index.html")  # efwf
    else:
        return render_template("register.html")


@app.route("/instruction", methods=["GET", "POST"])
def instruction():
    if request.method == "POST":  # efwf
        return redirect("/")
    else:
        return render_template("index.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
