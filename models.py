from config import mysql

class BlogsModels:

    def createBlogTable():
        my_cursor = mysql.connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS blog_bug.blogs (
                blog_id INT NOT NULL AUTO_INCREMENT,
                blog_title VARCHAR(1000) NOT NULL,
                blog_content TEXT NOT NULL,
                blog_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (blog_id) 
        )"""
        my_cursor.execute(sql)
        mysql.connection.commit()
        my_cursor.close()

    def displayBlog():
        my_cursor = mysql.connection.cursor()
        sql = "SELECT * FROM blog_bug.blogs"
        my_cursor.execute(sql)
        blogs = my_cursor.fetchall()
        return blogs

    def searchBlog(search_input):
        my_cursor = mysql.connection.cursor()
        sql = "SELECT * FROM blog_bug.blogs WHERE (blogs.blog_title LIKE %s)"
        param = ('%' + search_input + '%',)
        my_cursor.execute(sql, param)
        blogs = my_cursor.fetchall()
        return blogs

    def createBlog(blog_title, blog_content):
        my_cursor = mysql.connection.cursor()
        sql = "INSERT INTO blog_bug.blogs (blog_title, blog_content) VALUES (%s, %s)"
        params = (blog_title, blog_content)
        my_cursor.execute(sql, params)
        mysql.connection.commit()
        my_cursor.close()

    def getBlog(blog_id):
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("SELECT * FROM blog_bug.blogs  WHERE blogs.blog_id=%s", (blog_id,))
        blog = my_cursor.fetchone()
        return blog

    def updateBlog(blog_id, blog_title, blog_content):
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("UPDATE blog_bug.blogs SET blogs.blog_title = %s, blogs.blog_content = %s WHERE blogs.blog_id = %s", (blog_title, blog_content, blog_id,))
        mysql.connection.commit()
        my_cursor.close()

    def deleteBlog(blog_id):
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("DELETE FROM blog_bug.blogs WHERE blogs.blog_id=%s", (blog_id,))
        mysql.connection.commit()
        my_cursor.close()
