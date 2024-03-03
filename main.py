from flask import request, jsonify
from config import app
from models import BlogsModels
from contr import BlogController
import datetime

@app.route("/api/blogs", methods=["GET"])
def displayBlogs():
    BlogsModels.createBlogTable()
    blog_list = BlogController.json_blogs(BlogsModels.displayBlog())
    return jsonify({"blogs": blog_list})

@app.route("/api/blogs/<string:search_input>", methods=["GET"])
def SearchBlogs(search_input):
    blog_list = BlogController.json_blogs(BlogsModels.searchBlog(search_input))
    return jsonify({"blogs": blog_list})

@app.route("/api/create_blogs", methods=["POST"])
def createBlogs():
    blog_title = request.json.get("blog_title")
    blog_content = request.json.get("blog_content")
    current_datetime = datetime.datetime.now()

    if not blog_title or not blog_content:
        return (jsonify({"message": "Fill Up All Input Fields!"}), 
        400,
        )
    try: 
        BlogsModels.createBlogTable()
        BlogsModels.createBlog(blog_title, blog_content, current_datetime)
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