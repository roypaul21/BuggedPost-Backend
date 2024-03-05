from models import BlogsModels, UsersModel, UsersBlogsModel
import hashlib

class BlogController:
    
    def json_blogs(blogs):
        blogs_list = []
        for blog in blogs:
            blog_dict = {
                "blog_id": blog["blog_id"],
                "blog_title": blog["blog_title"],
                "blog_content": blog["blog_content"],
                "blog_date": blog["blog_created"]
            }
            blogs_list.append(blog_dict)
        
        return blogs_list
    
    def json_user_blogs(user_blogs):
        blogs_list = []
        for blog in user_blogs:
            blog_dict = {
                "username": blog["username"],
                "blog_id": blog["blog_id"],
                "blog_title": blog["blog_title"],
                "blog_content": blog["blog_content"],
                "blog_date": blog["blog_created"]
            }
            blogs_list.append(blog_dict)
        
        return blogs_list

    def isBlogExist(blog_id):
       
        if not BlogsModels.getBlog(blog_id):
            return True
        else:
            return False
           
    def BlogInputEmpty(blog_title, blog_content):
        if not blog_title or not blog_content:
            return True
        
        else:
            return False

class UserController:

    def createUserContr(username, user_password, current_datetime):
        hash = hashlib.new("SHA256")
        hash.update(user_password.encode())
        hashed_password = hash.hexdigest()

        BlogsModels.createBlogTable()
        UsersModel.createUsersTable()
        UsersModel.createUserBlogsTable()
        UsersModel.createUser(username, hashed_password, current_datetime)

    def createUserBlogContr(blog_title, blog_content, current_datetime, user_id):
        BlogsModels.createBlogTable()
        BlogsModels.createBlog(blog_title, blog_content, current_datetime, user_id)
        fetch_blog_id = BlogsModels.getBlogID(user_id)
        UsersBlogsModel.createUsersBlogs(user_id, fetch_blog_id["blog_id"])


    def loginUserContr(username, user_password):
        hash = hashlib.new("SHA256")
        hash.update(user_password.encode())
        hashed_password = hash.hexdigest()

        stored_user = UsersModel.getUser(username, hashed_password) 
        if not stored_user:
            return False
        return stored_user['user_id']
    


        
    


        