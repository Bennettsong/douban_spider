#!/usr/bin/env python3
# coding=utf-8
# author=XingLong Pan
# date=2016-12-06

import pymysql.cursors
import configparser


class DbHelper:
    __connection = None

    def __init__(self):
        self.__connect_database()

    def __connect_database(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.__connection = pymysql.connect(
            host=config['mysql']['host'],
            user=config['mysql']['user'],
            port=int(config['mysql']['port']),
            password=config['mysql']['password'],
            db=config['mysql']['db_name'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    def insert_movie(self, movie):
        try:
            with self.__connection.cursor() as cursor:
                sql = "INSERT IGNORE INTO `movie` (`douban_id`, `title`, `directors`, " \
                      "`scriptwriters`, `actors`, `types`,`release_region`," \
                      "`release_date`,`alias`,`languages`,`duration`,`score`," \
                      "`description`,`tags`,`recommendMovie`,`vote_num`,`rating_per_stars5`,`rating_per_stars4`,`rating_per_stars3`,`rating_per_stars2`,`rating_per_stars1`,`comment_num`) VALUES (%s," \
                      "%s, %s, %s, %s, %s, %s, %s," \
                      "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(sql, (
                    movie['douban_id'],
                    movie['title'],
                    movie['directors'],
                    movie['scriptwriters'],
                    movie['actors'],
                    movie['types'],
                    movie['release_region'],
                    movie['release_date'],
                    movie['alias'],
                    movie['languages'],
                    movie['duration'],
                    movie['score'],
                    movie['description'],
                    movie['tags'],
                    movie['recommendMovie'],
                    movie['vote_num'],
                    movie['rating_per_stars5'],
                    movie['rating_per_stars4'],
                    movie['rating_per_stars3'],
                    movie['rating_per_stars2'],
                    movie['rating_per_stars1'],
                    movie['comment_num']
                ))
                self.__connection.commit()
        finally:
            pass

    def insert_movieComments(self, movieComments):
        try:
            with self.__connection.cursor() as cursor:
                data = [list(result.values()) for result in movieComments]
                sql = "INSERT IGNORE INTO `movie_comment` (`douban_id`, `comment_url`, `star`, " \
                      "`content`, `comment_id`, `people_id`, `people`,`useful_num`," \
                      "`time`,`people_url`) VALUES (%s," \
                      "%s, %s, %s, %s, %s, %s, %s, %s," \
                      "%s);"
                cursor.executemany(sql, data)
                self.__connection.commit()
                # print('插入成功！')
        except:
            # 如果发生错误则回滚
            self.__connection.rollback()
            print('插入失败！')
        finally:
            pass

    def insert_personalInfo(self, personalInfo):
        try:
            with self.__connection.cursor() as cursor:
                sql = "INSERT IGNORE INTO `personal_info` (`pid`, `name`, `location`, `introduction`, " \
                      "`follow_num`, `personUrl`, `register_time`, `follow_url`,`do`,`wish`,`collect`,`do_num`,`wish_num`,`collect_num`) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(sql, (
                    personalInfo['pid'],
                    personalInfo['name'],
                    personalInfo['location'],
                    personalInfo['introduction'],
                    personalInfo['follow_num'],
                    personalInfo['personUrl'],
                    personalInfo['register_time'],
                    personalInfo['follow_url'],
                    personalInfo['do'],
                    personalInfo['wish'],
                    personalInfo['collect'],
                    personalInfo['do_num'],
                    personalInfo['wish_num'],
                    personalInfo['collect_num']
                ))
                self.__connection.commit()
                # print('插入成功！')
        except Exception as e:
            # 如果发生错误则回滚
            self.__connection.rollback()
            print(e)
            print('插入失败！')
        finally:
            pass
    def insert_followPersonUrl(self, followPersonUrls):
        try:
            with self.__connection.cursor() as cursor:
                data = [list(result.values()) for result in followPersonUrls]
                sql = "INSERT IGNORE INTO `follow_person_url` (`original_id`, `follow_id`, `follow_url`) VALUES (%s, %s, %s);"
                cursor.executemany(sql, data)
                self.__connection.commit()
        except:
            # 如果发生错误则回滚
            self.__connection.rollback()
            print('插入失败！')
        finally:
            pass
    def insert_wishMovies(self, wishMovies):
        try:
            with self.__connection.cursor() as cursor:
                data = [list(result.values()) for result in wishMovies]
                sql = "INSERT IGNORE INTO `wish_movie` (`douban_id`, `people_id`, `time`) VALUES (%s, %s, %s);"
                cursor.executemany(sql, data)
                self.__connection.commit()
                # print('插入成功！')
        except:
            # 如果发生错误则回滚
            self.__connection.rollback()
            print('插入失败！')
        finally:
            pass
    # 根据flag判断是否已经读取
    def queryPersonUrl(self):
        try:
            with self.__connection.cursor() as cursor:
                sql = "SELECT people_url FROM (SELECT DISTINCT `people_id`,`people_url` FROM movie_comment) AS a;"
                cursor.execute(sql)
                results = cursor.fetchall()
                cursor.close()
                data = [result['people_url'] for result in results]
                return data
        except:
            print('读取失败！')
            return None

    def close_db(self):
        self.__connection.close()
