# -*- coding: utf-8 -*-
"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sqlite3



# download manager data_base path .
if os_type == 'Linux' or os_type == 'FreeBSD' or os_type == 'OpenBSD':
    persepolis_db_path = os.path.join(
        str(home_address), ".config/persepolis_download_manager/persepolis.db")
elif os_type == 'Darwin':
    persepolis_db_path = os.path.join(
        str(home_address), "Library/Application Support/persepolis_download_manager/persepolis.db")
elif os_type == 'Windows':
    persepolis_db_path = os.path.join(
        str(home_address), 'AppData', 'Local', 'persepolis_download_manager', 'persepolis.db')

# persepolis_db_connection
persepolis_db_connection = sqlite3.connect(persepolis_db_path)

# persepolis_db_cursor
persepolis_db_cursor = persepolis_db_connection.cursor()



# persepolis tmp folder path
if os_type != 'Windows':
    user_name_split = home_address.split('/')
    user_name = user_name_split[2]
    persepolis_tmp = '/tmp/persepolis_' + user_name
else:
    persepolis_tmp = os.path.join(
        str(home_address), 'AppData', 'Local', 'persepolis_tmp')

# plugins.db is store links, when browser plugins are send new links.
plugins_db_path = os.path.join(persepolis_tmp, 'plugins.db')

# plugins_db_connection
plugins_db_connection = sqlite3.connect(plugins_db_path)

# plugins_db_cursor
plugins_db_cursor = plugins_db_connection.cursor()

def createTables():
# queues_list contains name of categories and category settings
    persepolis_db_cursor.execute("""CREATE TABLE IF NOT EXISTS category_table(
                                                                category TEXT PRIMARY KEY,
                                                                start_time_enable TEXT,
                                                                start_hour TEXT,
                                                                start_minute TEXT,
                                                                end_time_enable TEXT,
                                                                end_hour TEXT,
                                                                end_minute TEXT,
                                                                reverse TEXT,
                                                                limit_enable TEXT,
                                                                limit_value TEXT,
                                                                after_downloads TEXT
                                                                        )""")


# download table contains download table download items information
    persepolis_db_cursor.execute("""CREATE TABLE IF NOT EXISTS download_table(
                                                                                file_name TEXT,
                                                                                status TEXT,
                                                                                size TEXT,
                                                                                downloaded_size TEXT,
                                                                                percent TEXT,
                                                                                connections TEXT,
                                                                                rate TEXT,
                                                                                estimate_time_left TEXT,
                                                                                gid TEXT PRIMARY KEY,
                                                                                firs_try_date TEXT,
                                                                                last_try_date TEXT,
                                                                                category TEXT,
                                                                                FOREIGN KEY(category) REFERENCES category_table(category)
                                                                                ON UPDATE CASCADE
                                                                                ON DELETE CASCADE
                                                                                )""")


# addlink_table contains addlink window download information
    persepolis_db_cursor.execute("""CREATE TABLE IF NOT EXISTS addlink_table(
                                                                            ID INTEGER PRIMARY KEY,
                                                                            gid TEXT,
                                                                            last_try_date TEXT,
                                                                            firs_try_date TEXT,
                                                                            out TEXT,
                                                                            final_download_path TEXT,
                                                                            start_hour TEXT,
                                                                            start_minute TEXT,
                                                                            end_hour TEXT,
                                                                            end_minute TEXT,
                                                                            link TEXT,
                                                                            ip TEXT,
                                                                            port TEXT,
                                                                            proxy_user TEXT,
                                                                            proxy_passwd TEXT,
                                                                            download_user TEXT,
                                                                            download_passwd TEXT,
                                                                            connections TEXT,
                                                                            limit TEXT,
                                                                            download_path TEXT,
                                                                            referer TEXT,
                                                                            load_cookies TEXT,
                                                                            user_agent TEXT,
                                                                            header TEXT,
                                                                            FOREIGN KEY(gid) REFERENCES download_table(gid) 
                                                                            ON UPDATE CASCADE 
                                                                            ON DELETE CASCADE 
                                                                            )""") 

# plugins_table contains links that sends by browser plugins. 
    plugins_db_cursor.execute("""CREATE TABLE IF NOT EXISTS plugins_table(
                                                                            ID INTEGER PRIMARY KEY,
                                                                            link TEXT,
                                                                            referer TEXT,
                                                                            load_cookies TEXT,
                                                                            user_agent TEXT,
                                                                            header TEXT,
                                                                            out TEXT,
                                                                            status TEXT
                                                                            )""") 
# insert new item in plugins_table
def insertInPluginsTable(link, referer, load_cookies, user_agent, header, out):
    plugins_db_cursor.execute("""INSERT INTO plugins_table VALUES(
                                                                NULL,
                                                                :link,
                                                                :referer,
                                                                :load_cookies,
                                                                :user_agent,
                                                                :header,
                                                                :out,
                                                                'new'
                                                                    )""", {
                                                                        'link': link,
                                                                        'referer': referer,
                                                                        'load_cookies': load_cookies,
                                                                        'user_agent': user_agent,
                                                                        'header': header,
                                                                        'out': out
                                                                        })

    plugins_db_connection.commit()

# insert new category in category_table
def insertInCategoryTable(category, start_time_enable,start_hour,start_minute,
                            end_time_enable, end_hour, end_minute, reverse,
                            limit_enable, limit_value, after_downloads):    
    persepolis_db_cursor.execute("""INSERT INTO category_table VALUES(
                                                            :category,
                                                            :start_time_enable,
                                                            :start_hour,
                                                            :start_minute,
                                                            :end_time_enable,
                                                            :end_hour,
                                                            :end_minute,
                                                            :reverse,
                                                            :limit_enable,
                                                            :limit_value,
                                                            :after_downloads
                                                            )""", {
                                                                'category': category,
                                                                'start_time_enable': start_time_enable,
                                                                'start_hour': start_hour,
                                                                'start_minute': start_minute,
                                                                'end_time_enable': end_time_enable,
                                                                'end_hour': end_hour,
                                                                'end_minute': end_minute,
                                                                'reverse': reverse,
                                                                'limit_enable': limit_enable,
                                                                'limit_value': limit_value,
                                                                'after_downloads': after_downloads
                                                                })
    persepolis_db_connection.commit()
 

# insert in to download_table in persepolis.db
def insertInDownloadTable(file_name, status, size, downloaded_size,
                        percent, connections, rate, estimate_time_left,
                        gid, firs_try_date, last_try_date):

    persepolis_db_cursor.execute("""INSERT INTO download_table VALUES(
                                                                :file_name,
                                                                :status,
                                                                :size,
                                                                :downloaded_size,
                                                                :percent,
                                                                :connections,
                                                                :rate,
                                                                :estimate_time_left,
                                                                :gid,
                                                                :firs_try_date,
                                                                :last_try_date,
                                                                :category
                                                                )""", {
                                                                    'file_name': file_name,
                                                                    'status': status,
                                                                    'size': size,
                                                                    'downloaded_size': downloaded_size,
                                                                    'percent': percent,
                                                                    'connections': connections,
                                                                    'rate': rate,
                                                                    'estimate_time_left': estimate_time_left,
                                                                    'gid': gid,
                                                                    'firs_try_date': firs_try_date,
                                                                    'last_try_date': last_try_date,
                                                                    'category': category
                                                                    })
    persepolis_db_connection.commit()
# insert in addlink table in persepolis.db 
def insertInAddLinkTable(gid, last_try_date, firs_try_date, out, final_download_path,
                        start_hour, start_minute, end_hour, end_minute, link,
                        ip, port, proxy_user, proxy_passwd, download_user,
                        download_passwd, connections, limit, download_path,
                        referer, load_cookies, user_agent, header):

    persepolis_db_cursor.execute("""INSERT INTO addlink_table VALUES(NULL,
                                                        :gid,
                                                        :last_try_date,
                                                        :firs_try_date,
                                                        :out,
                                                        :final_download_path,
                                                        :start_hour,
                                                        :start_minute,
                                                        :end_hour,
                                                        :end_minute,
                                                        :link,
                                                        :ip,
                                                        :port,
                                                        :proxy_user,
                                                        :proxy_passwd,
                                                        :download_user,
                                                        :download_passwd,
                                                        :connections,
                                                        :limit,
                                                        :download_path,
                                                        :referer,
                                                        :load_cookies,
                                                        :user_agent,
                                                        :header
                                                        )""", {
                                                            'gid' :gid,
                                                            'last_try_date': last_try_date,
                                                            'firs_try_date': firs_try_date,
                                                            'out': out,
                                                            'final_download_path': final_download_path,
                                                            'start_hour': start_hour,
                                                            'start_minute': start_minute,
                                                            'end_hour': end_hour,
                                                            'end_minute': end_minute,
                                                            'link': link,
                                                            'ip': ip,
                                                            'port': port,
                                                            'proxy_user': proxy_user,
                                                            'proxy_passwd': proxy_passwd,
                                                            'download_user': download_user,
                                                            'download_passwd': download_passwd,
                                                            'connections': connections,
                                                            'limit': limit,
                                                            'download_path' :download_path,
                                                            'referer': referer,
                                                            'load_cookies': load_cookies,
                                                            'user_agent': user_agent,
                                                            'header': header
                                                            })
    persepolis_db_connection.commit() 
    
 

# return download information in download_table with special gid.
def searchGidInDownloadTable(gid):
    persepolis_db_cursor.execute("""SELECT * FROM download_table WHERE gid = {}""".format(str(gid)))
    return persepolis_db_cursor.fetchall()

    
# return download information in addlink_table with special gid.
def searchGidInAddLinkTable(gid):
    persepolis_db_cursor.execute("""SELECT * FROM addlink_table WHERE gid = {}""".format(str(gid)))
    return persepolis_db_cursor.fetchall()

# return category information in category_table
def searchCategoryInCategoryTable(category):
    persepolis_db_cursor.execute("""SELECT * FROM category_table WHERE gid = {}""".format(str(category)))

# close connections
def closeConnections():
    persepolis_db_cursor.close()
    persepolis_db_connection.close()
