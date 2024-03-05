from config import mysql

class BlogsModels:

    def createBlogTable():
        my_cursor = mysql.connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS blogs (
                blog_id INTEGER NOT NULL AUTO_INCREMENT,
                blog_title VARCHAR(1000) NOT NULL,
                blog_content TEXT NOT NULL,
                blog_created DATETIME NOT NULL,
                user_session_id INT NOT NULL, 
                PRIMARY KEY (blog_id) 
        );"""
        my_cursor.execute(sql)
        mysql.connection.commit()
        my_cursor.close()

    def displayBlog():
        my_cursor = mysql.connection.cursor()
        sql = """SELECT users.username, blogs.* FROM blogs 
                INNER JOIN users_blogs ON blogs.blog_id = users_blogs.blog_id 
                INNER JOIN users ON users.user_id = users_blogs.user_id """
        my_cursor.execute(sql)
        blogs = my_cursor.fetchall()
        return blogs

    def searchBlog(search_input):
        my_cursor = mysql.connection.cursor()
        sql = """SELECT users.username, blogs.* FROM blogs 
                INNER JOIN users_blogs ON blogs.blog_id = users_blogs.blog_id 
                INNER JOIN users ON users.user_id = users_blogs.user_id 
                WHERE (blogs.blog_title LIKE %s) """
        param = ('%' + search_input + '%',)
        my_cursor.execute(sql, param)
        blogs = my_cursor.fetchall()
        return blogs

    def createBlog(blog_title, blog_content, current_datetime, user_session_id):
        my_cursor = mysql.connection.cursor()
        sql = "INSERT INTO blogs (blog_title, blog_content, blog_created, user_session_id) VALUES (%s, %s, %s, %s)"
        params = (blog_title, blog_content, current_datetime, user_session_id)
        my_cursor.execute(sql, params)
        mysql.connection.commit()
        my_cursor.close()

    def getBlog(blog_id):
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("SELECT * FROM blogs  WHERE blogs.blog_id=%s", (blog_id,))
        blog = my_cursor.fetchone()
        return blog
    
    def getBlogID(user_session_id):
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("SELECT blogs.blog_id FROM blogs WHERE blogs.user_session_id=%s ORDER BY blog_id DESC LIMIT 1", (user_session_id,))
        blog = my_cursor.fetchone()
        return blog

    def updateBlog(blog_id, blog_title, blog_content):
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("UPDATE blogs SET blogs.blog_title = %s, blogs.blog_content = %s WHERE blogs.blog_id = %s", (blog_title, blog_content, blog_id,))
        mysql.connection.commit()
        my_cursor.close()

    def deleteBlog(blog_id):
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("DELETE FROM blogs WHERE blogs.blog_id=%s", (blog_id,))
        mysql.connection.commit()
        my_cursor.close()


class UsersModel: 
    
    def createUserBlogsTable():
        my_cursor = mysql.connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS users_blogs (
                user_blog_id INTEGER NOT NULL AUTO_INCREMENT,
                user_id INTEGER NOT NULL,
                blog_id INTEGER NOT NULL,
                PRIMARY KEY (user_blog_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                FOREIGN KEY (blog_id) REFERENCES blogs (blog_id) ON DELETE CASCADE
            );"""
        my_cursor.execute(sql)
        mysql.connection.commit()
        my_cursor.close()
    
    def createUsersTable():
        my_cursor = mysql.connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER NOT NULL AUTO_INCREMENT,
                username VARCHAR(1000) NOT NULL,
                user_password VARCHAR(1000) NOT NULL,
                user_created DATETIME NOT NULL,
                PRIMARY KEY (user_id) 
        );"""
        my_cursor.execute(sql)
        mysql.connection.commit()
        my_cursor.close()
    
    def getUsername(user_name):
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("SELECT * FROM users WHERE users.username=%s", (user_name,))
        blog = my_cursor.fetchone()
        return blog
    
    def createUser(username, password, current_datetime):
        my_cursor = mysql.connection.cursor()
        sql = "INSERT INTO users (username, user_password, user_created) VALUES (%s, %s, %s)"
        params = (username, password, current_datetime)
        my_cursor.execute(sql, params)
        mysql.connection.commit()
        my_cursor.close()

    def getUser(username, password):
        my_cursor = mysql.connection.cursor()
        sql = "SELECT * FROM users WHERE users.username=%s AND users.user_password=%s"
        param = (username, password,)
        my_cursor.execute(sql, param)
        user = my_cursor.fetchone()
        return user
     
    
class UsersBlogsModel: 
    
    def displayUserBlogs(user_id):
        my_cursor = mysql.connection.cursor()
        sql = """SELECT blogs.blog_id, blogs.blog_title, blogs.blog_content, blogs.blog_created FROM users 
                 INNER JOIN users_blogs ON users.user_id = users_blogs.user_id
                 INNER JOIN blogs ON blogs.blog_id = users_blogs.blog_id WHERE users.user_id = %s"""
        param = (user_id,)
        my_cursor.execute(sql, param)
        user_blogs = my_cursor.fetchall()
        return user_blogs
    
    def searchUserBlogs(user_id, search_input):
        my_cursor = mysql.connection.cursor()
        sql = """SELECT blogs.blog_id, blogs.blog_title, blogs.blog_content, blogs.blog_created FROM users 
                 INNER JOIN users_blogs ON users.user_id = users_blogs.user_id
                 INNER JOIN blogs ON blogs.blog_id = users_blogs.blog_id WHERE users.user_id=%s AND blogs.blog_title LIKE %s"""
        param = (user_id, '%' + search_input + '%',)
        my_cursor.execute(sql, param)
        user_blogs = my_cursor.fetchall()
        return user_blogs
    
    def createUsersBlogs(user_id, blog_id):
        my_cursor = mysql.connection.cursor()
        sql = "INSERT INTO users_blogs (user_id, blog_id) VALUES (%s, %s)"
        params = (user_id, blog_id)
        my_cursor.execute(sql, params)
        mysql.connection.commit()
        my_cursor.close()
