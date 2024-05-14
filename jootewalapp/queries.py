from django.db import connection, connections
from .helpers import *
import psycopg2
import psycopg2.sql as sql


def get_user_details_after_otp_verification(user_id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            """SELECT UserId , FirstName , LastName , Email , Role  FROM dbo.Users WHERE UserId=%s""", [user_id])
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def check_existing_email_q(email):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM public.user_data WHERE email = %s AND isdeleted=0 """,[email])
        resp = cursor.fetchall()
    return resp if resp else None


def check_user_in_otp_table(user_id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            """SELECT ID FROM dbo.UsersOTP WHERE UserId=%s""", [user_id])
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def check_email_in_otp_table(email):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            """SELECT UserId , OTP FROM dbo.UsersOTP WHERE Email=%s""", [email])
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def update_user_otp(user_id, otp, date):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            """UPDATE dbo.UsersOTP SET OTP=%s , UpdatedAt=%s WHERE UserId=%s""", [otp, date, user_id])
    return resp


def insert_user_otp(data):
    with connection.cursor() as cursor:
        resp = cursor.execute("""INSERT INTO dbo.UsersOTP (OtpId,UserId,Email,Mobile,OTP,IsDeleted,CreatedAt,UpdatedAt)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", data)
    return resp


def get_user_id_from_email(email):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            """SELECT UserId , FirstName FROM dbo.Users WHERE Email=%s""", [email])
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def user_insert_q(Data):
    with connection.cursor() as cursor:
        cursor.execute("""INSERT INTO public.user_data (user_uuid , first_name, last_name, email, password, phone, address, city, country, pincode, isdeleted, createdat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING user_uuid""", Data)
        resp = dictfetchone(cursor)
    return resp


def RequestRegisterProductStatus_q(UserId, ProductID):
    with connection.cursor() as cursor:
        resp = cursor.execute(f""" SELECT ID, UserId, ProductID, AccessStatus, IsDeleted, CreatedAt, CreatedBy, UpdatedAt, UpdatedBy, RegisteredUserProductID 
        FROM dbo.RegisteredUserProduct where IsDeleted = 0 and AccessStatus = 'Enabled' and UserId = '{UserId}' and ProductID = '{ProductID}';""")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def register_product_form_insert(Data):
    with connection.cursor() as cursor:
        resp = cursor.execute("""INSERT INTO dbo.RegisteredUsersRequestedProducts (RequestID, UserId, ProductID, PartNumber, SerialNumber, 
                PurchasePlatform, PrefferedDistributor, RequestStatus, IsDeleted, CreatedAt, UpdatedAt)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", Data)
    return resp


# def check_user_q_v1(email):
#     with connection.cursor() as cursor:
#         resp = cursor.execute("SELECT UserId , FirstName , LastName , Email , Role FROM dbo.RegisteredUsers WHERE Email = %s",[email])
#         if resp and cursor.rowcount:
#             resp = dictfetchone(cursor)
#         else:
#             resp = None
#     return resp


def check_user_q_v1(email):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            "SELECT UserId , FirstName , LastName , Email , Role FROM dbo.RegisteredUsers WHERE Email = %s AND IsDeleted=0 AND Status='REGISTERED' ", [email])
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def check_last_login_user_q(user_id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            "SELECT ID FROM dbo.UserLoginLog WHERE UserId = %s", [user_id])
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def login_update_q_v1(date, user_id):
    with connection.cursor() as cursor:
        resp = cursor.execute("""UPDATE dbo.UserLoginLog 
                            SET LastLogin = %s , UpdatedAt = %s
                            WHERE UserId = %s""", [date, date, user_id])
    return resp


def login_log_insert_q(data):
    with connection.cursor() as cursor:
        resp = cursor.execute("""INSERT INTO dbo.UserLoginLog (LoginUUID,UserId,FirstName,LastName,IsDeleted,LastLogin,CreatedAt,UpdatedAt)
                              VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", data)
    return resp


def SupportsiteForm_q(data):
    with connection.cursor() as cursor:
        resp = cursor.execute("""INSERT INTO dbo.SupportPackageInquiry (SupportPackageID,FirstName,LastName,Email,PhoneNumber,
        Company,Message) VALUES (%s,%s,%s,%s,%s,%s,%s)""", data)
    return resp


def MasterProductsListLegacy_q():
    with connection.cursor() as cursor:
        sql_query = """
        SELECT ID as KeyIndex,ProductID,ProductName
        FROM dbo.ProductMaster where IsDeleted = 0 AND ProductType = 'Legacy' order by ProductName ASC
        """
        cursor.execute(sql_query)
        resp = dictfetchall(cursor) if cursor.rowcount else None
    return resp


def MasterProductsListCurrent_q():
    with connection.cursor() as cursor:
        sql_query = """
        SELECT ID as KeyIndex,ProductID,ProductName
        FROM dbo.ProductMaster where IsDeleted = 0 AND ProductType = 'Current' order by ProductName ASC
        """
        cursor.execute(sql_query)
        resp = dictfetchall(cursor) if cursor.rowcount else None
    return resp


def MasterProductsListLegacyCount_q():
    with connection.cursor() as cursor:
        resp = cursor.execute(f"""SELECT count(ID) as count 
                            FROM dbo.ProductMaster where IsDeleted = 0 AND ProductType = 'Legacy'""")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def MasterProductsListCurrentCount_q():
    with connection.cursor() as cursor:
        resp = cursor.execute(f"""SELECT count(ID) as count 
                            FROM dbo.ProductMaster where IsDeleted = 0 AND ProductType = 'Current'""")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def get_product_files_detail_by_id_q(product_id):
    with connection.cursor() as cursor:
        resp = cursor.execute("""WITH OrderedFolders AS (
                                    SELECT
                                    FolderName,
                                    ID,
                                    ROW_NUMBER() OVER (PARTITION BY FolderName ORDER BY ID) AS RowNum
                                FROM dbo.FileMaster
                                WHERE IsDeleted = 0 AND ProductID = %s	
                                                )
                    SELECT FolderName
                    FROM OrderedFolders
                    WHERE RowNum = 1
                    ORDER BY ID""",
                              [product_id])
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = None
    return resp


def get_product_description_by_id_q(product_id):
    with connection.cursor() as cursor:
        resp = cursor.execute("""SELECT ProductDescription FROM dbo.ProductMaster
                        WHERE ProductID=%s""", [product_id])
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)['ProductDescription']
        else:
            resp = ''
    return resp


def check_user_is_admin_q(user_id):
    with connection.cursor() as cursor:
        resp = cursor.execute("""SELECT Role FROM dbo.RegisteredUsers
                        WHERE UserId=%s""", [user_id])
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)['Role']
        else:
            resp = "GENERAL"
    return resp


def get_files_of_folder_product(folder_name, product_id):
    with connection.cursor() as cursor:
        resp = cursor.execute("""SELECT ID as KeyIndex ,FileID, FileName , FileType ,
                            DATENAME(month, [CreatedAt]) + ' ' + CAST(DATEPART(day, [CreatedAt]) AS VARCHAR(2)) + ', ' + CAST(DATEPART(year, [CreatedAt]) AS VARCHAR(4)) + ' ' + FORMAT([CreatedAt], 'hh:mm tt') AS CreatedAt
                            FROM dbo.FileMaster
                            WHERE IsDeleted = 0 AND ProductID=%s AND FolderName=%s
                        """, [product_id, folder_name])
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = None
    return resp


def get_file_url_from_id_q(file_id):
    with connection.cursor() as cursor:
        resp = cursor.execute("""SELECT FileUrl , FileType
                            FROM dbo.FileMaster
                            WHERE FileID=%s
                        """, [file_id])
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def get_user_type(user_id):
    with connection.cursor() as cursor:
        resp = cursor.execute("""SELECT Status , Role
                            FROM dbo.Users
                            WHERE UserId=%s
                        """, [user_id])
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def SiteFAQDetailByID_q(FAQID):
    with connection.cursor() as cursor:
        sql_query = f"""
        SELECT ID as KeyIndex, FAQID, Question, Answer, SerialNumber, IsDeleted, CreatedAt, CreatedBy, UpdatedAt, UpdatedBy
        FROM dbo.SiteFAQ where FAQID = '{FAQID}' and IsDeleted = 0
        """
        cursor.execute(sql_query)
        resp = dictfetchone(cursor) if cursor.rowcount else None
    return resp


def SiteFAQList_q(page_number, page_size):
    offset = (page_number - 1) * page_size
    with connection.cursor() as cursor:
        sql_query = f"""
            SELECT ID as KeyIndex, FAQID, Question, Answer, SerialNumber, IsDeleted, CreatedAt, CreatedBy, UpdatedAt, UpdatedBy 
            FROM dbo.SiteFAQ where IsDeleted = 0 ORDER BY ID DESC
            OFFSET {offset} ROWS
            FETCH NEXT {page_size} ROWS ONLY
        """
        cursor.execute(sql_query)
        resp = dictfetchall(cursor) if cursor.rowcount else None
    return resp


def SiteFAQListCount_q():
    with connection.cursor() as cursor:
        sql_query = f"""
            Select count(co.KeyIndex) as Count from ( SELECT ID as KeyIndex, FAQID, Question, Answer, SerialNumber, IsDeleted, CreatedAt, CreatedBy, UpdatedAt, UpdatedBy
            FROM dbo.SiteFAQ where IsDeleted = 0 ) co
        """
        cursor.execute(sql_query)
        resp = dictfetchone(cursor) if cursor.rowcount else None
    return resp


def get_file_access_registered_product(user_id, product_id):
    with connection.cursor() as cursor:
        resp = cursor.execute(f"""Select ID FROM dbo.RegisteredUserProduct WHERE
            UserId=%s AND ProductID=%s AND AccessStatus='Enabled' AND IsDeleted=0""", [user_id, product_id])
        if resp and cursor.rowcount:
            resp = True
        else:
            resp = False
    return resp


def topic_ques_q(page_number, page_size):
    offset = (page_number - 1) * page_size
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT * FROM dbo.Topics WHERE IsDeleted = 0 ORDER BY ID DESC OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY;")
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = None
    return resp


def topic_ans_q(id, page_number, page_size):
    offset = (page_number - 1) * page_size
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT * FROM dbo.TopicReply WHERE IsDeleted = 0 AND TopicID = '{id}' ORDER BY ID DESC OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY;")
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = None
    return resp


def forumcategory_q():
    with connection.cursor() as cursor:
        resp = cursor.execute(f""" SELECT fc.ID as KeyIndex ,  fc.ForumCategoryID , fc.Title , STRING_AGG(fo.ForumID, ',') AS Forum,COALESCE(COUNT(fo.ForumID), 0) AS ForumCount,
            DATENAME(month, fc.CreatedAt) + ' ' + CAST(DATEPART(day, fc.CreatedAt) AS VARCHAR(2)) + ', ' + CAST(DATEPART(year, fc.CreatedAt) AS VARCHAR(4)) + ' ' + FORMAT(fc.CreatedAt, 'hh:mm tt') AS CreatedAt
            FROM dbo.ForumCategory fc
            LEFT JOIN dbo.Forum fo ON fc.ForumCategoryID = fo.ForumCategoryID
            WHERE fc.IsDeleted = 0 AND (fo.IsDeleted = 0 OR fo.IsDeleted IS NULL) 
            GROUP BY fc.ID,fc.Title,fc.ForumCategoryID,fc.CreatedAt
            ORDER BY fc.ID DESC""")
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = None
    return resp


def forumcategory_count_q():
    with connection.cursor() as cursor:
        resp = cursor.execute(f""" SELECT count(fc.ID) as count 
            FROM dbo.ForumCategory fc
            LEFT JOIN dbo.Forum fo ON fc.ForumCategoryID = fo.ForumCategoryID
            WHERE fc.IsDeleted = 0 AND (fo.IsDeleted = 0 OR fo.IsDeleted IS NULL) 
            GROUP BY fc.ID,fc.Title,fc.ForumCategoryID,fc.CreatedAt""")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)['count']
        else:
            resp = 0
    return resp


def forumdatasearch_count_q(search_term):
    with connection.cursor() as cursor:
        resp = cursor.execute(f"""SELECT count(fc.ID) as count
            FROM dbo.ForumCategory fc
            LEFT JOIN dbo.Forum fo ON fc.ForumCategoryID = fo.ForumCategoryID
            WHERE fc.IsDeleted = 0 AND (fo.IsDeleted = 0 OR fo.IsDeleted IS NULL)
			AND (fc.Title like '%{search_term}%' OR fo.ForumTitle like '%{search_term}%' )
            GROUP BY fc.ID,fc.Title,fc.ForumCategoryID,fc.CreatedAt""")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)['count']
        else:
            resp = 0
    return resp


def get_forum_data_from_ids(forum_cat_id, forum_id):
    with connection.cursor() as cursor:
        query = f"""SELECT fo.ID as KeyIndex ,fo.ForumCategoryID, fo.ProductID , fo.ForumID , 
        fo.ForumTitle, STRING_AGG(tt.TopicID, ',') AS TopicIDs,COALESCE(COUNT(tt.TopicID), 0) AS topicscount,
        DATENAME(month, fo.CreatedAt) + ' ' + CAST(DATEPART(day, fo.CreatedAt) AS VARCHAR(2)) + ', ' + CAST(DATEPART(year, fo.CreatedAt) AS VARCHAR(4)) + ' ' + FORMAT(fo.CreatedAt, 'hh:mm tt') AS CreatedAt
        FROM dbo.Forum fo
        LEFT JOIN dbo.Topics tt ON fo.ForumID = tt.ForumID
        WHERE fo.IsDeleted=0 AND (tt.IsDeleted = 0 OR tt.IsDeleted IS NULL) AND fo.ForumCategoryID='{forum_cat_id}' AND
        fo.ForumID IN (SELECT value FROM STRING_SPLIT('{forum_id}',','))
        GROUP BY fo.ID,fo.ProductID,fo.ForumTitle,fo.CreatedAt,fo.ForumID,fo.ForumCategoryID
        ORDER BY fo.ID DESC"""
        # print("Query ========>",query)
        resp = cursor.execute(query)
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = None
    return resp


def forumdata_q(id, page_number, page_size):
    offset = (page_number - 1) * page_size
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT * FROM dbo.Forum WHERE IsDeleted = 0 AND ForumCategoryID = '{id}' ORDER BY ID DESC OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY;")
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = []
    return resp


def forumdatasearch_q(term):
    with connection.cursor() as cursor:
        resp = cursor.execute(f"""SELECT fc.ID as KeyIndex ,  fc.ForumCategoryID , fc.Title , STRING_AGG(fo.ForumID, ',') AS Forum,COALESCE(COUNT(fo.ForumID), 0) AS ForumCount,
            DATENAME(month, fc.CreatedAt) + ' ' + CAST(DATEPART(day, fc.CreatedAt) AS VARCHAR(2)) + ', ' + CAST(DATEPART(year, fc.CreatedAt) AS VARCHAR(4)) + ' ' + FORMAT(fc.CreatedAt, 'hh:mm tt') AS CreatedAt
            FROM dbo.ForumCategory fc
            LEFT JOIN dbo.Forum fo ON fc.ForumCategoryID = fo.ForumCategoryID
            WHERE fc.IsDeleted = 0 AND (fo.IsDeleted = 0 OR fo.IsDeleted IS NULL)
			AND (fc.Title like '%{term}%' OR fo.ForumTitle like '%{term}%' )
            GROUP BY fc.ID,fc.Title,fc.ForumCategoryID,fc.CreatedAt
            ORDER BY fc.ID DESC""")
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = []
    return resp


def forumdatasearch_forums_q(forum_ids):
    with connection.cursor() as cursor:
        resp = cursor.execute("""SELECT * FROM dbo.Forum WHERE IsDeleted = 0 AND 
        ForumID IN (SELECT value FROM STRING_SPLIT(%s, ','))
        ORDER BY ID DESC""", [forum_ids])
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = []
    return resp


def topicountsearch_q(id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            "SELECT count(ID) AS count FROM dbo.Topics WHERE IsDeleted = 0 AND ForumID = %s", [id])
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = {"count": 0}
    return resp


def topicount_q(id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT Count(ID) AS Count FROM dbo.Topics WHERE IsDeleted = 0 AND ForumID = '{id}';")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = []
    return resp


def forumbyid_q(id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            "SELECT * FROM dbo.Forum WHERE IsDeleted = 0 AND ForumID = %s;", [id])
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def topicbyid_q(id, page_number, page_size):
    with connection.cursor() as cursor:
        offset = (page_number - 1) * page_size
        resp = cursor.execute(
            f"SELECT * FROM dbo.Topics WHERE IsDeleted = 0 AND TopicID = '{id}' ORDER BY ID DESC OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY;")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def opportunitylist_q(id, page_number, page_size):
    offset = (page_number - 1) * page_size
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT * FROM dbo.OpportunityRegistration WHERE IsDeleted = 0 AND UserID = '{id}' ORDER BY ID DESC OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY;")
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = None
    return resp


def usercheck_q(email):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT * FROM supportsite.dbo.RegisteredUsers WHERE IsDeleted = 0 AND Email = '{email}';")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def registered_user_q(id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT RegisteredUserID, FirstName, LastName FROM dbo.RegisteredUsers WHERE UserId = '{id}';")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def registered_user_product_q(id, prodid):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT UserID, ProductID, AccessStatus FROM [dbo].[RegisteredUserProduct] WHERE UserId = '{id}' and ProductID = '{prodid}';")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def get_product_id_from_topic_id_q(topicid):
    with connection.cursor() as cursor:
        resp = cursor.execute("""
        SELECT fo.ProductID
        FROM dbo.Topics tt
        LEFT JOIN dbo.Forum fo ON tt.ForumID = fo.ForumID
        WHERE tt.IsDeleted=0 AND tt.TopicID=%s""", [topicid])
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)['ProductID']
        else:
            resp = None
    return resp


def forumtopicsprodcount_q(id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT Count(*) AS Count FROM dbo.Forum WHERE IsDeleted = 0 AND ForumID = '{id}';")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def forumtopicsprod_q(id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT * FROM dbo.Forum WHERE IsDeleted = 0 AND ForumID = '{id}';")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def forum_title_name_q(id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT * FROM dbo.Forum WHERE IsDeleted = 0 AND ForumID = '{id}';")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = ''
    return resp


def forumtopics_q(forum_id, page_number, page_size):
    offset = (page_number - 1) * page_size
    with connection.cursor() as cursor:
        resp = cursor.execute(f"""SELECT tt.ID as KeyIndex, tt.ForumID,tt.TopicID,tt.AuthorName,tt.QuestionAsked,tt.ViewsCount,
            STRING_AGG(tr.TopicReplyID, ',') AS TopicReply,COALESCE(COUNT(tr.ID), 0) AS RepliesCount,
            DATENAME(month, tt.CreatedAt) + ' ' + CAST(DATEPART(day, tt.CreatedAt) AS VARCHAR(2)) + ', ' + CAST(DATEPART(year, tt.CreatedAt) AS VARCHAR(4)) + ' ' + FORMAT(tt.CreatedAt, 'hh:mm tt') AS CreatedAt
            FROM dbo.Topics tt
            LEFT JOIN dbo.TopicReply tr ON tt.TopicID=tr.TopicID
            WHERE tt.IsDeleted = 0 AND (tr.IsDeleted=0 OR tr.IsDeleted IS NULL) AND tt.ForumID = '{forum_id}'
            GROUP BY tt.ID,tt.ForumID,tt.TopicID,tt.AuthorName,tt.QuestionAsked,tt.ViewsCount,tt.CreatedAt
            ORDER BY tt.ID DESC OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY""")
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = None
    return resp


def forumtopicscount_q(forum_id):
    with connection.cursor() as cursor:
        resp = cursor.execute(f"""
            SELECT count(co.ID) as count
            FROM(SELECT tt.ID
            FROM dbo.Topics tt
            LEFT JOIN dbo.TopicReply tr ON tt.TopicID=tr.TopicID
            WHERE tt.IsDeleted = 0 AND (tr.IsDeleted=0 OR tr.IsDeleted IS NULL) AND tt.ForumID = '{forum_id}'
            GROUP BY tt.ID,tt.ForumID,tt.TopicID,tt.AuthorName,tt.QuestionAsked,tt.ViewsCount,tt.CreatedAt) co""")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)['count']
        else:
            resp = 0
    return resp


def topicreply_q(id):
    with connection.cursor() as cursor:
        resp = cursor.execute(f"""SELECT TOP (1) ID as KeyIndex , TopicID,TopicReplyID,AuthorName,Reply,
            DATENAME(month, CreatedAt) + ' ' + CAST(DATEPART(day, CreatedAt) AS VARCHAR(2)) + ', ' + CAST(DATEPART(year, CreatedAt) AS VARCHAR(4)) + ' ' + FORMAT(CreatedAt, 'hh:mm tt') AS CreatedAt
            FROM [dbo].[TopicReply] where TopicReplyID IN (SELECT value FROM STRING_SPLIT('{id}',','))
            ORDER BY ID DESC""")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def replycount_q(id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT Count(*) AS Count FROM [dbo].[TopicReply] where TopicID = '{id}';")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def topiccount_q(id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT Count(TopicID) as Count FROM [dbo].[Topics] where ForumID = '{id}';")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def registered_user_q(id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT RegisteredUserID, FirstName, LastName FROM dbo.RegisteredUsers WHERE UserId = '{id}';")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def topic_insert_q(data):
    with connection.cursor() as cursor:
        resp = cursor.execute("""INSERT INTO dbo.Topics (TopicID,ForumID,RegisteredUserID,AuthorName,QuestionAsked,ViewsCount,IsDeleted,CreatedAt,CreatedBy,UpdatedAt,UpdatedBy)
                              VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data)
    return resp


def topicdetail_q(id):
    with connection.cursor() as cursor:
        resp = cursor.execute(f"""SELECT tt.ID, tt.ForumID, tt.TopicID, tt.RegisteredUserID, tt.AuthorName, tt.QuestionAsked, 
                            tt.ViewsCount, tt.IsDeleted, 
                            DATENAME(month, tt.CreatedAt) + ' ' + CAST(DATEPART(day, tt.CreatedAt) AS VARCHAR(2)) + ', ' + CAST(DATEPART(year, tt.CreatedAt) AS VARCHAR(4)) + ' ' + FORMAT(tt.CreatedAt, 'hh:mm tt') AS CreatedAt,
                            fo.ForumID,fo.ForumTitle FROM dbo.Topics tt 
                            JOIN dbo.Forum fo ON tt.ForumID = fo.ForumID
                            WHERE tt.IsDeleted = 0 AND tt.TopicID = '{id}' ORDER BY tt.ID DESC""")
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = None
    return resp


def topicrepliesdetailcount_q(id):
    # offset = (page_number - 1) * page_size
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT Count(*) AS Count FROM dbo.TopicReply WHERE IsDeleted = 0 AND TopicID = '{id}';")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def topicrepliesdetail_q(id, page_number, page_size):
    offset = (page_number - 1) * page_size
    with connection.cursor() as cursor:
        resp = cursor.execute(f"""SELECT ID, TopicID, TopicReplyID, RegisteredUserID, AuthorName, Reply, IsDeleted, 
                DATENAME(month, [CreatedAt]) + ' ' + CAST(DATEPART(day, [CreatedAt]) AS VARCHAR(2)) + ', ' + CAST(DATEPART(year, [CreatedAt]) AS VARCHAR(4)) + ' ' + FORMAT([CreatedAt], 'hh:mm tt') AS CreatedAt
                FROM dbo.TopicReply WHERE IsDeleted = 0 AND TopicID = '{id}' ORDER BY ID DESC OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY""")
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = None
    return resp


def topicviewcount_q(id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT ViewsCount FROM dbo.Topics WHERE IsDeleted = 0 AND TopicID = '{id}';")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def registered_user_q(id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT RegisteredUserID, FirstName, LastName FROM dbo.RegisteredUsers WHERE UserId = '{id}';")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def check_user_registered_or_not_q(prod_id, user_id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            "SELECT ID FROM dbo.RegisteredUserProduct WHERE ProductID=%s AND UserId = %s", [prod_id, user_id])
        if resp and cursor.rowcount:
            resp = True
        else:
            resp = False
    return resp


def file_accessible_q(product_id, user_id):
    with connection.cursor() as cursor:
        resp = cursor.execute("""SELECT ID FROM dbo.RegisteredUserProduct 
                WHERE UserId = %s AND ProductID=%s AND AccessStatus='Enabled' """, [user_id, product_id])
        if resp and cursor.rowcount:
            resp = True
        else:
            resp = False
    return resp


def forumcategory_search_q(term, page_number, page_size):
    offset = (page_number - 1) * page_size
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"select * from ForumCategory fc join Forum f on fc.ForumCategoryID = f.ForumCategoryID where f.ForumTitle like '%{term}%' or fc.Title like '%{term}%' ORDER BY fc.ID DESC OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY;")
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = None
    return resp


def get_prod_id_from_forum_id_q(forum_id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"select ProductID from Forum where ForumID='{forum_id}'")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)['ProductID']
        else:
            resp = None
    return resp


def topic_search_q(term, page_number, page_size):
    offset = (page_number - 1) * page_size
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"select * from topics tt join topicreply tr on tt.TopicID = tr.TopicID where tt.AuthorName like '%{term}%' or tr.AuthorName like '%{term}%' or tt.QuestionAsked like '%{term}%' or tr.Reply like '%{term}%' ORDER BY tt.ID DESC OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY;")
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = None
    return resp


def topic_reply_insert_q(data):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            """INSERT INTO dbo.TopicReply (TopicID,TopicReplyID,RegisteredUserID,AuthorName,Reply,IsDeleted,CreatedAt,CreatedBy,UpdatedAt,UpdatedBy) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data)
    return resp


def FeedbackForm_q(data):
    with connection.cursor() as cursor:
        resp = cursor.execute("""Insert into dbo.Feedback ( FeedbackID, FirstName, LastName, Contact, Email, Company, FeedbackType, Feedback)
        values( %s,%s,%s,%s,%s,%s,%s,%s )""", data)
    return resp


def opportunityregister_q(data):
    with connection.cursor() as cursor:
        resp = cursor.execute("""INSERT INTO supportsite.dbo.OpportunityRegistration (OpportunityID,LRNNumber,UserID,FirstName,LastName,CompanyName,Email,Phone,OpportunityStatus,SalesName,SalesEmail,SalesPhone,FAEName,FAEEmail,FAEPhone,CustomerCompanyName,	CustomerMarket,Address,City,State,PostalCode,Country,CustomerWebsite,EngineerName1,EngineerEmail1,EngineerName2,EngineerEmail2,	EngineerName3,EngineerEmail3,ProjectName,ProjectDescription,PrototypeDate,ProductionDate,ProjectType,EAU,LogicPDModelNumber,LogicPDModelNumber2,LogicPDModelNumber3,comment,IsDeleted,CreatedAt,CreatedBy,UpdatedAt,UpdatedBy) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data)
    return resp


def lrncheck_q():
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT TOP 1 * FROM supportsite.dbo.OpportunityRegistration WHERE IsDeleted = 0 ORDER BY ID DESC;")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def usercheckopp_q(userid):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT * FROM supportsite.dbo.RegisteredUsers WHERE IsDeleted = 0 AND UserId = '{userid}' and Role = 'PARTNER';")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def admin_users_q():
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT FirstName, LastName, Email FROM [supportsite].[dbo].[AdminUsers];")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def opportunitybyuserid_q(id, page_number, page_size):
    offset = (page_number - 1) * page_size
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT * FROM supportsite.dbo.OpportunityRegistration WHERE IsDeleted = 0 AND OpportunityID = '{id}' ORDER BY ID DESC OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY;")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def unansweredtopics_q(page_number, page_size):
    offset = (page_number - 1) * page_size
    with connection.cursor() as cursor:
        sql_query = f""" SELECT t.TopicID, t.AuthorName, t.QuestionAsked FROM Topics t LEFT JOIN Topicreply tr ON t.TopicID = tr.TopicID WHERE tr.TopicID IS NULL AND t.IsDeleted = 0 ORDER BY t.ID DESC OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY; """
        cursor.execute(sql_query)
        resp = dictfetchall(cursor) if cursor.rowcount else None
    return resp


def unansweredtopicscount_q():
    with connection.cursor() as cursor:
        sql_query = f"""SELECT Count(t.TopicID) AS Count FROM Topics t LEFT JOIN Topicreply tr ON t.TopicID = tr.TopicID WHERE tr.TopicID IS NULL AND t.IsDeleted = 0; """
        cursor.execute(sql_query)
        resp = dictfetchone(cursor) if cursor.rowcount else None
    return resp


def TDGForumSearch_q(where_clause, query_parameters, page_number, page_size):
    offset = (page_number - 1) * page_size
    with connection.cursor() as cursor:
        sql_query = f"""
			Select  tp.QuestionAsked, tp.TopicID, tp.AuthorName as TopicsAuthorName, tp.CreatedAt As TopicCreatedAt
            from dbo.Topics tp 
            left join dbo.TopicReply tr on tp.TopicID = tr.TopicID
            where tp.IsDeleted = 0 and tr.IsDeleted = 0 and {where_clause} order by tr.ID desc
            OFFSET {offset} ROWS
            FETCH NEXT {page_size} ROWS ONLY
        """
        cursor.execute(sql_query, query_parameters)
        resp = dictfetchall(cursor) if cursor.rowcount else None
    return resp


def TDGForumSearchCount_q(where_clause, query_parameters):
    with connection.cursor() as cursor:
        sql_query = f"""
            Select count(co.reply) as Count from (Select tr.reply,tp.TopicID, tp.QuestionAsked, tp.AuthorName as TopicsAuthorName, tr.AuthorName as TopicReplyAuthorName, tp.CreatedAt As TopicCreatedAt, tr.CreatedAt as TopicReplyCreatedAt
            from dbo.Topics tp 
            left join dbo.TopicReply tr on tp.TopicID = tr.TopicID
            where tp.IsDeleted = 0 and tr.IsDeleted = 0 and {where_clause} ) co
        """
        cursor.execute(sql_query, query_parameters)
        resp = dictfetchone(cursor) if cursor.rowcount else None
    return resp


def TopicwiseReplyData_q(UID):
    with connection.cursor() as cursor:
        sql_query = f"""
            Select ID as KeyIndex, TopicID,TopicReplyID,RegisteredUserID,AuthorName,Reply,IsDeleted,CreatedAt,CreatedBy,UpdatedAt,UpdatedBy
            From dbo.TopicReply where IsDeleted = 0 and TopicID = '{UID}' Order by ID desc
        """
        cursor.execute(sql_query)
        resp = dictfetchall(cursor) if cursor.rowcount else None
    return resp


def TopicwiseReplyDataCount_q(UID):
    with connection.cursor() as cursor:
        sql_query = f"""
            Select count(co.KeyIndex) as count from ( Select ID as KeyIndex, TopicID,TopicReplyID,RegisteredUserID,AuthorName,Reply,IsDeleted,CreatedAt,CreatedBy,UpdatedAt,UpdatedBy
            From dbo.TopicReply where IsDeleted = 0 and TopicID = '{UID}' ) co
        """
        cursor.execute(sql_query)
        resp = dictfetchone(cursor) if cursor.rowcount else None
    return resp


def admin_users_q():
    with connection.cursor() as cursor:
        resp = cursor.execute(
            f"SELECT FirstName, LastName, Email FROM [supportsite].[dbo].[AdminUsers];")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def opportunityupdate_q(data):
    with connection.cursor() as cursor:
        sql = """
            UPDATE dbo.OpportunityRegistration 
            SET 
                LRNNumber = %s,
                UserID = %s,
                FirstName = %s,
                LastName = %s,
                CompanyName = %s,
                Email = %s,
                Phone = %s,
                SalesName = %s,
                SalesEmail = %s,
                SalesPhone = %s,
                FAEName = %s,
                FAEEmail = %s,
                FAEPhone = %s,
                CustomerCompanyName = %s,
                CustomerMarket = %s,
                Address = %s,
                City = %s,
                State = %s,
                PostalCode = %s,
                Country = %s,
                CustomerWebsite = %s,
                EngineerName1 = %s,
                EngineerEmail1 = %s,
                EngineerName2 = %s,
                EngineerEmail2 = %s,
                EngineerName3 = %s,
                EngineerEmail3 = %s,
                ProjectName = %s,
                ProjectDescription = %s,
                PrototypeDate = %s,
                ProductionDate = %s,
                ProjectType = %s,
                EAU = %s,
                LogicPDModelNumber = %s,
                LogicPDModelNumber2 = %s,
                LogicPDModelNumber3 = %s,
                IsDeleted = %s,
                CreatedAt = %s,
                CreatedBy = %s,
                UpdatedAt = %s,
                UpdatedBy = %s
            WHERE
                OpportunityID=%s
        """
        resp = cursor.execute(sql, data)
    return resp


def opportunitycheck_q(userid, oppid):
    with connection.cursor() as cursor:
        resp = cursor.execute(f"""SELECT * FROM [dbo].[OpportunityRegistration] WHERE IsDeleted = 0
                               AND UserID = '{userid}' and OpportunityID = '{oppid}';""")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def TopicById_q(TopicID):
    with connection.cursor() as cursor:
        sql_query = f"""
			SELECT ID, ForumID, TopicID, RegisteredUserID, AuthorName, QuestionAsked, ViewsCount, IsDeleted, CreatedAt, CreatedBy, UpdatedAt, UpdatedBy 
            FROM dbo.Topics where IsDeleted = 0 and TopicID = '{TopicID}'
        """
        cursor.execute(sql_query)
        resp = dictfetchone(cursor) if cursor.rowcount else None
    return resp


def TopicReplySearch_q(TopicID, SearchTerm, page_number, page_size):
    offset = (page_number - 1) * page_size
    with connection.cursor() as cursor:
        sql_query = f"""
			SELECT ID as KeyIndex, TopicID, TopicReplyID, RegisteredUserID, AuthorName, Reply, 
            IsDeleted, CreatedAt, CreatedBy, UpdatedAt, UpdatedBy FROM dbo.TopicReply where TopicID = '{TopicID}' and 
            ( Reply LIKE '%{SearchTerm}%' or AuthorName LIKE '%{SearchTerm}%' )and IsDeleted =0 order by ID desc 
            OFFSET {offset} ROWS
            FETCH NEXT {page_size} ROWS ONLY
        """
        cursor.execute(sql_query)
        resp = dictfetchall(cursor) if cursor.rowcount else None
    return resp


def TopicReplySearchCount_q(TopicID, SearchTerm):
    with connection.cursor() as cursor:
        sql_query = f"""
            Select count(co.reply) as Count from (SELECT ID as KeyIndex, TopicID, TopicReplyID, RegisteredUserID, AuthorName, Reply, 
            IsDeleted, CreatedAt, CreatedBy, UpdatedAt, UpdatedBy FROM dbo.TopicReply where TopicID = '{TopicID}' and 
            ( Reply LIKE '%{SearchTerm}%' or AuthorName LIKE '%{SearchTerm}%' ) and IsDeleted =0) co
        """
        cursor.execute(sql_query)
        resp = dictfetchone(cursor) if cursor.rowcount else None
    return resp


def GetUserDetails_q(UserId):
    with connection.cursor() as cursor:
        resp = cursor.execute(f"""SELECT ID as KeyIndex, RegisteredUserId, UserId, FirstName, LastName, Email, Mobile, Company, Industry, 
                Address, Country, City, PostalId, Region, Status, Role, IsDeleted, CreatedAt, CreatedBy, UpdatedAt, UpdatedBy 
                FROM dbo.RegisteredUsers where IsDeleted=0 and UserId = '{UserId}';""")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = 0
    return resp


def GetUserRegisteredProducts_q(UserId):
    with connection.cursor() as cursor:
        resp = cursor.execute(f"""SELECT RUP.ID as KeyIndex, 
       RUP.UserID, 
       RUP.ProductID, 
       RUP.AccessStatus, 
       RUP.IsDeleted, 
       RUP.CreatedAt, 
       RUP.CreatedBy, 
       RUP.UpdatedAt, 
       RUP.UpdatedBy,
       PM.ProductName,  
       PM.ProductDescription,
        RURP.RequestStatus,
        RURP.CreatedAt AS RequestedAt

FROM dbo.RegisteredUserProduct RUP
JOIN dbo.ProductMaster PM ON RUP.ProductID = PM.ProductID
JOIN dbo.RegisteredUsersRequestedProducts RURP ON RUP.ProductID = RURP.ProductID
WHERE RUP.IsDeleted = 0 
  AND RUP.AccessStatus = 'Enabled' 
  AND PM.IsDeleted = 0                          
  AND RUP.UserID = '{UserId}'""")
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = None
    return resp


def get_file_info_q(ProductID):
    with connection.cursor() as cursor:
        resp = cursor.execute("""SELECT FileID,FileName,FileType,SerialNumber,FileUrl,FolderName,CreatedAt
                               FROM dbo.FileMaster WHERE ProductID = %s AND IsDeleted = 0""", [ProductID])
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = None
    return resp


def get_folder_names_q(ProductID):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            "SELECT DISTINCT FolderName FROM [supportsite].[dbo].[FileMaster ] WHERE ProductID = %s", [ProductID])
        if resp and cursor.rowcount:
            resp = dictfetchall(cursor)
        else:
            resp = None
    return resp


def getuserdetails_q(userid):
    with connection.cursor() as cursor:
        resp = cursor.execute(f"""SELECT ID as KeyIndex, RegisteredUserId, UserId, FirstName, LastName, Email, Mobile, Company, Industry, 
                Address, Country, City, PostalId, Region, Status, Role, IsDeleted, CreatedAt, CreatedBy, UpdatedAt, UpdatedBy 
                FROM dbo.RegisteredUsers where IsDeleted=0 and UserId = '{userid}'""")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def userdetailsupdate_ru_q(data):
    with connection.cursor() as cursor:
        resp = cursor.execute("""
            UPDATE dbo.RegisteredUsers
            SET
                FirstName = %s,
                LastName = %s,
                Mobile = %s,
                UpdatedAt=%s
            WHERE
                UserId=%s
        """, data)

    return resp


def userdetailsupdate_asu_q(data):
    with connection.cursor() as cursor:
        resp = cursor.execute("""
            UPDATE dbo.Users
            SET
                FirstName = %s,
                LastName = %s,
                Mobile = %s,
                UpdatedAt=%s
            WHERE
                UserId=%s
        """, data)

    return resp


def HomepageBannerlist_q():
    with connection.cursor() as cursor:
        resp = cursor.execute(
            """SELECT TOP(1) BannerID, Title, Description, MobileImage, WebImage, IsDeleted, CreatedAt, CreatedBy, UpdatedAt, UpdatedBy FROM dbo.HomePage order by ID desc""")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def HomepageBannerlistcount_q():
    with connection.cursor() as cursor:
        resp = cursor.execute(
            """SELECT count(ID) as count FROM supportsite.dbo.HomePage""")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def CheckUserDetailByEmail_q(data):
    with connection.cursor() as cursor:
        resp = cursor.execute(f"""SELECT ID, RegisteredUserId, UserId, FirstName, LastName, Email, Mobile, Company, Industry, Address, Country, City, 
        PostalId, Region, Status, Role, IsDeleted, CreatedAt, CreatedBy, UpdatedAt, UpdatedBy 
        FROM supportsite.dbo.RegisteredUsers where IsDeleted= 0 and Email = '{data}';""")
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def Microsoftlogin_update_q_v1(date, user_id):
    with connection.cursor() as cursor:
        resp = cursor.execute("""UPDATE dbo.UserLoginLog 
                            SET LastLogin = %s , UpdatedAt = %s
                            WHERE UserId = %s""", [date, date, user_id])
    return resp


def Microsoftcheck_last_login_user_q(user_id):
    with connection.cursor() as cursor:
        resp = cursor.execute(
            "SELECT ID FROM dbo.UserLoginLog WHERE UserId = %s", [user_id])
        if resp and cursor.rowcount:
            resp = dictfetchone(cursor)
        else:
            resp = None
    return resp


def Microsoftlogin_log_insert_q(data):
    with connection.cursor() as cursor:
        resp = cursor.execute("""INSERT INTO dbo.UserLoginLog (LoginUUID,UserId,FirstName,LastName,IsDeleted,LastLogin,CreatedAt,UpdatedAt)
                              VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", data)
    return resp
