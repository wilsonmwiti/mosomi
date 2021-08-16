from django.urls import path

from school import views

app_name = 'School'
urlpatterns = [
    path('home', views.home, name='home'),
    path('register', views.school_register, name='register'),
    path('login', views.school_login, name='login'),
    path('logout', views.school_logout, name='logout'),
    path('students/<int:stream_id>', views.school_students, name='school_students'),
    path('streams/<int:form_id>', views.school_streams, name='school_streams'),
    path('classes', views.school_classes, name='school_classes'),
    path('add_class', views.add_class, name='add_class'),
    path('edit_class/<int:class_id>', views.edit_class, name='edit_class'),
    path('add/stream/<int:class_id>', views.add_stream, name='add_stream'),
    path('edit/stream/<int:stream_id>', views.edit_stream, name='edit_stream'),
    path('add_student/<int:stream_id>', views.add_student, name='add_student'),
    # path('edit_student/<int:student_id>', vie/school/add/exam/ws.edit_student, name='edit_student'),
    path('add/guardian/<int:stream_id>', views.add_guardian, name='add_guardian'),
    path('add/term/<int:form_id>', views.add_term, name='add_term'),
    path('add/exam/<int:form_id>/<int:term_year_id>', views.add_exam, name='add_exam'),

    #examinations
    path('exam/classes', views.examination_classes, name='examination_classes'),
    path('exam/terms/<int:form_id>', views.examination_terms, name='examination_terms'),
    path('exam/exams/<int:term_year_id>/<int:form_id>', views.examinations_exam, name='examinations_exam'),
    path('exam/students/<int:form_id>/<int:exam_id>', views.examination_students, name='examination_students'),
    path('exam/subject/score/<int:student_id>/<int:exam_id>/<int:form_id>', views.student_subject_scores, name='student_subject_scores'),
    path('edit_student_score/<int:student_id>/<int:exam_id>/<int:subject_id>', views.edit_subject_score, name='edit_student_score'),
    path('final/score/<int:student_id>/<int:exam_id>', views.grade_student, name='grade_student'),
    #finance
    path('finance/classes', views.finance_classes, name='finance_classes'),
    path('finance/students/<int:class_id>', views.finance_students, name='finance_students'),
    path('finance/student/payments/<int:student_id>/<int:term_id>/<int:form_id>', views.finance_student_payments, name='finance_student_payments'),
    path('finance/student/add/payment/<int:student_id>/<int:term_id>/<int:form_id>', views.finance_add_payment, name='finance_add_payment'),
    path('payment/receipt/<int:student_fee_id>', views.payment_receipt_preview, name='payment_receipt_preview'),

    path('finance/years', views.finance_years, name='finance_years'),
    path('finance/term/years/<int:term_id>', views.school_term_years, name='school_term_years'),
    path('set_term_fee/<int:term_year_id>/<int:form_id>', views.set_term_fee, name='set_term_fee'),
    path('finance_classes/<int:term_year_id>', views.school_finance_classes, name='finance_classes'),
    path('add_fee_break_down/<int:term_year_id>', views.add_fee_break_down, name='add_fee_break_down'),

    path('finance_year_classes/<int:year>', views.finance_year_classes, name='finance_year_classes'),
    path('finance_terms/<int:form_id>/<int:year>', views.finance_terms, name='finance_terms'),

    #sms
    path('sms/menu', views.sms_menu, name='sms_menu'),
    path('personalized_sms_menu', views.personalized_sms_menu, name='personalized_sms_menu'),
    path('simple_sms', views.simple_sms, name='simple_sms'),
    path('personalized_from_file', views.personalized_from_file, name='personalized_from_file'),
    path('personalized_from_contact_group', views.personalized_from_contact_group, name='personalized_from_contact_group'),

    #reports
    path('generate_exam_results/<int:exam_id>', views.generate_exam_results, name='generate_exam_results_template'),

    # deletions
    path('delete_stream/<int:stream_id>', views.delete_stream, name='delete_stream'),
    path('delete_student/<int:student_id>', views.delete_student, name='delete_student'),
    path('delete_class', views.delete_class, name='delete_class'),

    #template
    path('exam/results/template/<int:exam_id>', views.download_exam_template, name='exam_results_template'),
    path('upload/exam/results/<int:exam_id>', views.upload_student_marks, name='upload_student_marks'),

    #settings
    path('settings', views.settings, name='settings'),
    path('term/years/<int:term_id>', views.term_years, name='term_years'),

    #new exams
    path('exam/years', views.exam_years, name='exam_years'),
    path('exam/forms/<int:year>', views.forms_by_year, name='forms_by_year'),
    path('exam/terms/<int:year>/<int:form_id>', views.exam_terms_by_year, name='exam_terms_by_year'),
]