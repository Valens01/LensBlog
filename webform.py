from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired, EqualTo,Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField



class SearchForm(FlaskForm):
    searched=StringField("search",validators=[DataRequired()])
    
    submit=SubmitField("Submit") 


class LoginForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField("Submit") 

#create a post form
class PostForm(FlaskForm):
    title= StringField("Title",validators=[DataRequired()] )
    content=CKEditorField("Content",validators=[DataRequired()])
    slug=StringField("Slug",validators=[DataRequired()] )
    submit=SubmitField("Post") 

#create a form class
class UsersForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    username=StringField("username",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired()])
    favorite_color= StringField("Favorite Color",validators=[DataRequired()])
    password_hash= PasswordField("password",validators=[DataRequired(),EqualTo('password_hash2',message='password must match')])
    password_hash2=PasswordField("confirm password",validators=[DataRequired()])
    submit=SubmitField("submit") 

#create a passwordform class
class PasswordForm(FlaskForm):
    email= StringField("what's your Email",validators=[DataRequired()])
    password=PasswordField("what's your Password",validators=[DataRequired()])
    submit=SubmitField("submit") 

#create a form class
class NamerForm(FlaskForm):
    name = StringField(" what's your name",validators=[DataRequired()])
    submit=SubmitField("submit") 
