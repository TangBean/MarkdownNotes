#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-12-31 16:37:23
# Project: zhihu_hot

from pyspider.libs.base_handler import *
import json
import MySQLdb
import random


class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent': 'GoogleBot',
            'Host': 'www.zhihu.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
    }

    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost',
                                    port=3306,
                                    user='root',
                                    passwd='123',
                                    db='wenda',
                                    charset='utf8')
        self.include_param = 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics'
        self.form_data = {
            'include': self.include_param,
            'offset': '0',
            'limit': '10',
            'sort_by': 'default',
            'platform': 'desktop'
        }
        self.cookies = {
            '_xsrf': 'f21a3e88-e8d0-4572-ade6-b3b8e32da431',
            '_zap': 'e2169407-707a-418a-bbaa-132b2a57ba96',
            'capsion_ticket': '"2|1:0|10:1544500242|14:capsion_ticket|44:N2Y4ZWZlODhkZWVmNDgyYThhNzEwYmM2MGQxOTUyNDQ=|d31973038ec0c6be7c1617ea89cf490e077cd2946ef7f4285267a6890b4a57bc"',
            'd_c0': '"AIChfPnHpg6PToEgSz_0-Ock5cQ7wSGWni4=|1544490662"',
            'q_c1': 'd0ce0a17b9c247a0a97c82cbc94bc3f9|1544493153000|1544493153000',
            'tgw_l7_route': '156dfd931a77f9586c0da07030f2df36',
            'tst': 'h',
            'z_c0': '"2|1:0|10:1544500244|4:z_c0|92:Mi4xVmd6M0FBQUFBQUFBZ0tGOC1jZW1EaVlBQUFCZ0FsVk5GSUw4WEFBbG9PSGY3MGZtMkNlejlDVXNOMFlkMGNGaXBB|da45ee9835195eb4f7003e12fec5b7a405bd572f90052372235e1b636b0db5dd"'
        }

    def add_question(self, title, content, comment_count):
        try:
            cursor = self.conn.cursor();
            sql = "insert into question (title, content, user_id, created_date, comment_count) " \
                  "values('%s', '%s', %d, %s, %d);" % (title, content, random.randint(1, 10), 'now()', comment_count)
            cursor.execute(sql)
            qid = cursor.lastrowid
            self.conn.commit()
            return qid
        except Exception as e:
            print(e)
            self.conn.rollback()

    def add_user(self, name, head_url):
        try:
            cursor = self.conn.cursor();
            sql = "insert into user (name, password, salt, head_url) " \
                  "values('%s', '%s', '%s', '%s');" % (name, '', '', head_url)
            cursor.execute(sql)
            uid = cursor.lastrowid
            self.conn.commit()
            return uid
        except Exception as e:
            print(e)
            self.conn.rollback()

    def add_comment(self, uid, content, qid):
        try:
            cursor = self.conn.cursor()
            sql = "insert into comment (user_id, content, entity_id, entity_type, created_date, status) " \
                  "values(%d, '%s', %d, %d, %s, %d);" % (uid, content, qid, 1, 'now()', 0)
            cursor.execute(sql)
            cid = cursor.lastrowid
            self.conn.commit()
            return cid
        except Exception as e:
            print(e)
            self.conn.rollback()

    def user_exist(self, username):
        try:
            cursor = self.conn.cursor()
            sql = "select id from user where name='%s';" % (username)
            cursor.execute(sql)
            res = cursor.fetchone()
            self.conn.commit()
            if res is None:
                return -1
            else:
                return res[0]
        except Exception as e:
            print(e)
            self.conn.rollback()

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.zhihu.com/hot', callback=self.question_page, cookies=self.cookies, validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def question_page(self, response):
        for each in response.doc('div.HotItem-content>a').items():
            url = each.attr.href
            index = url.find('question/')
            qid = url[(index + 9): len(url)]
            q_title = each('h2').text().replace('"', '//"').replace("'", "//'")
            q_content = each('p').text().replace('"', '//"').replace("'", "//'")
            save_param = {'q_title': q_title, 'q_content': q_content}
            answer_url = "https://www.zhihu.com/api/v4/questions/" + str(qid) + "/answers"
            self.crawl(answer_url, callback=self.detail_page, params=self.form_data, validate_cert=False,
                       save=save_param)

    @config(priority=2)
    def detail_page(self, response):
        data_obj = json.loads(response.content.decode('utf8'))

        if len(data_obj['data']) <= 0:
            return {
                "url": response.url,
                "title": response.doc('title').text(),
            }
        elif len(data_obj['data']) > 10:
            data_obj['data'] = data_obj['data'][0:10]

        # print(response.save['q_title'])
        # print(response.save['q_content'])
        # print(len(data_obj['data']))
        qid = self.add_question(response.save['q_title'], response.save['q_content'], len(data_obj['data']))

        for cmt in data_obj['data']:
            username = cmt['author']['name']
            headUrl = cmt['author']['avatar_url']
            uid = self.user_exist(username)
            if uid == -1:
                uid = self.add_user(username, headUrl)

            content = cmt['content'].replace('"', '//"').replace("'", "//'")
            self.add_comment(uid, content, qid)

        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
