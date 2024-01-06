from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import Candidate, Instructor, Course, expense
from sqlalchemy import inspect
from app import db

views = Blueprint('views', __name__)

@views.route("/test")
def test():
    d = Course.query.get(1)
    return jsonify(d.to_dict())

@views.route('/')
@login_required
def home():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    return redirect(url_for('auth.login'))


@views.route('/candidate/<int:id>/update', methods=['GET', 'POST', 'PUT'])
@login_required
def update_candidate(id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    instance = Candidate.query.get(id)
    if not instance:
        flash('Candidate does not exist', category="Error")
        return redirect(url_for('views.candidate'))
    if request.method == "POST":
        instance.firstname = request.form.get('firstname')
        instance.lastname = request.form.get('lastname')
        instance.email = request.form.get('email')
        instance.select_course = request.form.get('select_course')
        instance.birthdate = request.form.get('birthdate')
        instance.birthplace = request.form.get('birthplace')
        instance.telephone = request.form.get('telephone')
        instance.nationality = request.form.get('nationality')
        instance.cin_passport = request.form.get('cin_passport')
        instance.address = request.form.get('address')
        instance.gradelevel = request.form.get('gradelevel')
        db.session.commit()
        flash("Candidate updated successfully", category="Success")
        return redirect(url_for('views.candidate'))

    return render_template("update-candidate.html", tmp=instance)


@views.route('/instructor/<int:id>/update', methods=['GET', 'POST', 'PUT'])
@login_required
def update_instructor(id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    instance = Instructor.query.get(id)
    if not instance:
        flash('Instructor does not exist', category="Error")
        return redirect(url_for('views.instructor'))
    if request.method == "POST":
        instance.firstname1 = request.form.get('firstname1')
        instance.lastname1 = request.form.get('lastname1')
        instance.email = request.form.get('email')
        instance.course = request.form.get('select_course')
        instance.birthdate1 = request.form.get('birthdate1')
        instance.birthplace1 = request.form.get('birthplace1')
        instance.telephone1 = request.form.get('telephone1')
        instance.nationality1 = request.form.get('nationality1')
        instance.cin_passport1 = request.form.get('cin_passport1')
        instance.address = request.form.get('address')
        instance.select_payment = request.form.get('select_payment')
        db.session.commit()
        flash("Instructor updated successfully", category="Success")
        return redirect(url_for('views.instructor'))

    return render_template("update-instructor.html", tmp=instance)


@views.route('/course/<int:id>/update', methods=['GET', 'POST', 'PUT'])
@login_required
def update_course(id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    instance = Course.query.get(id)
    if not instance:
        flash('Course does not exist', category="Error")
        return redirect(url_for('views.course'))
    if request.method == "POST":
        instance.name = request.form.get('coursename')
        instance.length = request.form.get('length')
        db.session.commit()
        flash("Course updated successfully", category="Success")
        return redirect(url_for('views.course'))

    return render_template("update-course.html", tmp=instance)


@views.route('/course', methods=['GET', 'POST'])
@login_required
def course():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if request.method == "POST":
        search_term = request.form.get('search_term', '')
        results = []

        if search_term:
            # Get all columns of the Person model
            columns = [column.key for column in inspect(Course).c]

            # Construct the search query dynamically
            query = db.session.query(Course).filter(
                db.or_(
                    *[getattr(Course, column).like(f'%{search_term}%') for column in columns])
            )
            results = query.all()
        else:
            results = Course.query.all()

        # Convert the search results to a list of dictionaries
        results = [result.to_dict() for result in results]

        return jsonify(results)

    results = Course.query.all()
    results = [result.to_dict() for result in results]
    return render_template("course.html", results=results)


@views.route('/instructor', methods=['GET', 'POST'])
@login_required
def instructor():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if request.method == "POST":
        search_term = request.form.get('search_term', '')
        results = []

        if search_term:
            # Get all columns of the Person model
            columns = [column.key for column in inspect(Instructor).c]

            # Construct the search query dynamically
            query = db.session.query(Instructor).filter(
                db.or_(
                    *[getattr(Instructor, column).like(f'%{search_term}%') for column in columns])
            )
            results = query.all()
        else:
            results = Instructor.query.all()

        # Convert the search results to a list of dictionaries
        results = [result.to_dict() for result in results]

        return jsonify(results)

    results = Instructor.query.all()
    results = [result.to_dict() for result in results]
    return render_template("instructor.html", results=results)


@views.route('/candidate', methods=['GET', 'POST'])
@login_required
def candidate():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if request.method == "POST":
        search_term = request.form.get('search_term', '')
        results = []

        if search_term:
            # Get all columns of the Person model
            columns = [column.key for column in inspect(Candidate).c]

            # Construct the search query dynamically
            query = db.session.query(Candidate).filter(
                db.or_(
                    *[getattr(Candidate, column).like(f'%{search_term}%') for column in columns])
            )
            results = query.all()
        else:
            results = Candidate.query.all()

        # Convert the search results to a list of dictionaries
        results = [result.to_dict() for result in results]

        return jsonify(results)

    results = Candidate.query.all()
    results = [result.to_dict() for result in results]
    return render_template("candidate.html", results=results)


@views.route('/dashboard', methods=['GET', 'POST',])
@login_required
def dashboard():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    return redirect(url_for('auth.login'))


@views.route('/HR', methods=['GET', 'POST'])
@login_required
def HR():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        if request.form['form-name'] == 'candidate':
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            email = request.form.get('email')
            select_course = request.form.get('select_course')
            birthdate = request.form.get('birthdate')
            birthplace = request.form.get('birthplace')
            telephone = request.form.get('telephone')
            nationality = request.form.get('nationality')
            cin_passport = request.form.get('cin_passport')
            address = request.form.get('address')
            gradelevel = request.form.get('gradelevel')

            if len(firstname) < 2:
                flash('First name must have more than 2 characters.',
                      category="Error")
                return redirect(url_for('views.HR'))
            elif len(lastname) < 2:
                flash('Last name must have more than 2 characters.',
                      category='Error')
                return redirect(url_for('views.HR'))
            elif not select_course:
                flash('Username must have more than 2 characters.', category='Error')
                return redirect(url_for('views.HR'))
            elif len(email) < 2:
                flash('Email must have more than 4 characters.', category='Error')
                return redirect(url_for('views.HR'))
            elif len(birthdate) < 7:
                flash('Birthdate is not complete', category='Error')
                return redirect(url_for('views.HR'))
            elif len(birthplace) < 1:
                flash('Birthplace is not complete', category='Error')
                return redirect(url_for('views.HR'))
            elif len(str(telephone)) != 8:
                flash(
                    'Phone number cannot contain more or less than 8 number', category='Error')
                return redirect(url_for('views.HR'))
            elif len(nationality) < 2:
                flash('please provide the nationality', category='Error')
                return redirect(url_for('views.HR'))
            elif not cin_passport:
                flash('Please provide a CIN number or you passport number',
                      category='Error')
                return redirect(url_for('views.HR'))
            elif not address:
                flash('Please provide the full address', category='Error')
                return redirect(url_for('views.HR'))
            elif not gradelevel:
                flash('Please provide your educational grade level',
                      category='Error')
                return redirect(url_for('views.HR'))
            else:
                if Candidate.query.filter_by(email=email).first():
                    flash('This email is associated to another candidate',
                          category='Error')
                    return redirect(url_for('views.HR'))
                new_candidate = Candidate(firstname=firstname, lastname=lastname, email=email, select_course=select_course, birthdate=birthdate,
                                          birthplace=birthplace, telephone=telephone, nationality=nationality, cin_passport=cin_passport, address=address, gradelevel=gradelevel)
                db.session.add(new_candidate)
                db.session.commit()
                flash('Candidate successfully added', category='Success')
                return redirect(url_for('views.candidate'))

        elif request.form['form-name'] == 'instructor':
            firstname1 = request.form.get('firstname1')
            lastname1 = request.form.get('lastname1')
            email1 = request.form.get('email1')
            course = request.form.get('select_course1')
            birthdate1 = request.form.get('birthdate1')
            birthplace1 = request.form.get('birthplace1')
            telephone1 = request.form.get('telephone1')
            nationality1 = request.form.get('nationality1')
            cin_passport1 = request.form.get('cin_passport1')
            address1 = request.form.get('address1')
            select_payment = request.form.get('select_payment')

            if len(firstname1) < 2:
                flash('First name must have more than 2 characters.',
                      category="Error")
                return redirect(url_for('views.HR'))
            elif len(lastname1) < 2:
                flash('Last name must have more than 2 characters.',
                      category='Error')
                return redirect(url_for('views.HR'))
            elif not course:
                flash('Username must have more than 2 characters.', category='Error')
                return redirect(url_for('views.HR'))
            elif not select_payment:
                flash('Instructors must have a payment method', category='Error')
                return redirect(url_for('views.HR'))
            elif len(email1) < 2:
                flash('Email must have more than 4 characters.', category='Error')
                return redirect(url_for('views.HR'))
            elif len(birthdate1) < 7:
                flash('Birthdate is not complete', category='Error')
                return redirect(url_for('views.HR'))
            elif len(birthplace1) < 1:
                flash('Birthplace is not complete', category='Error')
                return redirect(url_for('views.HR'))
            elif len(str(telephone1)) != 8:
                flash(
                    'Phone number cannot contain more or less than 8 number', category='Error')
                return redirect(url_for('views.HR'))
            elif len(nationality1) < 2:
                flash('please provide the nationality', category='Error')
                return redirect(url_for('views.HR'))
            elif not cin_passport1:
                flash('Please provide a CIN number or you passport number',
                      category='Error')
                return redirect(url_for('views.HR'))
            elif not address1:
                flash('Please provide the full address', category='Error')
                return redirect(url_for('views.HR'))
            else:
                if Instructor.query.filter_by(email=email1).first():
                    flash('This email is associated to another instructor',
                          category='Error')
                    return redirect(url_for('views.HR'))
                new_instructor = Instructor(firstname1=firstname1, lastname1=lastname1, email=email1, course=course, birthdate1=birthdate1, birthplace1=birthplace1,
                                            telephone1=telephone1, nationality1=nationality1, cin_passport1=cin_passport1, address=address1, select_payment=select_payment)
                db.session.add(new_instructor)
                db.session.commit()
                flash('Instructor successfully added', category='Success')
                return redirect(url_for('views.instructor'))

        elif request.form['form-name'] == 'course':
            name, length = request.form.get(
                "coursename"), request.form.get("length")
            if Course.query.filter_by(name=name).first():
                flash('This course already exists',
                      category='Error')
                return redirect(url_for('views.HR'))
            course = Course(name=name, length=length)
            db.session.add(course)
            db.session.commit()
            flash('Course successfully added', category='Success')
            return redirect(url_for('views.course'))

    return render_template('HR.html')

@views.route("/expense", methods=['GET', 'POST'])
@login_required
def Expense():
    if not current_user.is_authenticated:
        return render_template('auth.login')
    if request.method == 'POST':
        amount = request.form.get('amount')
        type = request.form.get('type')
        category = request.form.get('category')

        if int(amount) <= 0:
            flash('Amount added must be greater than zero', category="Error")
            return redirect(url_for('views.Expense'))

        new_expense = expense(amount=amount, type=type, category=category)
        db.session.add(new_expense)
        db.session.commit()
        flash('Amount added!', category='success')
        return redirect(url_for('views.Expensetable'))
    expenses = expense.query.all()
    return render_template('expense.html', expenses=expenses)
@views.route("/expensetable")
@login_required
def Expensetable():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if request.method == "POST":
        search_term = request.form.get('search_term', '')
        results = []

        if search_term:
            # Get all columns of the Person model
            columns = [column.key for column in inspect(expense).c]

            # Construct the search query dynamically
            query = db.session.query(expense).filter(
                db.or_(
                    *[getattr(expense, column).like(f'%{search_term}%') for column in columns])
            )
            results = query.all()
        else:
            results = expense.query.all()

        # Convert the search results to a list of dictionaries
        results = [result.to_dict() for result in results]

        return jsonify(results)

    results = expense.query.all()
    results = [result.to_dict() for result in results]
    return render_template("expensetable.html", results=results)
@views.route('/expense/<int:id>/update', methods=['GET', 'POST', 'PUT'])
@login_required
def update_expense(id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    instance = expense.query.get(id)
    if not instance:
        flash('expense does not exist', category="Error")
        return redirect(url_for('views.Expense'))
    if request.method == "POST":
        instance.amount = request.form.get('amount')
        instance.type = request.form.get('type')
        instance.category = request.form.get('category')
        instance.comment = request.form.get('comment')
        db.session.commit()
        flash("Expense/Income updated successfully", category="Success")
        return redirect(url_for('views.Expense'))

    return render_template("update-expense.html", tmp=instance)

@views.route("/visual")
@login_required
def visual():
    if current_user.is_authenticated:
        return render_template('visual.html')
    return redirect(url_for('auth.login'))
@views.route("/management")
@login_required
def management():
    if current_user.is_authenticated:
        return render_template('management.html')
    return redirect(url_for('auth.login'))