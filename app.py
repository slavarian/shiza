import psycopg2
from psycopg2 import Error

from database.core import Create_table 

from flask import (
    Flask,
    render_template,
    request ,
    redirect ,
    url_for ,
    session
)
from flask.app import Flask as FlaskApp


app: FlaskApp = Flask(__name__)
app.secret_key = "safdasdf312f3j9f"


db_params = {
    'host': 'localhost',
    'port': '5432',
    'database': 'mydata',
    'user': 'postgres',
    'password': 'admin'
}
def connect_to_db():
    connection = psycopg2.connect(**db_params)
    return connection


@app.route('/')
def main_page():   
    return render_template(
        template_name_or_list="index.html"
    )
   

@app.route('/lk', methods=['GET','POST'])
def lk_page():
     if 'id' in session:
        user_id = session['id']
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT login, author FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchall()
        cursor.execute("SELECT articles.id,articles.articles_author , articles.article_title, articles.articles_info, "
                   "comments.user_comment , comments.comment "
                   "FROM articles LEFT JOIN comments ON articles.id = comments.articles_id "
                   "ORDER BY articles.id DESC")

        rows = cursor.fetchall()
        cursor.execute("SELECT id, articles_author, article_title, articles_info, total_rating , vote_count "
               "FROM articles "
               "ORDER BY id DESC")
    
        articles = cursor.fetchall()
    
        if user:
            username = user[0] 
            return render_template('lk.html', username=username,rows=rows , articles=articles)
        

        return redirect(url_for('login'))


@app.route('/lk_non_author', methods=['GET','POST'])
def lk_non_author_page():
    if 'id' in session:
        user_id = session['id']
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT login, author FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchall()
        cursor.execute("SELECT articles.id,articles.articles_author , articles.article_title, articles.articles_info, "
                   "comments.user_comment , comments.comment "
                   "FROM articles LEFT JOIN comments ON articles.id = comments.articles_id "
                   "ORDER BY articles.id DESC")

        rows = cursor.fetchall()
        cursor.execute("SELECT id, articles_author, article_title, articles_info, total_rating , vote_count "
               "FROM articles "

               "ORDER BY id DESC")
    
        articles = cursor.fetchall()
    
      
        if user:
            username = user[0] 
            return render_template('lk_non_author.html', username=username,rows=rows , articles=articles)

    return redirect(url_for('login'))

@app.route('/lk_all_post', methods=['GET','POST'])
def lk_all_post():
    if 'id' in session:
        user_id = session['id']
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT login, author FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchall()
        cursor.execute("SELECT articles.id,articles.articles_author , articles.article_title, articles.articles_info, "
                   "comments.user_comment , comments.comment "
                   "FROM articles LEFT JOIN comments ON articles.id = comments.articles_id "
                   "ORDER BY articles.id DESC")

        rows = cursor.fetchall()
        cursor.execute("SELECT id, articles_author, article_title, articles_info, total_rating , vote_count "
               "FROM articles "
               "WHERE total_rating >= 5 "
               "ORDER BY id DESC")
    
        articles = cursor.fetchall()
    
        if user:
            username = user[0] 
            return render_template('lk_all_post.html', username=username,rows=rows , articles=articles)

    return redirect(url_for('login'))

@app.route('/create_post', methods=['GET','POST'])
def create_post():
    if request.method == 'POST':
        user = session['id']
        article_title = request.form['title']
        articles_info = request.form['tittle_info']

        connection = connect_to_db()
        cursor = connection.cursor()

        cursor.execute("SELECT login FROM users WHERE id = %s", (user,))
        user_login = cursor.fetchone()
        cursor.execute("INSERT INTO articles (articles_author, article_title, articles_info) VALUES (%s, %s, %s)",
                        (user_login, article_title, articles_info))
            
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('lk_page'))
        
     
    return render_template('create_post.html')


@app.route('/reg', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        author = request.form['author']

        connection = connect_to_db()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT id FROM users WHERE login = %s", (login,))
            existing_user = cursor.fetchone()

            if existing_user:
                error = 'Пользователь с таким именем уже существует'
                return render_template('reg.html', error=error)

            cursor.execute("INSERT INTO users (login, email, password ,password2 , first_name, last_name , author) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                           (login, email, password, password2, first_name, last_name, author))
            connection.commit()

            return redirect(url_for('login'))

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
            error = 'Ошибка при регистрации пользователя'
            return render_template('reg.html', error=error)
        finally:
            if connection:
                cursor.close()
                connection.close()

    return render_template('reg.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        connection = connect_to_db()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT id, author FROM users WHERE login = %s AND password = %s", (login, password))
            user = cursor.fetchone()

            if user:
                session['id'] = user[0]
                author = user[1]
                if author == "да":
                    return redirect(url_for('lk_page'))
                elif author == "нет":
                    return redirect(url_for('lk_non_author_page'))
            else:
                error = 'Неверное имя пользователя или пароль'
                return render_template('login.html', error=error)

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
            error = 'Ошибка при входе'
            return render_template('login.html', error=error)
        finally:
            if connection:
                cursor.close()
                connection.close()

    return render_template('login.html')


@app.route('/rate/<int:post_id>', methods=['POST'])
def rate_post(post_id):
    if 'id' in session:
        user_id = session['id']
        rating = request.form['rating']  
        connection = connect_to_db()
        cursor = connection.cursor()

  
        cursor.execute("SELECT total_rating, vote_count FROM articles WHERE id = %s", (post_id,))
        result = cursor.fetchone()
        total_rating = result[0]
        vote_count = result[1]

        if rating == 'like':
            total_rating += 1 
        elif rating == 'dislike':
            total_rating -= 1  

        vote_count += 1 

        cursor.execute("UPDATE articles SET total_rating = %s, vote_count = %s WHERE id = %s",
                           (total_rating, vote_count, post_id))
        connection.commit()
      

        cursor.close()
        connection.close()

        return redirect('/lk_non_author')
    else:
        return redirect(url_for('login'))


@app.route('/comment/<int:post_id>', methods=['GET', 'POST'])
def comment(post_id):
    if request.method == 'POST':
        connection = connect_to_db()
        cursor = connection.cursor()
        comment_text = request.form['comment']
        user = session['id']
   
        cursor.execute("SELECT login FROM users WHERE id = %s", (user,))
        user_login = cursor.fetchone()

        cursor.execute("INSERT INTO comments (user_comment, articles_id, comment) VALUES (%s, %s, %s)", 
                           (user_login, post_id, comment_text))
        connection.commit()
       
     
        return redirect('/lk_non_author')

    return render_template('comment.html', post_id=post_id)


if __name__ == '__main__':
    app.run(
        host='localhost',
        port=8050,
        debug=True)
    Create_table()
   