from flask_restx import Resource, Namespace, abort

from .api_models import course_model, student_model, add_course, add_student
from .extensions import db
from .models import Course, Student


ns = Namespace("api")

@ns.route("/hello")
class Hello(Resource):
    def get(self):
        return {"hello": "restx"}



@ns.route("/courses")
class CourseListAPI(Resource):
    #Get the full JSON of students from the db
    @ns.marshal_list_with(course_model)
    def get(self):
        return Course.query.all()

    #Add a new course to the db through the API 
    @ns.expect(add_course)
    @ns.marshal_with(course_model)
    def post(self):
        print(ns.payload)
        course = Course(name=ns.payload["name"])
        db.session.add(course)
        db.session.commit()
        return course, 201


@ns.route("/courses/<int:id>")
class CourseAPI(Resource):

    #Quote a course where the id = input
    @ns.marshal_with(course_model)
    def get(self, id):
        course = Course.query.get(id)
        return course 

    #Edit a course where the ID == input
    @ns.expect(add_course)
    @ns.marshal_with(course_model)
    def put(self, id):
        course = Course.query.get(id)
        course.name = ns.payload["name"]
        db.session.commit()
        return course, 201 

    #Deletes a course where the ID == input
    def delete(self, id):
        course = Course.query.get(id)
        db.session.delete(course)
        db.session.commit()
        return {}, 204



      
@ns.route("/students")
class StudentListAPI(Resource):
    #Get the full JSON of students from the db
    @ns.marshal_list_with(student_model)
    def get(self):
        return Student.query.all()

    #Add a new student to the db through the API 
    @ns.expect(add_student)
    @ns.marshal_with(student_model)
    def post(self):
        student = Student(name=ns.payload["name"], course_id=ns.payload["course_id"])
        db.session.add(student)
        db.session.commit()
        return student, 201        

@ns.route("/students/<int:id>")
class StudentAPI(Resource):
    #Search a student where the id num == input 
    @ns.marshal_with(student_model)
    def get(self, id):
        student = Student.query.get(id)
        return student 
    
    #Edit a student where the ID == input
    @ns.expect(add_student)
    @ns.marshal_with(student_model)
    def put(self, id):
        student = Student.query.get(id)
        student.name = ns.payload["name"]
        student.course_id = ns.payload["course_id"]
        db.session.commit()
        return student, 201 

    #Deletes a student where the ID == input
    def delete(self, id):
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()
        return {}, 204






#De lo que me he dado cuenta que pueden haber muchos errores, como que el usuario busca un numero incorrecto, o que el usuario agrega string donde haya un int
