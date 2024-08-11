from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
		path("SchoolSignup.html", views.SchoolSignup, name="SchoolSignup"),
		path("SchoolSignupAction", views.SchoolSignupAction, name="SchoolSignupAction"),
	        path("SchoolLogin.html", views.SchoolLogin, name="SchoolLogin"),
	        path("CompanyLogin.html", views.CompanyLogin, name="CompanyLogin"),
	        path("StudentLogin.html", views.StudentLogin, name="StudentLogin"),
	        path("SchoolLoginAction", views.SchoolLoginAction, name="SchoolLoginAction"),
	        path("CompanyLoginAction", views.CompanyLoginAction, name="CompanyLoginAction"),
	        path("StudentLoginAction", views.StudentLoginAction, name="StudentLoginAction"),
	
		path("EnrollStudent.html", views.EnrollStudent, name="EnrollStudent"),
		path("EnrollStudentAction", views.EnrollStudentAction, name="EnrollStudentAction"),
		path("UploadCertificate.html", views.UploadCertificate, name="UploadCertificate"),
		path("UploadCertificateAction", views.UploadCertificateAction, name="UploadCertificateAction"),
		path("ViewStudents", views.ViewStudents, name="ViewStudents"),
		path("SendAccessRequest", views.SendAccessRequest, name="SendAccessRequest"),
		
		path("AccessCertificate", views.AccessCertificate, name="AccessCertificate"),
		path("ViewDetails", views.ViewDetails, name="ViewDetails"),
		path("AccessOwnCertificate", views.AccessOwnCertificate, name="AccessOwnCertificate"),
		path("GrantAccess", views.GrantAccess, name="GrantAccess"),
		path("GrantAccessAction", views.GrantAccessAction, name="GrantAccessAction"),
		path("UpdateCertificate.html", views.UpdateCertificate, name="UpdateCertificate"),
		path("UpdateCertificateAction", views.UpdateCertificateAction, name="UpdateCertificateAction"),
]
