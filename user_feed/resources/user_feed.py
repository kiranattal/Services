from os import name
from flask import Flask, Blueprint
from flask_restful import reqparse,Api,Resource

feed_bp=Blueprint("api",__name__)
feed_api=Api(feed_bp)



class Feed(Resource):
    def get(self, user):
        user_posts=[]
        user_friends=[]
        user_s_friends_posts=[]


feed_api.add_resource(Feed,"/feed/<string:user>")