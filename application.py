from contextlib import closing
from flask import Flask, render_template, url_for, flash, json, request, redirect, session, g, abort
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from flask.ext.mysql import MySQL
import random
from random import randint
import os

mysql = MySQL()
application = Flask(__name__)
application.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
application.config['MYSQL_DATABASE_USER'] = 'sunday'
application.config['MYSQL_DATABASE_PASSWORD'] = 'Sunxiran0701!'
application.config['MYSQL_DATABASE_DB'] = 'BucketList'
#application.config['MYSQL_DATABASE_HOST'] = 'mydbinstance.c8t6fbtwcbmn.us-west-2.rds.amazonaws.com'
application.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(application)

#application = Flask(__name__)
#application.config.from_envvar('MUSIAUTH_SETTING', silent=True)'

@application.route('/')
def main():
    return render_template('index.html')

@application.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@application.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

@application.route('/showAudioone')
def showAudioone():
    print session.get('email')
    audio_files = [f for f in os.listdir('Audio/') if f.endswith('mp3')]
    audio_files_number = len(audio_files)
    return render_template('audioone.html',
	audio_files_number = audio_files_number,
	audio_files = audio_files)

@application.route('/showAudiotwo')
def showAudiotwo():
	return render_template('audiotwo.html')

@application.route('/showAudiothree')
def showAudiothree():
    return render_template('audiothree.html')

@application.route('/showAudiofour')
def showAudiofour():
    return render_template('audiofour.html')

@application.route('/showComplete')
def showComplete():
	return render_template('complete.html')

@application.route('/signUp', methods=['POST','GET'])
def signUp():
    _email = request.form['inputEmail']
    conn = mysql.connect()
    cursor = conn.cursor()
    #cursor.execute("insert into tbl_user (user_name, user_username, user_password) values (%s, %s, %s)", ('sunday', _email, 'sunday'))
    #conn.commit()
    #return redirect(url_for('showAudioone'))
    cursor.execute("select * from tbl_ma where user_email = %s", [_email])
    data = cursor.fetchone()
    if data is None:
        cursor.execute("insert into tbl_ma (user_email, user_audioone, user_audiotwo, user_audiothree, user_audiofour, user_result) values (%s, %s, %s, %s, %s, %s)", (_email, 'null','null','null','null','YES'))
        conn.commit()
        cursor.close()
        conn.close()
        session['email'] = _email
        return redirect(url_for('showAudioone'))
    else:
        return redirect(url_for('showSignUp'))

@application.route('/signIn', methods=['POST'])
def signIn():
    try:
        _email = request.form['inputEmail']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from tbl_ma where user_email = %s", [_email])
        data = cursor.fetchone()
        session['email'] = _email
        if data is None:
            session['email'] = _email
	    return redirect(url_for('showSignIn'))
        else:
            return redirect(url_for('showAudioone'))
    except Exception as e:
        return redirect(url_for('showSignIn'))
    finally:
        cursor.close()
        conn.close()

@application.route('/selectAudioone', methods=['POST'])
def selectAudioone():
    _email = session['email']
    print _email
    conn = mysql.connect()
    cursor = conn.cursor()
    key = str(randint(25,50))
    print key
    cursor.execute("update tbl_ma set user_audioone = %s where user_email = %s", (key,_email))
    conn.commit()
    cursor.close()
    conn.close()    
    return redirect(url_for('showAudiotwo'))

@application.route('/selectAudiotwo', methods=['POST'])
def selectAudiotwo():
    _email = session['email']
    print _email
    conn = mysql.connect()
    cursor = conn.cursor()
    key = str(randint(0, 25))
    print key
    cursor.execute("update tbl_ma set user_audiotwo = %s where user_email = %s",(key,_email))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('showAudiothree'))

@application.route('/selectAudiothree', methods=['POST'])
def selectAudiothree():
    _email = session['email']
    print _email
    conn = mysql.connect()
    cursor = conn.cursor()
    key = str(randint(75,100))
    print key
    cursor.execute("update tbl_ma set user_audiothree = %s where user_email = %s",(key,_email))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('showAudiofour'))

@application.route('/selectAudiofour', methods=['POST'])
def selectAudiofour():
    _email = session['email']
    print _email
    conn = mysql.connect()
    cursor = conn.cursor()
    key = str(randint(50,75))
    print key
    cursor.execute("update tbl_ma set user_audiofour = %s where user_email = %s",(key,_email))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('showComplete'))

@application.route('/signOut', methods=['POST'])
def signOut():
    del session['email']
    return redirect('/')

#@application.route('/userHome')
#def userHome():
#    if session.get('user'):
#        return render_template('userHome.html')
#    else:
#        return render_template('error.html',error = 'Unauthorized Access')


#@application.route('/logout')
#def logout():
#    session.pop('user',None)
#    return redirect('/')

#@application.route('/validateLogin',methods=['POST'])
#def validateLogin():
#    try:
#        _username = request.form['inputEmail']
#        _password = request.form['inputPassword']
        
        # connect to mysql

#        con = mysql.connect()
#        cursor = con.cursor()
#	cursor.execute("select * from tbl_user where user_username = %s and user_password = %s",(_username,_password))
#	data = cursor.fetchone()

#        if data is None:
#        	return render_template('error.html',error = 'Wrong Email address or Password.')
#        else:
#        	#return redirect('/userHome')    
#    		return render_template('userHome.html')
#    except Exception as e:
#        return render_template('error.html',error = str(e))
#    finally:
#        cursor.close()
#        con.close()


if __name__ == "__main__":
    	application.run(debug=True)
