# post_service.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

posts = {
        '1': {'user_id': '1', 'post': 'Hello, world!'},
        '2': {'user_id': '2', 'post': 'My first blog post'}
    }
#get all posts with user information
@app.route('/post', methods=['GET'])
def get_posts():
    allposts = posts
    for i in allposts:
        response = requests.get(f'http://host.docker.internal:5000/user/{allposts[i]["user_id"]}')
        # response = requests.get(f'http://localhost:5000/user/{allposts[i]["user_id"]}')
        
        if response.status_code ==200:
            allposts[i]['user'] = response.json()
    return jsonify(allposts)




#get specific post with user
@app.route('/post/<id>', methods=['GET'])
def get_post(id):
    if id in posts:
        post_info = posts.get(id, {}) 
    # Get user info from User Service
        if post_info:
            # response = requests.get(f'http://localhost:5000/user/{post_info["user_id"]}')
            response = requests.get(f'http://host.docker.internal:5000/user/{post_info["user_id"]}')
            
            if response.status_code == 200:
                post_info['user'] = response.json()
        return jsonify(post_info)
    else:
        return {'error':'Post does not exist'}





#create a post
@app.route('/post', methods=['POST'])
def create_post():
    newId = (len(posts)+1)
    new_post = {
        str(newId ):  { 'user_id':request.json['user_id'], 'post':request.json["post"]}
            }
    posts.update(new_post)
    return new_post





#Update post while keeping user the same
@app.route('/post/<id>', methods=['PUT'])
def update_post(id):    
    if id in posts:
        update_post = {'user_id':posts[id]['user_id'],'post':request.json["post"]}
        posts.update({id:update_post})
        return update_post
    else:
        return {'error':'User Not Found'}
    




#delete post
@app.route('/post/<id>',methods=['DELETE'])
def delete_post(id):
    if id in posts:
        del posts[id]
        return posts
    else:
       return {'error': 'User Does Not Exist'}



if __name__ == '__main__':
    app.debug=True
    app.run(port=5001)