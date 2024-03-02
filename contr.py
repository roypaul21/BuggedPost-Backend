from models import BlogsModels

class BlogController:
    
    def json_blogs(blogs):
        blogs_list = []

        for blog in blogs:
            blog_dict = {
                "blog_id": blog[0],
                "blog_title": blog[1],
                "blog_content": blog[2],
                "blog_date": blog[3]
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