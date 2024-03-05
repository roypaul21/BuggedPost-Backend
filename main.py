from flask import request, jsonify, session
from config import app
from models import BlogsModels, UsersModel, UsersBlogsModel
from contr import BlogController, UserController
import datetime

#--------------------------USER--------------------------
@app.route("/api/get_credentials", methods=["GET"])
def getCredentials():
    user_id = session.get("user_id")
    print(user_id)
    return (jsonify({"cred": user_id}))

@app.route("/api/create_user", methods=["POST"])
def createUsers():
    username = request.json.get("username") 
    user_password = request.json.get("userPassword") 
    user_confirm_password = request.json.get("userConfirmPassword") 
    current_datetime = datetime.datetime.now()

    if not username or not user_password or not user_confirm_password:
        return (jsonify({"message": "Fill Up All Input Fields!"}), 400,)
    
    if user_password != user_confirm_password:
        return (jsonify({"message": "Passwords Doesn't Match!"}), 400,)

    if UsersModel.getUsername(username):
        return (jsonify({"message": "Username Already Exist!"}), 400,)
    
    try:
        UserController.createUserContr(username, user_password, current_datetime)

    except Exception as e:
        return (jsonify({"message": str(e)}), 400)

    return jsonify({"message": "User Created Successfully!"}), 201


@app.route("/api/login", methods=["POST"])
def loginUser():
    username = request.json.get("username") 
    user_password = request.json.get("userPassword")  
    
    if not UsersModel.getUsername(username):
        return (jsonify({"message": "Username Doesn't Exist!"}), 401 ,)
    
    try:
        user_id = UserController.loginUserContr(username, user_password)
        if not user_id:
            return (jsonify({"message": " Wrong User Password!"}), 401 ,)
        
        session["user_id"] = user_id
        

    except Exception as e:
        return (jsonify({"message": str(e)}), 401)

    return jsonify({"message": "User Login Successfully"}), 201

@app.route("/api/logout", methods=["POST"])
def logoutUser():
    session.pop("user_id")
    return jsonify({"message": "User Logout Succesfully"}), 201

@app.route("/api/user_blogs", methods=["GET"])
def getUserBlogs():
    user_id = session.get("user_id")
    if not user_id:
        return (jsonify({"message": "Unauthorized!"}), 401 ,)
    
    try:
        user_blog = UsersBlogsModel.displayUserBlogs(user_id)
        user_blog_list = BlogController.json_blogs(user_blog)

        return jsonify({"blogs": user_blog_list}) 

    except Exception as e:
        return (jsonify({"message": str(e)}), 401)  

    
@app.route("/api/user_blogs/<string:search_input>", methods=["GET"])
def getSearchUserBlogs(search_input):
    user_id = session.get("user_id")
    if not user_id:
        return (jsonify({"message": "Unauthorized!"}), 401 ,)
    try:
        user_blog = UsersBlogsModel.searchUserBlogs(user_id, search_input)
        user_blog_list = BlogController.json_blogs(user_blog)

        return jsonify({"blogs": user_blog_list}) 

    except Exception as e:
        return (jsonify({"message": str(e)}), 401)  

    


#---------------------------------BLOG POST----------------------------------
#this is for future display all blogs so other users can see it
"""@app.route("/api/blogs", methods=["GET"])
def displayBlogs():
    BlogsModels.createBlogTable()
    blog_list = BlogController.json_blogs(BlogsModels.displayBlog())
    return jsonify({"blogs": blog_list})

@app.route("/api/blogs/<string:search_input>", methods=["GET"])
def SearchBlogs(search_input):
    blog_list = BlogController.json_blogs(BlogsModels.searchBlog(search_input))
    return jsonify({"blogs": blog_list})"""

@app.route("/api/create_blogs", methods=["POST"])
def createBlogs():
    blog_title = request.json.get("blog_title")
    blog_content = request.json.get("blog_content")
    current_datetime = datetime.datetime.now()
    user_id = session.get("user_id")

    if not blog_title or not blog_content:
        return (jsonify({"message": "Fill Up All Input Fields!"}), 
        400,
        )
    try: 
        UserController.createUserBlogContr(blog_title, blog_content, current_datetime, user_id)
    except Exception  as e:
        return (jsonify({"message": str(e)}), 400)
    
    return jsonify({"message": "Blog Created Successfully!"}), 201

@app.route("/api/update_blogs/<int:blog_id>", methods=["PATCH"])
def updateBlog(blog_id):
    blogs = BlogsModels.getBlog(blog_id) 
    data = request.json
    blog_title = data.get("blog_title", blogs["blog_title"])
    blog_content = data.get("blog_content", blogs["blog_content"])
    if BlogController.isBlogExist(blog_id):
        return (jsonify({"message": "Blog Doesn't Exist!"}), 
        404,
        ) 
    
    if BlogController.BlogInputEmpty(blog_title, blog_content):
        return (jsonify({"message": "Fill Up Input All Fields!"}), 
        400,
        ) 
    
    try: 
        BlogsModels.updateBlog(blog_id, blog_title, blog_content)

    except Exception  as e:
        return (jsonify({"message": str(e)}), 400)
    
    return jsonify({"message": "Blog Updated Successfully!"}), 200

@app.route("/api/delete_blogs/<int:blog_id>", methods=["DELETE"])
def deleteBlog(blog_id):    
    try: 
        BlogsModels.deleteBlog(blog_id)

    except Exception  as e:
        return (jsonify({"message": str(e)}), 400)
    
    return jsonify({"message": "Blog Removed Successfully!"}), 200


if __name__ == "__main__":
    app.run(debug=False)