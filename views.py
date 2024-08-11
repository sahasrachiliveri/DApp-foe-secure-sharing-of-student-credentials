from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import os
import json
from web3 import Web3, HTTPProvider
import ipfsApi
import os
from django.core.files.storage import FileSystemStorage
import pickle

global details, username, school_name, company_name
details=''
global contract

api = ipfsApi.Client(host='http://127.0.0.1', port=5001)

def readDetails(contract_type):
    global details
    details = ""
    print(contract_type+"======================")
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Student.json' #student contract code
    deployed_contract_address = '0x057805C973CcC8d919cc3E2f2F683BBa85c2B91C' #hash address to access student contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'schoolcompany':
        details = contract.functions.getSchoolCompany().call()
    if contract_type == 'enrollstudent':
        details = contract.functions.getStudent().call()
    if contract_type == 'credential':
        details = contract.functions.getCredential().call()
    if contract_type == 'accessrequest':
        details = contract.functions.getAccess().call()
    print(details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Student.json' #student contract file
    deployed_contract_address = '0x057805C973CcC8d919cc3E2f2F683BBa85c2B91C' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'schoolcompany':
        details+=currentData
        msg = contract.functions.addSchoolCompany(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'enrollstudent':
        details+=currentData
        msg = contract.functions.enrollStudent(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'credential':
        details+=currentData
        msg = contract.functions.setCredentialData(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)    
    if contract_type == 'accessrequest':
        details+=currentData
        msg = contract.functions.setAccessRequest(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)

def saveDataBlockChain1(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Student.json' #student contract file
    deployed_contract_address = '0x057805C973CcC8d919cc3E2f2F683BBa85c2B91C' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    if contract_type == 'credential':
        msg = contract.functions.setCredentialData(currentData).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)    
    

def StudentLoginAction(request):
    if request.method == 'POST':
        global details, username
        username = request.POST.get('username', False)
        readDetails('enrollstudent')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[1] == username:
                status = "success"
                break
        if status == "success":
            context= {'data':'Welcome '+username}
            return render(request, "StudentScreen.html", context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'StudentLogin.html', context)            

def CompanyLoginAction(request):
    if request.method == 'POST':
        global details, username, school_name, company_name
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        readDetails('schoolcompany')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'company' and array[4] == username and array[5] == password:
                status = "success"
                company_name = array[1]
                break
        if status == "success":
            context= {'data':'Welcome '+username}
            return render(request, "CompanyScreen.html", context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'CompanyLogin.html', context)

def SchoolLoginAction(request):
    if request.method == 'POST':
        global details, username, school_name, company_name
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        readDetails('schoolcompany')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            print(array)
            if array[0] == 'school' and array[4] == username and array[5] == password:
                status = "success"
                school_name = array[1]
                break
        if status == "success":
            context= {'data':'Welcome '+username}
            return render(request, "SchoolScreen.html", context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'SchoolLogin.html', context)

def UploadCertificate(request):
    if request.method == 'GET':
       return render(request, 'UploadCertificate.html', {})

def UpdateCertificate(request):
    if request.method == 'GET':
       return render(request, 'UpdateCertificate.html', {})    

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def EnrollStudent(request):
    if request.method == 'GET':
       return render(request, 'EnrollStudent.html', {})    

def SchoolLogin(request):
    if request.method == 'GET':
       return render(request, 'SchoolLogin.html', {})

def CompanyLogin(request):
    if request.method == 'GET':
       return render(request, 'CompanyLogin.html', {})    

def StudentLogin(request):
    if request.method == 'GET':
       return render(request, 'StudentLogin.html', {})

def SchoolSignup(request):
    if request.method == 'GET':
       return render(request, 'SchoolSignup.html', {})

def CompanySignup(request):
    if request.method == 'GET':
       return render(request, 'CompanySignup.html', {})


def SchoolSignupAction(request):
    if request.method == 'POST':
        global details
        school = request.POST.get('t1', False)
        address = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        user = request.POST.get('t4', False)
        password = request.POST.get('t5', False)
        readDetails('schoolcompany')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[1] == school:
                status = school+" School name already exists"
                break
            if array[4] == user:
                status = user+" Username already exists"
                break
        if status == "none":
            data = "school#"+school+"#"+address+"#"+contact+"#"+user+"#"+password+"\n"
            saveDataBlockChain(data,"schoolcompany")
            context = {"data":"School signup task completed"}
            return render(request, 'SchoolSignup.html', context)
        else:
            context = {"data":status}
            return render(request, 'SchoolSignup.html', context)
                               
def CompanySignupAction(request):
    if request.method == 'POST':
        global details
        company = request.POST.get('t1', False)
        address = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        user = request.POST.get('t4', False)
        password = request.POST.get('t5', False)
        readDetails('schoolcompany')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[4] == user:
                status = user+" Username already exists"
                break
        if status == "none":
            data = "company#"+company+"#"+address+"#"+contact+"#"+user+"#"+password+"\n"
            saveDataBlockChain(data,"schoolcompany")
            context = {"data":"Company signup task completed"}
            return render(request, 'CompanySignup.html', context)
        else:
            context = {"data":status}
            return render(request, 'CompanySignup.html', context)            
                
def ViewStudents(request):
    if request.method == 'GET':
        global details, username, school_name
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="white">'
        arr = ['School Name','Student ID','Student Name','School Details','Course Name','Joining Date']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('enrollstudent')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            print(arr[i])
            array = arr[i].split("#")
            output += "<tr><td>"+font+array[0]+"</td>"
            output += "<td>"+font+array[1]+"</td>"
            output += "<td>"+font+array[2]+"</td>"
            output += "<td>"+font+array[3]+"</td>"
            output += "<td>"+font+array[4]+"</td>"
            output += "<td>"+font+array[5]+"</td>"
        context= {'data':output}        
        return render(request, 'ViewStudents.html', context)            
        
def EnrollStudentAction(request):
    if request.method == 'POST':
        global details, username, school_name
        sid = request.POST.get('t1', False)
        sname = request.POST.get('t2', False)
        school_details = request.POST.get('t3', False)
        course = request.POST.get('t4', False)
        joining_date = request.POST.get('t5', False)
        
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == sid:
                status = sid+" Student ID already exists"
                break
        if status == "none":
            details = ""
            data = school_name+"#"+sid+"#"+sname+"#"+school_details+"#"+course+"#"+joining_date+"\n"
            saveDataBlockChain(data,"enrollstudent")
            context = {"data":"New Student Enrollment Task Completed"}
            return render(request, 'EnrollStudent.html', context)
        else:
            context = {"data":status}
            return render(request, 'EnrollStudent.html', context)


def UploadCertificateAction(request):
    if request.method == 'POST':
        global details, username, school_name
        sid = request.POST.get('t1', False)
        certificate = request.POST.get('t2', False)
        issue_date = request.POST.get('t3', False)
        filename = request.FILES['t4'].name
        myfile = request.FILES['t4'].read()
        myfile = pickle.dumps(myfile)
        hashcode = api.add_pyobj(myfile)
        #readDetails('credential')
        data = school_name+"#"+sid+"#"+certificate+"#"+issue_date+"#"+filename+"#"+hashcode+"\n"
        saveDataBlockChain(data,"credential")
        context = {"data":"Certificate saved on IPFS with hashcode saving in Blockchain: "+hashcode}
        return render(request, 'UploadCertificate.html', context)

def UpdateCertificateAction(request):
    if request.method == 'POST':
        global details, username, school_name
        sid = request.POST.get('t1', False)
        certificate = request.POST.get('t2', False)
        issue_date = request.POST.get('t3', False)
        filename = request.FILES['t4'].name
        myfile = request.FILES['t4'].read()
        myfile = pickle.dumps(myfile)
        hashcode = api.add_pyobj(myfile)
        readDetails('credential')
        data = ""
        credential = details.split("\n")
        for i in range(len(credential)-1):
            array = credential[i].split("#")
            if array[1] != sid:
                data += credential[i]+"\n"
        data += school_name+"#"+sid+"#"+certificate+"#"+issue_date+"#"+filename+"#"+hashcode+"\n"
        saveDataBlockChain1(data,"credential")
        context = {"data":"Modified certificate saved on IPFS with hashcode saving in Blockchain: "+hashcode}
        return render(request, 'UpdateCertificate.html', context)    
    

def SendAccessRequest(request):
    if request.method == 'GET':
        global details, username, school_name
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="white">'
        arr = ['School Name','Student ID','Student Name','School Details','Course Name','Joining Date','Send Access Request']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('enrollstudent')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            output += "<tr><td>"+font+array[0]+"</td>"
            output += "<td>"+font+array[1]+"</td>"
            output += "<td>"+font+array[2]+"</td>"
            output += "<td>"+font+array[3]+"</td>"
            output += "<td>"+font+array[4]+"</td>"
            output += "<td>"+font+array[5]+"</td>"
            output+='<td><a href=\'SendRequest?t1='+array[1]+'\'><font size=3 color=white>Click Here</font></a></td></tr>'
        context= {'data':output}        
        return render(request, 'SendAccessRequest.html', context) 

def SendRequest(request):
    if request.method == 'GET':
        global details, username, company_name
        sid = request.GET.get('t1', False)
        
        saveDataBlockChain(data,"accessrequest")
        context = {"data":"Access Request sent to student: "+sid}
        return render(request, 'SendAccessRequest.html', context)

def checkAccess(credential_arr, sid):
    status = False
    for i in range(len(credential_arr)-1):
        arr = credential_arr[i].split("#")
        if arr[0] == sid and arr[1] == company_name and arr[2] == "Accepted":
            status = True
            break
    return status    

def AccessCertificate(request):
    if request.method == 'GET':
        global details, username, company_name
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="white">'
        arr = ['School Name','Student ID','Certificate Details','Issue Date','File Name','Hashcode','Certificate']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('accessrequest')
        credential_arr = details.split("\n")
        readDetails('credential')
        access_certificate = details.split("\n")
        for i in range(len(access_certificate)-1):
            array = access_certificate[i].split("#")
            status = checkAccess(credential_arr, array[1])
            if status == True:
                output += "<tr><td>"+font+array[0]+"</td>"
                output += "<td>"+font+array[1]+"</td>"
                output += "<td>"+font+array[2]+"</td>"
                output += "<td>"+font+array[3]+"</td>"
                output += "<td>"+font+array[4]+"</td>"
                output += "<td>"+font+array[5]+"</td>"
                content = api.get_pyobj(array[5])
                content = pickle.loads(content)
                if os.path.exists('C:/Users/hp/OneDrive/Desktop/14/Blockchain/StudentCredentialBlockchain/certificate_templates'+array[4]):
                    os.remove('C:/Users/hp/OneDrive/Desktop/14/Blockchain/StudentCredentialBlockchain/certificate_templates'+array[4])
                with open('C:/Users/hp/OneDrive/Desktop/14/Blockchain/StudentCredentialBlockchain/certificate_templates'+array[4], "wb") as file:
                    file.write(content)
                file.close()
                output+='<td><img src=static/certificates/'+array[4]+'  width=400 height=400></img></td>'    
        context= {'data':output}        
        return render(request, 'AccessCertificate.html', context) 

def ViewDetails(request):
    if request.method == 'GET':
        global details, username
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="white">'
        arr = ['School Name','Student ID','Student Name','School Details','Course Name','Joining Date']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('enrollstudent')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[1] == username:
                output += "<tr><td>"+font+array[0]+"</td>"
                
                output += "<td>"+font+array[2]+"</td>"
                output += "<td>"+font+array[3]+"</td>"
                output += "<td>"+font+array[4]+"</td>"
                output += "<td>"+font+array[5]+"</td>"
        context= {'data':output}        
        return render(request, 'ViewDetails.html', context)  


def AccessOwnCertificate(request):
    if request.method == 'GET':
        global details, username
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="white">'
        arr = ['School Name','Student ID','Certificate Details','Issue Date','File Name','Hashcode','Certificate']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('credential')
        access_certificate = details.split("\n")
        for i in range(len(access_certificate)-1):
            array = access_certificate[i].split("#")
            if array[1] == username:
                output += "<tr><td>"+font+array[0]+"</td>"
                output += "<td>"+font+array[1]+"</td>"
                output += "<td>"+font+array[2]+"</td>"
                output += "<td>"+font+array[3]+"</td>"
                output += "<td>"+font+array[4]+"</td>"
                output += "<td>"+font+array[5]+"</td>"
                content = api.get_pyobj(array[5])
                content = pickle.loads(content)
                if os.path.exists('C:/Users/hp/OneDrive/Desktop/14/Blockchain/StudentCredentialBlockchain/certificate_templates'+array[4]):
                    os.remove('C:/Users/hp/OneDrive/Desktop/14/Blockchain/StudentCredentialBlockchain/certificate_templates'+array[4])
                with open('C:/Users/hp/OneDrive/Desktop/14/Blockchain/StudentCredentialBlockchain/certificate_templates'+array[4], "wb") as file:
                    file.write(content)
                file.close()
                output+='<td><img src=static/certificates/'+array[4]+'  width=400 height=400></img></td>'    
        context= {'data':output}        
        return render(request, 'AccessOwnCertificate.html', context)



def GrantAccess(request):
    if request.method == 'GET':
        global details, username
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="white">'
        arr = ['Student ID','Company Name','Access Status','Grant Access']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('accessrequest')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == username:
                
                output += "<td>"+font+array[1]+"</td>"
                output += "<td>"+font+array[2]+"</td>"
                output+='<td><a href=\'GrantAccessAction?t1='+array[0]+'&t2='+array[1]+'\'><font size=3 color=white>Click Here</font></a></td></tr>'
        context= {'data':output}        
        return render(request, 'GrantAccess.html', context)  

def GrantAccessAction(request):
    if request.method == 'GET':
        global details, username, company_name
        sid = request.GET.get('t1', False)
        company = request.GET.get('t2', False)
        data = ""
        readDetails('accessrequest')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] != sid and array[1] != company:
                data+=array[0]+"#"+array[1]+"#"+array[2]+"\n"
        data+=sid+"#"+company+"#Accepted\n"
        saveDataBlockChain(data,"accessrequest")
        context = {"data":"Access Request granted to company: "+company}
        return render(request, 'StudentScreen.html', context)
        










        

