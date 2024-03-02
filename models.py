from config import mysql

class BlogsModels:

    def createBlogTable():
        my_cursor = mysql.connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS blogs (
                blog_id INTEGER NOT NULL AUTO_INCREMENT,
                blog_title VARCHAR(1000) NOT NULL,
                blog_content TEXT NOT NULL,
                blog_created DATETIME NOT NULL,
                PRIMARY KEY (blog_id) 
        );"""
        my_cursor.execute(sql)
        mysql.connection.commit()
        my_cursor.close()

    def displayBlog():
        my_cursor = mysql.connection.cursor()
        sql = "SELECT * FROM blogs"
        my_cursor.execute(sql)
        blogs = my_cursor.fetchall()
        return blogs

    def searchBlog(search_input):
        my_cursor = mysql.connection.cursor()
        sql = "SELECT * FROM blogs WHERE (blogs.blog_title LIKE %s)"
        param = ('%' + search_input + '%',)
        my_cursor.execute(sql, param)
        blogs = my_cursor.fetchall()
        return blogs

    def createBlog(blog_title, blog_content, current_datetime):
        my_cursor = mysql.connection.cursor()
        sql = "INSERT INTO blogs (blog_title, blog_content, blog_created) VALUES (%s, %s, %s)"
        params = (blog_title, blog_content, current_datetime)
        my_cursor.execute(sql, params)
        mysql.connection.commit()
        my_cursor.close()

    def getBlog(blog_id):
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("SELECT * FROM blogs  WHERE blogs.blog_id=%s", (blog_id,))
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
