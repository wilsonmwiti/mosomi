from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models


class School(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    school_type = models.CharField(max_length=250)
    logo = models.ImageField(default='media/school_logos')
    primary_color = models.CharField(default='#005522', max_length=250)
    created_at = models.DateField(auto_now_add=True)


class SchoolAdmin(get_user_model()):
    phone_number = models.CharField(max_length=250)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


class Form(models.Model):
    name = models.CharField(max_length=250)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


class FormYear(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    year = models.DateField(auto_now_add=True)


class Stream(models.Model):
    name = models.CharField(max_length=250)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)


class Guardian(models.Model):
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=250)


class SubjectGroup(models.Model):
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Subject(models.Model):
    name = models.CharField(max_length=250)
    # school = models.ForeignKey(School, on_delete=models.CASCADE)
    subject_group = models.ForeignKey(SubjectGroup, on_delete=models.CASCADE)


class Student(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    student_image = models.ImageField(upload_to='media/student_images', blank=True)
    admission_number = models.IntegerField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    guardian = models.ForeignKey(Guardian, null=True, on_delete=models.CASCADE)

    def score_rank(self, exam_id):
        rank = 0
        exam = Exam.objects.filter(id=exam_id).first()
        student_forms = StudentForm.objects.filter(form_id=exam.form_id, is_current=True)
        students = []
        for student_form in student_forms:
            students.append(student_form.student)

        student_scores = []
        rank_score = 0
        student_subject_scores = ExamStudentSubjectScore.objects.filter(exam_id=exam_id, student_id=self.id)
        if student_subject_scores is not None:
            for score in student_subject_scores:
                rank_score += score.score

        for student in list(set(students)):
            final_score = 0
            subject_scores = ExamStudentSubjectScore.objects.filter(exam_id=exam_id, student_id=student.id)
            for score in subject_scores:
                final_score += score.score
            student_scores.append(final_score)

        rank = sorted(student_scores, reverse=True).index(rank_score) + 1
        return rank


class Term(models.Model):
    name = models.CharField(max_length=250)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


class TermYear(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)


class Fee(models.Model):
    fee = models.DecimalField(max_digits=65, decimal_places=2)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    term_year = models.ForeignKey(TermYear, on_delete=models.CASCADE)


class FeeBreakDown(models.Model):
    name = models.CharField(max_length=250)
    percentage = models.DecimalField(max_digits=10, decimal_places=2)
    term_year = models.ForeignKey(TermYear, on_delete=models.CASCADE)


class Teacher(get_user_model()):
    phone_number = models.CharField(max_length=250)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


class StudentForm(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    is_current = models.BooleanField(default=False)
    year = models.CharField(max_length=250)


class StudentFormSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class StudentStream(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)


class StudentFee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    term_year = models.ForeignKey(TermYear, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=65,decimal_places=2)
    date_paid = models.DateField(null=True)


class StudentTerm(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    term_year = models.ForeignKey(TermYear, on_delete=models.CASCADE)
    # is_current = models.BooleanField(default=False)


class Exam(models.Model):
    term_year = models.ForeignKey(TermYear, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    def sorted_students(self):
        student_total_score = {}
        sorted_students = []
        student_forms = StudentForm.objects.filter(form_id=self.form_id, is_current=True)
        students = []
        for student_form in student_forms:
            students.append(student_form.student)

        for student in list(set(students)):
            final_score = 0
            subject_scores = ExamStudentSubjectScore.objects.filter(exam_id=self.id, student_id=student.id)
            for score in subject_scores:
                final_score += score.score
            student_total_score[student.id] = final_score
        sorted_student_total_score = sorted(student_total_score.items(), key=lambda kv: kv[1], reverse=True)

        # print(students)
        for item in sorted_student_total_score:
            student = Student.objects.filter(id=item[0]).first()
            if student is not None:
                sorted_students.append(student)
        print(sorted_students)
        return sorted_students


class ExamStudentSubjectScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=65,decimal_places=2)
    grade = models.CharField(max_length=2)


class FormSubject(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


# class Teacher(get_user_model()):
#     phone_number = models.CharField(max_length=250)





