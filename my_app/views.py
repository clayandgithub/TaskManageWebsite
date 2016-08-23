#coding=utf-8
import sys, os, math,string,hashlib,time,datetime
from flask import Flask, request, render_template,redirect, url_for
from werkzeug import secure_filename

from my_app import app,new_db

reload(sys) 
sys.setdefaultencoding('utf8')

def encrypt(s):
	return hashlib.new("md5", s).hexdigest()

def check_encrypted_Pwd(user_ac, e_user_pwd):
	if user_ac=='':
		return False
	password = new_db.getPwdByUA(user_ac)
	if e_user_pwd==hashlib.new("md5", password).hexdigest():
		return True
	return False

def checkUser_Pwd(user_ac, user_pwd):
	if user_ac=='' or user_pwd=='':
		return False
	return user_pwd == new_db.getPwdByUA(user_ac)

def checkRegister_Info(user_ac, user_pwd1,user_pwd2):
	reg_error = 0
	if user_ac=='' or user_pwd1=='':
		reg_error = 1
	elif user_pwd1!=user_pwd2:
		reg_error = 2
	#检测是否重名
	elif new_db.getPwdByUA(user_ac)!='':
		reg_error = 3
	return reg_error

def getPhotoByUserAccount(user_ac):
	return new_db.getAvatar(user_ac)
def getNotesByUserAccount(user_ac):
	return new_db.getNoteByUA(user_ac)

def getTaskById(task_id,userAccount):
	task ={'id':0,'name':'','start_year':'',
	'start_month':'','start_day':'','start_hour':'','start_minute':'',
	'end_year':'','end_month':'','end_day':'','end_hour':'',
	'end_minute':'','description':'','status':'false'}
	#安全措施:验证身份
	task_ids = new_db.getTasksIdByUA(userAccount)
	temp_id = (task_id,)
	if task_id==0 or task_ids.count(temp_id)==0:
		pass
	else:
		temp_task = new_db.getTaskWholeInfo(task_id)
		if temp_task!=[]:
			start_year = temp_task[0][4].split('-',1)[0]
			start_month = temp_task[0][4].split('-',2)[1]
			start_day = (temp_task[0][4].split('_',1)[0]).rsplit('-',1)[1]
			start_hour = (temp_task[0][4].split('_',1)[1]).split(':',1)[0]
			start_minute = (temp_task[0][4].split(':',2)[1])
			end_year = temp_task[0][5].split('-',1)[0]
			end_month = temp_task[0][5].split('-',2)[1]
			end_day = (temp_task[0][5].split('_',1)[0]).rsplit('-',1)[1]
			end_hour = (temp_task[0][5].split('_',1)[1]).split(':',1)[0]
			end_minute = (temp_task[0][5].split(':',2)[1])
			if temp_task[0][5]=='2099-12-31_23:59:59':
				task = {'id':temp_task[0][0],'name':temp_task[0][2],'start_year':start_year,
				'start_month':start_month,'start_day':start_day,'start_hour':start_hour,
				'start_minute':start_minute,'end_year':'','end_month':'',
				'end_day':'','end_hour':'','end_minute':'',
				'description':temp_task[0][3],'status':temp_task[0][6]}
			else:
				task = {'id':temp_task[0][0],'name':temp_task[0][2],'start_year':start_year,
				'start_month':start_month,'start_day':start_day,'start_hour':start_hour,
				'start_minute':start_minute,'end_year':end_year,'end_month':end_month,
				'end_day':end_day,'end_hour':end_hour,'end_minute':end_minute,
				'description':temp_task[0][3],'status':temp_task[0][6]}
	return task

def isToday(task_date):
	today_date = new_db.getDateTime()
	#task_date:'1992-01-06',today_date:'1992-01-06'
	try:
		d1 = datetime.datetime.strptime(task_date, '%Y-%m-%d')
		d2 = datetime.datetime.strptime(today_date, '%Y-%m-%d')
		delta = d1 - d2
	except:
		return False
	if delta.days==0 or task_date=='2099-12-31':
		return True
	else:
		return False
	#task_date:1992-02-02

def time_cmp(E1,E2):
	return cmp(E1['endline'], E2['endline']) 

def getAllUnfinTasksByUA(user_ac):
	temp_tasks = new_db.getTasksByUA(user_ac)
	temp_num = len(temp_tasks)
	tasks = []
	if temp_num>0:
		for i in range(temp_num):
			if temp_tasks[i][6]=='false':
				temp_task={'id':temp_tasks[i][0],'name':temp_tasks[i][2],
				'endline':temp_tasks[i][5]}
				tasks.append(temp_task)
		tasks.sort(time_cmp)
	return tasks

def getEightUnfinTasksByUA(user_ac):
	temp_tasks = new_db.getTasksByUA(user_ac)
	temp_num = len(temp_tasks)
	tasks = []
	temp_count=0
	if temp_num>0:
		for i in range(temp_num):
			if temp_tasks[i][6]=='false' and not isToday(temp_tasks[i][5].split('_',1)[0]):
				temp_task={'id':temp_tasks[i][0],'name':temp_tasks[i][2],
				'endline':temp_tasks[i][5]}
				tasks.append(temp_task)
				++temp_count
				if temp_count==8:
					break
		tasks.sort(time_cmp)
	return tasks

def getAllTodayTasksByUA(user_ac):
	#task_id,task_name,endtime(时间不是日期)
	temp_tasks = new_db.getTasksByUA(user_ac)
	temp_num = len(temp_tasks)
	tasks = []
	if temp_num>0:
		for i in range(temp_num):
			if temp_tasks[i][6]=='false' and isToday(temp_tasks[i][5].split('_',1)[0]):
				if temp_tasks[i][5]=='2099-12-31_23:59:59':
					temp_task={'id':temp_tasks[i][0],'name':temp_tasks[i][2],
					'endline':temp_tasks[i][5]}
					tasks.append(temp_task)
				else:
					temp_task={'id':temp_tasks[i][0],'name':temp_tasks[i][2],
					'endline':temp_tasks[i][5].split('_',1)[1]}
					tasks.append(temp_task)
		tasks.sort(time_cmp)
	return tasks

def getEightTodayTasksByUA(user_ac):
	temp_tasks = new_db.getTasksByUA(user_ac)
	temp_num = len(temp_tasks)
	tasks = []
	temp_count=0

	if temp_num>0:
		for i in range(temp_num):
			if temp_tasks[i][6]=='false' and isToday(temp_tasks[i][5].split('_',1)[0]):
				if temp_tasks[i][5]=='2099-12-31_23:59:59':
					temp_task={'id':temp_tasks[i][0],'name':temp_tasks[i][2],
					'endline':temp_tasks[i][5]}
					tasks.append(temp_task)
				else:
					temp_task={'id':temp_tasks[i][0],'name':temp_tasks[i][2],
					'endline':temp_tasks[i][5].split('_',1)[1]}
					tasks.append(temp_task)
					++temp_count
					if temp_count==8:
						break
		tasks.sort(time_cmp)
	return tasks


def getAllFinishedTasksByUA(user_ac):
	temp_tasks = new_db.getTasksByUA(user_ac)
	temp_num = len(temp_tasks)
	tasks = []
	if temp_num>0:
		for i in range(temp_num):
			if temp_tasks[i][6]=='true':
				temp_task={'id':temp_tasks[i][0],'name':temp_tasks[i][2],
				'endline':temp_tasks[i][5]}
				tasks.append(temp_task)
		tasks.sort(time_cmp,reverse=True)
	return tasks

def getEightFinishedTasksByUA(user_ac):
	temp_tasks = new_db.getTasksByUA(user_ac)
	temp_num = len(temp_tasks)
	tasks = []
	temp_count=0

	if temp_num>0:
		for i in range(temp_num):
			if temp_tasks[i][6]=='true':
				temp_task={'id':temp_tasks[i][0],'name':temp_tasks[i][2],
				'endline':temp_tasks[i][5]}
				tasks.append(temp_task)
				++temp_count
				if temp_count==8:
					break
		tasks.sort(time_cmp,reverse=True)
	return tasks

def getAllTasksByUA(user_ac):
	temp_tasks = new_db.getTasksByUA(user_ac)
	temp_num = len(temp_tasks)
	tasks = []
	if temp_num>0:
		for i in range(temp_num):
			temp_task={'id':temp_tasks[i][0],'name':temp_tasks[i][2],
			'endline':temp_tasks[i][5],'status':temp_tasks[i][6]}
			tasks.append(temp_task)
		tasks.sort(time_cmp,reverse=True)
	return tasks

def getTasksByKeyWords(key_words,user_ac):
	temp_tasks = new_db.getTasksByUA(user_ac)
	temp_num = len(temp_tasks)
	tasks = []
	if temp_num>0:
		for i in range(temp_num):
			if temp_tasks[i][2].find(key_words,0)!=-1 or temp_tasks[i][3].find(key_words,0)!=-1:
				temp_task={'id':temp_tasks[i][0],'name':temp_tasks[i][2],
				'endline':temp_tasks[i][5],'status':temp_tasks[i][6]}
				tasks.append(temp_task)
		tasks.sort(time_cmp,reverse=True)
	return tasks

def isClose(birth):
	today_date = new_db.getDateTime().split('-',1)[1]
	birthday = birth.split('-',1)[1]
	#birthday:'1992-01-06',today_date:'1992-01-06'
	try:
		d1 = datetime.datetime.strptime(birthday, '%m-%d')
		d2 = datetime.datetime.strptime(today_date, '%m-%d')
		delta = d1 - d2
	except:
		return False
	if delta.days>=0 and delta.days<8:
		return True
	else:
		return False

def my_cmp(E1, E2):
	return cmp(E1['birthday'].split('-',1)[1], E2['birthday'].split('-',1)[1]) 

def getAllBirthPersonsByUA(user_ac):
	#在数据库中寻找所有的生日信息
	temp_persons = new_db.getBirthdaysByUA(user_ac)
	temp_num = len(temp_persons)
	persons = []
	if temp_num>0:
		for i in range(temp_num):
			temp_person={'id':temp_persons[i][1],'name':temp_persons[i][3],'birthday':temp_persons[i][2],
			'contact':temp_persons[i][4],'photo':temp_persons[i][5]}
			persons.append(temp_person)
	persons.sort(my_cmp)
	for temp_person in persons:
		if temp_person['birthday'].split('-',1)[0]=='0':
					temp_person['birthday'] = temp_person['birthday'].split('-',1)[1]
	return persons


def getBirthPersonsByUA(user_ac):
	#在数据库中寻找相应最近两天过生日的人(当前用户的朋友)的信息并添加到persons中
	temp_persons = new_db.getBirthdaysByUA(user_ac)
	temp_num = len(temp_persons)
	persons = []
	if temp_num>0:
		for i in range(temp_num):
			temp_person={'id':temp_persons[i][1],'name':temp_persons[i][3],'birthday':temp_persons[i][2],
			'contact':temp_persons[i][4],'photo':temp_persons[i][5]}
			if isClose(temp_person['birthday']):
				persons.append(temp_person)
	persons.sort(my_cmp)
	for temp_person in persons:
		if temp_person['birthday'].split('-',1)[0]=='0':
					temp_person['birthday'] = temp_person['birthday'].split('-',1)[1]
	return persons

def getBirthPersonById(person_id,userAccount):
	person = {'id':0,'name':'','year':'','month':'','day':'','contact':'',
		'photo':'../static/img/null_person_photo.jpg'}
	#安全措施:验证身份
	uid=new_db.getUidByUA(userAccount)
	person_ids = new_db.getPersonIdByUid(uid)
	temp_id = (person_id,)
	if person_id==0 or person_ids.count(temp_id)==0:
		pass
	else:
		temp_person = new_db.getBirthdayWholeInfo(person_id)
		if temp_person!=[]:
			temp_year = temp_person[0][2].split('-',2)[0]
			temp_month = temp_person[0][2].split('-',2)[1]
			temp_day = temp_person[0][2].split('-',2)[2]
			person = {'id':temp_person[0][1],'name':temp_person[0][3],'year':temp_year,
			'month':temp_month,'day':temp_day,'contact':temp_person[0][4],
			'photo':temp_person[0][5]}
	return person

#必要的全局变量
g_max_task_id = new_db.getMaxTaskID()
g_max_note_id = new_db.getMaxNoteID()
g_max_person_id = new_db.getMaxPersonID()
g_max_user_id = new_db.getMaxUserID()

@app.route('/',methods=['GET', 'POST'])
def homepage():

	#友情链接
	links = [
	{'name':'百度一下,你就知道','url':'http://www.baidu.com/'},
	{'name':'新浪微博','url':'http://www.weibo.com/'},
	{'name':'凤凰网','url':'http://www.ifeng.com/'},
	{'name':'面包网','url':'http://www.mianbao.com/'},
	{'name':'淘宝网','url':'http://www.taobao.com/'},
	{'name':'4399小游戏','url':'http://www.4399.com/'}
	]

	#--------------身份判断开始---------------
	if 'user_account' in request.cookies:
		cook1 = request.cookies.get('user_account')
		cook2 = request.cookies.get('user_password')
		if check_encrypted_Pwd(cook1, cook2):
			login_success = 1
			userAccount = cook1
		else:
			login_success = -1;
	else:
		login_success = 0;
	#--------------身份判断结束---------------

	if login_success == 1:
		#提交POST表单的情况
		if request.method=='POST':
			form_id = request.values['form_id']
			if form_id=='exit_login_form':
				resp = app.make_response(redirect(url_for('login')))
				resp.set_cookie('user_account',value='')
				resp.set_cookie('user_password',value='')
				return resp
			elif form_id=='note_form':
				content=request.values['my_note']
				new_db.updateNote(userAccount,content)
				#向数据库插入备忘录信息(sql)
				pass
			else:
				pass
		#提交GET表单的情况
		else:
			pass
		#开始渲染**************************************
		#读取头像
		my_photo = getPhotoByUserAccount(userAccount)
		#读取备忘录
		my_note = getNotesByUserAccount(userAccount)
		#未完成任务
		unfinish_tasks = getEightUnfinTasksByUA(userAccount)
		#今日任务
		today_tasks = getEightTodayTasksByUA(userAccount)
		#完成了的任务
		finished_tasks = getEightFinishedTasksByUA(userAccount)
		#生日提醒
		birthdayPersons = getBirthPersonsByUA(userAccount)

		#成功登录后的渲染***************************************************
		return render_template('main.html',userAccount = userAccount,
		my_photo = my_photo,my_note = my_note,links = links,
		unfinish_tasks = unfinish_tasks,finished_tasks = finished_tasks,
		today_tasks = today_tasks,birthdayPersons = birthdayPersons,
		len_of_birthdayPersons = len(birthdayPersons))
	else:
		return redirect(url_for('login'))

#登录页面
@app.route('/login',methods=['GET', 'POST'])
def login():
	if request.method=='POST':
		form_id = request.values['form_id']
		if form_id=='login_form':
			temp_userAccount = request.values['userAccount']
			temp_userPassword = request.values['userPassword']
			if checkUser_Pwd(temp_userAccount,temp_userPassword):
				#用户验证通过,登录成功
				login_success = 1
			else:
				#用户未通过验证,登录失败
				login_success = -1
		else:
			pass
		#表单判断完成,开始渲染或重定向
		if login_success==1:
			resp = app.make_response(redirect(url_for('homepage')))
			encrypt_pass = encrypt(temp_userPassword)
			resp.set_cookie('user_account',value=temp_userAccount)
			resp.set_cookie('user_password',value=encrypt_pass)
			return resp
		else:
			return render_template('login.html',login_success = login_success)
	else:
		return render_template('login.html')

#注册页面
@app.route('/register',methods=['GET', 'POST'])
def register():
	global g_max_user_id
	register_error = 0;
	register_account = '';
	register_password1 = '';
	register_password2 = '';

	if request.method=='POST':
		form_id = request.values['form_id']
		if form_id=='register_form':
			register_account = request.values['userAccount']
			register_password1 = request.values['userPassword1']
			register_password2 = request.values['userPassword2']
			register_error = checkRegister_Info(register_account,register_password1,
			register_password2)
		else:
			pass
		if register_error!=0:
			return render_template('register.html',register_error = register_error)
		else:
			#添加到数据库中(sql)
			g_max_user_id+=1
			new_db.registerNewUser(g_max_user_id,register_account,register_password1,
			"name","contact","../static/img/null_my_photo.jpg")
			resp = app.make_response(redirect(url_for('homepage')))
			encrypt_pass = encrypt(register_password1)
			resp.set_cookie('user_account',value=register_account)
			resp.set_cookie('user_password',value=encrypt_pass)
			return resp
	else:
		return render_template('register.html')

def isLegalTaskId(userAccount,task_id):
	res=True
	task_ids = new_db.getTasksIdByUA(userAccount)
	temp_id = (task_id,)
	if task_ids.count(temp_id)==0:
		res = False
	return res
#任务详情页面
@app.route('/singletask',methods=['GET', 'POST'])
@app.route('/newtask',methods=['GET', 'POST'])
def singletask():
	global g_max_task_id
	#--------------身份判断开始---------------
	if 'user_account' in request.cookies:
		cook1 = request.cookies.get('user_account')
		cook2 = request.cookies.get('user_password')
		if check_encrypted_Pwd(cook1, cook2):
			login_success = 1
			userAccount = cook1
		else:
			login_success = -1;
	else:
		login_success = 0;
	#--------------身份判断结束---------------
	if login_success==1:
		if request.method=='POST':
			form_id = request.values['form_id']
			if form_id=='singleTask_form':
				temp_id = request.values['single_task_id']
				currentTaskId = string.atoi(temp_id)
				single_task = getTaskById(currentTaskId,userAccount)
				return render_template('single_task.html',single_task = single_task)
			elif form_id=='task_save_mode_form':
				#将此任务保存到数据库中(sql),返回主页面
				task_error = ''
				if request.values['change_flag']=='true':
					task_error = '保存成功'
					#开始检测
					temp_id = request.values['task_id']
					task_id = string.atoi(temp_id)
					if task_id!=0 and not isLegalTaskId(userAccount,task_id):
						task_error='请不要修改js或html!';
					task_name = request.values['task_name']
					if task_name=='':
						task_error='任务名不能为空!';
					
					start_year = request.values['start_year']
					start_month = request.values['start_month']
					start_day = request.values['start_day']
					start_hour = request.values['start_hour']
					start_minute = request.values['start_minute']
					end_year = request.values['end_year']
					end_month = request.values['end_month']
					end_day = request.values['end_day']
					end_hour = request.values['end_hour']
					end_minute = request.values['end_minute']
					task_description = request.values['task_description']
					task_status = request.values['task_status']
					
					temp_timestamp = new_db.getTimeStamp()
					if start_year=='':
						start_year=temp_timestamp.split('-',1)[0]
					if start_month=='':
						start_month=temp_timestamp.split('-',2)[1]
					if start_day=='':
						start_day=temp_timestamp.split('_',1)[0].rsplit('-',1)[1]
					if start_hour=='':
						start_hour=temp_timestamp.split('_',1)[1].split(':',1)[0]
					if start_minute=='':
						start_minute=temp_timestamp.split(':',2)[1]
					start_second='00'
					if end_year=='':
						end_year=temp_timestamp.split('-',1)[0]
					if end_month=='':
						end_month=temp_timestamp.split('-',2)[1]
					if end_day=='':
						end_day=temp_timestamp.split('_',1)[0].rsplit('-',1)[1]
					if end_hour=='':
						end_hour=temp_timestamp.split('_',1)[1].split(':',1)[0]
					if end_minute=='':
						end_minute=temp_timestamp.split(':',2)[1]
					end_second='00'
					start_time=start_year+'-'+start_month+'-'+start_day+'_'\
						+start_hour+':'+start_minute+':'+start_second
					endLine=end_year+'-'+end_month+'-'+end_day+'_'\
						+end_hour+':'+end_minute+':'+end_second
					try:
						time.strptime(start_time,"%Y-%m-%d_%H:%M:%S")
						time.strptime(endLine,"%Y-%m-%d_%H:%M:%S")
					except:
						task_error='时间信息填写有误!'
					#update
					if endLine.rsplit(':',1)[0]==temp_timestamp.rsplit(':',1)[0]:
						endLine='2099-12-31_23:59:59'
					#update
					#检测结束
					if task_error == '保存成功':
						#将此任务保存到数据库中(sql),返回主页
						temp_id = request.values['task_id']
						task_id = string.atoi(temp_id)
						if task_id==0:
							task_id = g_max_task_id+1
							g_max_task_id+=1

						if temp_id=='0':
							#新任务
							new_db.InsertTask(task_id,userAccount,
							task_name,task_description,start_time,endLine,'false')
						else:
							new_db.updateTask(task_id,task_name,task_description,
							start_time,endLine)
						#保存结束
						return redirect(url_for('homepage'))
					else:
						pass
				else:
					pass
				temp_id = request.values['task_id']
				if temp_id!='0':
					task_id = string.atoi(temp_id)
				if task_id!=0 and not isLegalTaskId(userAccount,task_id):
					task_error='请不要修改js或html!'
					task_id=0
				single_task = getTaskById(task_id,userAccount)
				return render_template('single_task.html',single_task = single_task,
				task_error=task_error)
			elif form_id=='task_finish_mode_form':
				task_error='保存成功!'
				#检测start_year等信息,task_id和task_status要独立处理
				temp_id = request.values['task_id']
				task_id = string.atoi(temp_id)
				if task_id!=0 and not isLegalTaskId(userAccount,task_id):
					task_error = '请不要修改js或html!'
					task_id=0
					single_task = getTaskById(task_id,userAccount)
					return render_template('single_task.html',single_task = single_task,
					task_error=task_error)
				else:
					new_db.finishTask(task_id)
					return redirect(url_for('homepage'))
				#将此任务的状态改变保存到数据库中(sql)
			elif form_id=='task_del_mode_form':
				task_error='删除成功!'
				temp_id = request.values['task_id']
				task_id = string.atoi(temp_id)
				if task_id!=0 and not isLegalTaskId(userAccount,task_id):
					task_error = '请不要修改js或html!'
					task_id=0
					single_task = getTaskById(task_id,userAccount)
					return render_template('single_task.html',single_task = single_task,
					task_error=task_error)
				else:
					new_db.deleteTask(task_id)
					#将此任务在数据库中删除(sql),返回主页
					return redirect(url_for('homepage'))
		else:
			return redirect(url_for('homepage'))
	else:
		return redirect(url_for('login'))

#生日清单浏览网页
@app.route('/birthday_list',methods=['GET', 'POST'])
def birthday_list():
	#--------------身份判断开始---------------
	if 'user_account' in request.cookies:
		cook1 = request.cookies.get('user_account')
		cook2 = request.cookies.get('user_password')
		if check_encrypted_Pwd(cook1, cook2):
			login_success = 1
			userAccount = cook1
		else:
			login_success = -1;
	else:
		login_success = 0;
	#--------------身份判断结束---------------

	if login_success==1:
		if request.method=='POST':
			return redirect(url_for('homepage'))
		else:
			birth_persons = getAllBirthPersonsByUA(userAccount)
			return render_template('all_birthday.html',birth_persons = birth_persons)
	else:
		return redirect(url_for('login'))

PIC_KINDS = set(['jpg', 'jpeg','gif','png','bmp'])
def allowed_name(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in PIC_KINDS
def get_img_format(filename):
	return filename.rsplit('.', 1)[1]
def isLegalPersonId(uid,person_id):
	res=True
	if type(person_id)!=type(1):
		res=False
	else:
		person_ids = new_db.getPersonIdByUid(uid)
		temp_id = (person_id,)
		if person_ids.count(temp_id)==0:
			res = False
	return res

#生日详情界面
@app.route('/single_birthday',methods=['GET', 'POST'])
@app.route('/new_birthday',methods=['GET', 'POST'])
def singlebirthday():
	global g_max_person_id
	#--------------身份判断开始---------------
	if 'user_account' in request.cookies:
		cook1 = request.cookies.get('user_account')
		cook2 = request.cookies.get('user_password')
		if check_encrypted_Pwd(cook1, cook2):
			login_success = 1
			userAccount = cook1
		else:
			login_success = -1;
	else:
		login_success = 0;
	#--------------身份判断结束---------------
	if login_success==1:
		if request.method=='POST':
			form_id = request.values['form_id']
			if form_id=='single_birthday_form':
				temp_id = request.values['person_id']
				person_id = string.atoi(temp_id)
				person_info = getBirthPersonById(person_id,userAccount)
				return render_template('single_birthday.html',person_info = person_info)
			elif form_id=='birth_save_mode_form':
				#将此生日保存到数据库中(sql),继续留在此页
				birth_error = -1
				if request.values['change_flag']=='true':
					birth_error = 0
					uid=new_db.getUidByUA(userAccount)
					#开始检测
					photo_file = request.files['photo_file']
					if photo_file.filename=='':
						pass
					elif not allowed_name(photo_file.filename):
						birth_error=1
					temp_id = request.values['person_id']
					person_id = string.atoi(temp_id)
					if person_id!=0 and not isLegalPersonId(uid,person_id):
						birth_error=4
					person_name = request.values['person_name']
					if person_name=='':
						birth_error=2
					birth_year = request.values['birthday_year']
					birthday_month = request.values['birthday_month']
					birthday_day = request.values['birthday_day']
					
					if birth_year=='':
						birth_year = '1900'
					try:
						temp_time=birth_year+'-'+birthday_month+'-'+birthday_day
						time.strptime(temp_time,"%Y-%m-%d")
					except:
						birth_error=3
					#结束检测
					if birth_error == 0:
						#保存生日到数据库中(sql),返回主页面
						temp_id = request.values['person_id']
						person_id = string.atoi(temp_id)
						if person_id==0:
							person_id = g_max_person_id+1
							g_max_person_id+=1
						
						if  photo_file.filename!='':
							photo_file = request.files['photo_file']
							img_name = 'person_'+str(person_id)+'.'+get_img_format(photo_file.filename)
							temp_path = 'my_app/static/img/'+img_name
							photo_file.save(temp_path)
							new_photo = '../static/img/'+img_name
						else:
							new_photo=new_db.getPhotoByPersonId(person_id)
						birth_year = request.values['birthday_year']
						birthday_month = request.values['birthday_month']
						birthday_day = request.values['birthday_day']
						if birth_year=='':
							birth_year = '0'
						birthday=birth_year+'-'+birthday_month+'-'+birthday_day
						personName = request.values['person_name']
						contact=request.values['person_contact']
						if contact=='':
							contact='暂无联系方式'.decode("utf8")
						if string.atoi(temp_id)==0:
							new_db.insertBirthday(userAccount,person_id,birthday,
							personName,contact,new_photo)
						else:
							new_db.updateBirthday(person_id,birthday,personName,
							contact,new_photo)
						#保存结束
						return redirect(url_for('homepage'))
				else:
					pass
				if string.atoi(temp_id)!=0:
					person_id = string.atoi(temp_id)
				if person_id!=0 and not isLegalPersonId(uid,person_id):
					birth_error = 4
					person_id=0
				else:
					person_info = getBirthPersonById(person_id,userAccount)
				return render_template('single_birthday.html',person_info = person_info,
				birth_error = birth_error)
			elif form_id=='birth_del_mode_form':
				uid=new_db.getUidByUA(userAccount)
				temp_id = request.values['person_id']
				person_id = string.atoi(temp_id)
				if not isLegalPersonId(uid,person_id):
					pass
				else:
					new_db.deleteBirthday(person_id)
					#将此生日(person_id)删除(sql),返回主页
				return redirect(url_for('homepage'))
			else:
				return redirect(url_for('homepage'))
		else:
			return redirect(url_for('homepage'))
	else:
		return redirect(url_for('login'))

#通用任务浏览网页
@app.route('/search_results',methods=['GET', 'POST'])
@app.route('/task_list',methods=['GET', 'POST'])
def task_list():
	#--------------身份判断开始---------------
	if 'user_account' in request.cookies:
		cook1 = request.cookies.get('user_account')
		cook2 = request.cookies.get('user_password')
		if check_encrypted_Pwd(cook1, cook2):
			login_success = 1
			userAccount = cook1
		else:
			login_success = -1;
	else:
		login_success = 0;
	#--------------身份判断结束---------------
	if login_success==1:
		if request.method=='POST':
			form_id = request.values['form_id']
			if form_id=='search_form':
				key_words = request.values['search_key']
				tasks = getTasksByKeyWords(key_words,userAccount)
				return render_template('alltasks.html',tasks = tasks,
				task_list_mode='search_result')

			elif form_id=='task_list_form':
				task_list_mode = request.values['task_list_mode']
				if task_list_mode=='today':
					tasks = getAllTodayTasksByUA(userAccount)
					return render_template('alltasks.html',tasks = tasks,
					task_list_mode=task_list_mode)
				elif task_list_mode=='finished':
					tasks = getAllFinishedTasksByUA(userAccount)
					return render_template('alltasks.html',tasks = tasks,
					task_list_mode=task_list_mode)
				elif task_list_mode=='unfinish':
					tasks = getAllUnfinTasksByUA(userAccount)
					return render_template('alltasks.html',tasks = tasks,
					task_list_mode=task_list_mode)
				else:
					tasks = getAllTasksByUA(userAccount)
					return render_template('alltasks.html',tasks = tasks,
					task_list_mode=task_list_mode)
			else:
				return redirect(url_for('homepage'))
		else:
			return redirect(url_for('homepage'))
	else:
		return redirect(url_for('login'))

#账户设置界面
@app.route('/setting',methods=['GET', 'POST'])
def setting():
	#--------------身份判断开始---------------
	if 'user_account' in request.cookies:
		cook1 = request.cookies.get('user_account')
		cook2 = request.cookies.get('user_password')
		if check_encrypted_Pwd(cook1, cook2):
			login_success = 1
			userAccount = cook1
		else:
			login_success = -1;
	else:
		login_success = 0;
	#--------------身份判断结束---------------
	if login_success==1:
		if request.method=='POST':
			form_id = request.values['form_id']
			if form_id=='setting_form':
				setting_error = -1
				if request.values['change_flag']=='true':
					setting_error = 0
					change_pwd_flag = request.values['change_pwd_flag']
					
					uid=new_db.getUidByUA(userAccount)
					
					#开始判断
					photo_file = request.files['photo_file']
					if photo_file.filename=='':
						pass
					elif not allowed_name(photo_file.filename):
						setting_error=1
					new_account = request.values['my_account']
					if new_account==''\
					or new_account!=userAccount and new_db.getPwdByUA(new_account)!='':
						setting_error=2
					if change_pwd_flag=='true':
						orgin_password = request.values['orgin_password']
						new_password1 = request.values['new_password1']
						new_password2 = request.values['new_password2']
						#new_pwd=new_password1
						if orgin_password!=new_db.getPwdByUA(userAccount):
							setting_error=3
						elif new_password1=='' or new_password1!=new_password2:
							setting_error=4
					#判断结束

					if setting_error == 0:
						#保存设置到数据库中(sql),继续留在此页面
						if  photo_file.filename!='':
							photo_file = request.files['photo_file']
							img_name = 'user_'+str(uid)+'.'+get_img_format(photo_file.filename)
							temp_path = 'my_app/static/img/'+img_name
							photo_file.save(temp_path)
							new_photo = '../static/img/'+img_name
						else:
							new_photo=new_db.getAvatar(userAccount)
						if change_pwd_flag=='true':
							new_password = request.values['new_password1']
						else:
							new_password=new_db.getPwdByUA(userAccount)
						new_db.updateUser(uid,new_account,new_password,new_photo)
						#保存结束
						userAccount = new_account
						resp = app.make_response(render_template('setting.html',
						my_photo = new_photo,my_account = userAccount,
						setting_error = setting_error))
						encrypt_pass = encrypt(new_password)
						resp.set_cookie('user_account',value=new_account)
						resp.set_cookie('user_password',value=encrypt_pass)
						return resp
					else:
						pass
				else:
					pass
				#读取头像
				my_photo = getPhotoByUserAccount(userAccount)
				return render_template('setting.html',my_photo = my_photo,
				my_account = userAccount,setting_error = setting_error )
			else:
				pass
		else:
			#读取头像
			my_photo = getPhotoByUserAccount(userAccount)
			return render_template('setting.html',my_photo = my_photo,
			my_account = userAccount)
	else:
		return redirect(url_for('login'))
#清空数据库所有内容和cookies的地址(测试专用)
#@app.route('/clearall',methods=['GET', 'POST'])
#def clearall():
#	new_db.deleteAlluser()
#	resp = app.make_response(redirect(url_for('login')))
#	resp.set_cookie('user_account',value='')
#	resp.set_cookie('user_password',value='')
#	return redirect(url_for('login'))