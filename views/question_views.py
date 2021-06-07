from flask import Blueprint, render_template, request, url_for
from pybo.models import Question
from pybo.forms import QuestionForm
from datetime import datetime
from pybo import db
from werkzeug.utils import redirect
from pybo.forms import QuestionForm, AnswerForm


bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo'


@bp.route('/')
def q_list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)


@bp.route('/create/', methods=['GET', 'POST'])
def create():
    form = QuestionForm()
    print(f'method : {request.method}, {form.subject.data}, {form.validate_on_submit()}')
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        print(f'method : {question.id}')
        return redirect(url_for('main.index'))

    return render_template('question/question_form.html', form=form)
