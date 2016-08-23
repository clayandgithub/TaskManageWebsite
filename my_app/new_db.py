#coding=utf-8
#!/usr/bin/python
#SqlModule.py
import sys
import sqlite3
import time
import os

reload(sys) 
sys.setdefaultencoding('utf8')

cx=sqlite3.connect('./new_db.db',check_same_thread = False)
cu=cx.cursor()#for query



def getMaxUserID():
	#cu.execute("select * from Login where uid=(select max(distinct uid) from Login)")
	cu.execute("select max(distinct uid) from Login")
	temp_res = cu.fetchall()
	if temp_res==[(None,)]:
		temp_res=[(0,)]
	return temp_res[0][0]


def getMaxPersonID():
	cu.execute("select max(distinct personId) from birthday")
	temp_res = cu.fetchall()
	if temp_res==[(None,)]:
		temp_res=[(0,)]
	return temp_res[0][0]

def getMaxNoteID():
	cu.execute("select max(distinct issueId) from note")
	temp_res = cu.fetchall()
	if temp_res==[(None,)]:
		temp_res=[(0,)]
	return temp_res[0][0]

def getMaxTaskID():
	cu.execute("select max(distinct taskId) from task")
	temp_res = cu.fetchall()
	if temp_res==[(None,)]:
		temp_res=[(0,)]
	return temp_res[0][0]

def getTimeStamp():
    return time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))

def getDateTime():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))

def getCWD():
    return os.getcwd()

def getFileName(str):
    return os.listdir(os.getcwd()+str)#under current catalog

#user
def registerNewId(uid,account,psw):
    str1=[uid,account,psw]
    cx.execute("insert into Login values(?,?,?)",str1)
    cx.commit()

def registerNewUser(uid,account,psw,name,contract,avatar):
	registerNewId(uid,account,psw)
	issueId=uid
	createNote(issueId,uid,'')
	str1=[uid,name,contract,avatar]
	cx.execute("insert into user(uid,name,contract,avatar) values(?,?,?,?)",str1)
	cx.commit()

#UA-->UserAccount,Pwd-->Password
def getPwdByUA(user_accuount):
	str=[user_accuount]
	cu.execute("select psw from Login where account=(?)",str)
	temp_res=cu.fetchall()
	if temp_res==[]:
		return '' 
	else:
		return temp_res[0][0]

def getUidByUA(user_accuount):
	str=[user_accuount]
	cu.execute("select uid from Login where account=(?)",str)
	temp_res=cu.fetchall()
	if temp_res==[]:
		return 0 
	else:
		return temp_res[0][0]

def deleteAlluser():
	cu.execute("delete from Login")
	cu.execute("delete from user")
	cu.execute("delete from note")
	cu.execute("delete from task")
	cu.execute("delete from birthday")
	cx.commit()

def deleteUser(user_accuount):
	uid = getUidByUA(user_accuount)
	str=[uid]
	cu.execute("delete from Login where uid=?",str)
	cu.execute("delete from user where uid=?",str)
	cu.execute("delete from note where uid=?",str)
	cu.execute("delete from task where uid=?",str)
	cu.execute("delete from birthday where uid=?",str)
	cx.commit()

def updateAvatar(uid,avatar):
    str=[avatar,uid]
    cx.execute("update user set avatar=? where uid=?",str)
    cx.commit()

def updateUser(uid,new_account,new_psw,new_avatar):
	updateAvatar(uid,new_avatar)
	str=[new_account,new_psw,uid]
	cx.execute("update Login set account=?,psw=? where uid=?",str)
	cx.commit()

def getAvatar(user_account):
	uid = getUidByUA(user_account)
	str=[uid]
	cu.execute("select avatar from user where uid=?",str)
	temp_res=cu.fetchall()
	if temp_res==[]:
		return '../static/img/null_my_photo.jpg' 
	else:
		return temp_res[0][0]
#不用
def getUserInfo(uid):
    str=[uid]
    cu.execute("select * from user where uid=?",str)
    return cu.fetchall()

##task
def InsertTask(taskId,user_accuount,taskName,content,taskStartTime,taskEndTime,status):
	uid=getUidByUA(user_accuount)
	str=[taskId,uid,taskName,content,taskStartTime,taskEndTime,status]
	cx.execute("insert into task(taskId,uid,taskName,content,taskStartTime,taskEndTime,status) values(?,?,?,?,?,?,?)",str)
	cx.commit()

def deleteTask(taskId):
    str=[taskId]
    cx.execute("delete from task where taskId=?",str)
    cx.commit()

def updateTask(taskId,taskName,content,taskStartTime,taskEndTime):
    str=[taskName,content,taskStartTime,taskEndTime,taskId]
    cx.execute("update task set taskName=?,content=?,taskStartTime=?,taskEndTime=? where taskId=?",str)
    cx.commit()

def getTaskWholeInfo(taskId):
    str=[taskId]
    cu.execute("select * from task where taskId=?",str)
    return cu.fetchall()

def getTasksByUA(user_account):
	uid=getUidByUA(user_account)
	str=[uid]
	cu.execute("select * from task where uid=?",str)
	return cu.fetchall()

def getTasksIdByUA(user_account):
	uid=getUidByUA(user_account)
	str=[uid]
	cu.execute("select taskId from task where uid=?",str)
	return cu.fetchall()


def finishTask(task_id):
    str=['true',task_id]
    cx.execute("update task set status=? where taskId=?",str)
    cx.commit()

##note
def getNoteIdByUid(uid):
	str=[uid]
	cu.execute("select issueId from note where uid=(?)",str)
	temp_res=cu.fetchall()
	if temp_res==[]:
		return 0 
	else:
		return temp_res[0][0]

def createNote(issueId,uid,content):
    str=[issueId,uid,content]
    cx.execute("insert into note(issueId,uid,content) values(?,?,?)",str)
    cx.commit()
#不用
def deleteNote(user_accuount):
	uid=getUidByUA(user_accuount)
	str=[uid]
	cx.execute("delete from note where uid=?",str)
	cx.commit()

def updateNote(user_accuount,content):
	uid=getUidByUA(user_accuount)
	str=[content,uid]
	cx.execute("update note set content=? where uid=?",str)
	cx.commit()
#不用
def getNoteInfo(issueId):
    str=[issueId]
    cu.execute("select * from note where issueId=?",str)
    return cu.fetchall()

def getNoteByUA(user_accuount):
	uid=getUidByUA(user_accuount)
	str=[uid]
	cu.execute("select content from note where uid=?",str)
	temp_res=cu.fetchall()
	if temp_res==[]:
		return ''
	else:
		return temp_res[0][0]
##birthday
def insertBirthday(user_accuount,personId,birthday,personName,contract,photo):
	uid=getUidByUA(user_accuount)
	str=[uid,personId,birthday,personName,contract,photo]
	cx.execute("insert into birthday(uid,personId,birthday,personName,contract,photo) values(?,?,?,?,?,?)",str)
	cx.commit()

def updateBirthday(personId,birthday,personName,contract,photo):
	str=[birthday,personName,contract,photo,personId]
	cx.execute("update birthday set birthday=?,personName=?,contract=?,photo=? where personId=?",str)
	cx.commit()

def deleteBirthday(personId):
    str=[personId]
    cx.execute("delete from birthday where personId=?",str)
    cx.commit()

def getBirthdaysByUA(user_accuount):
	uid=getUidByUA(user_accuount)
	str=[uid]
	cu.execute("select * from birthday where uid=?",str)
	return cu.fetchall()

def getPersonIdByUid(uid):
	str=[uid]
	cu.execute("select personId from birthday where uid=?",str)
	return cu.fetchall()

def getBirthdayWholeInfo(personId):
    str=[personId]
	#需要split################################################
    cu.execute("select * from birthday where personId=?",str)
    return cu.fetchall()
def getPhotoByPersonId(person_id):
	str=[person_id]
	cu.execute("select photo from birthday where personId=?",str)
	temp_res=cu.fetchall()
	if temp_res==[]:
		return '../static/img/null_person_photo.jpg' 
	else:
		return temp_res[0][0]

def closeDB():
    cx.close()
    cu.close()
###########################################################


