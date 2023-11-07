import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import warnings
warnings.filterwarnings('ignore')

def ddhhmmss(text):
    return text.total_seconds()

# step1 ItemPack

def transaction_ItemPack(ItemPack_df,Entity,now,duration,list1,recipients,subject):

    data = ItemPack_df.dropna(subset=[Entity])  # remove null

    newdf = data.drop_duplicates(subset=["Code", "CompanyCode_Code", Entity]).reset_index(drop=True)  # remove duplicate
    # newdf['old_'.format(Entity)] = ''  # Create empty Col
    newdf['Old_Item'] = ''  # Create empty Col

    newdf = newdf[newdf.duplicated(subset=['Code'], keep=False)].reset_index(drop=True)

    # Step1_1
    df = newdf.drop_duplicates(subset=['Code'], keep='first', inplace=False).reset_index(drop=True)
    dfcount = newdf.groupby(by=['Code'], sort=False).count()

    b = 0
    tbl = []
    for i in range(0, len(df)):
        b = (dfcount[Entity].iloc[i]) + b
        t = (dfcount[Entity].iloc[i])

        for j in range(b - t + 1, b, 1):
            if (newdf.Code[j] == newdf.Code[j - 1]) & ((newdf[Entity][j] != newdf[Entity][j - 1])):
                tbl.append(j)

                newdf.Old_Item[j]= newdf[str(Entity)][j - 1]

    Final_tbl = newdf.iloc[tbl, :].reset_index(drop=True)
    Final_tbl['AbsTime'] = now - Final_tbl['EnterDateTime']

    Final_tbl['less_24h'] = Final_tbl['AbsTime'].apply(ddhhmmss)

    Final_tbl = Final_tbl[Final_tbl['less_24h'] < duration].reset_index(drop=True)

    #step1-2: send email

    for n in range(len(list1)):
        m = list1[n]
        filterdata = Final_tbl[Final_tbl['CompanyCode_Code'] == str(m)].reset_index(drop=True)
        recipient = recipients[n]

        if len(filterdata) == 0:
            continue

        emaillist = [elem.strip().split(',') for elem in recipient]
        for num in range(0, len(filterdata)):
            msg = MIMEMultipart()
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = 'changes.notification.gig@gmail.com'
            body = '''
            <html dir="rtl" lang="fa-IR">
            <head>
             <meta charset="utf-8">
            </head>

            <body style="direction: rtl;">
             <p style="font-size:120%">با سلام و احترام،</p>
             <p style="font-size:140%">به استحضار می‌رساند:</p>
             <p style="font-size:140%">کالا با نام {0}، با کد رجیستر {1}، از {2} به {3} تغییر پیدا کرد.</p>
             <p style="font-size:120%">با تشکر</p>
             <p>تیم مهندسی و تحلیل داده گلرنگ سیستم (Golrang System Analytics team)</p>
            </body> 
            </html>'''.format(filterdata['Name'][num], filterdata['Code'][num]
                              , filterdata['Old_Item'][num], filterdata[str(Entity)][num])
            body = ("<div style='direction:rtl'>" + body + "</div>")
            msg.attach(MIMEText(body, 'html', _charset='UTF-8'))

            try:
                """Checking for connection errors"""
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()  # NOT NECESSARY
                server.starttls()
                server.ehlo()  # NOT NECESSARY
                server.login('changes.notification.gig@gmail.com', 'bkxckcoyajmeigve')
                server.sendmail(msg['From'], emaillist, msg.as_string())
                server.close()

            except Exception as e:
                print("Error for connection: {}".format(e))

    return Final_tbl



# step2 ItemRegister ===========================================================================================================================

def transaction_ItemRegister(ItemRegister_df,Entity,now,duration,list1,recipients,subject):
    data = ItemRegister_df.dropna(subset=[Entity])  # remove null
    newdf = data.drop_duplicates(subset=["Code", "CompanyCode_Code", Entity]).reset_index(drop=True)  # remove duplicate
    newdf['Old_Item'] = ''  # Create empty Col
    newdf = newdf[newdf.duplicated(subset=['Code'], keep=False)].reset_index(drop=True)

    # Step1_1
    df = newdf.drop_duplicates(subset=['Code'], keep='first', inplace=False).reset_index(drop=True)
    dfcount = newdf.groupby(by=['Code'], sort=False).count()

    b = 0
    tbl = []
    for i in range(0, len(df)):
        b = (dfcount[Entity].iloc[i]) + b
        t = (dfcount[Entity].iloc[i])

        for j in range(b - t + 1, b, 1):
            if (newdf.Code[j] == newdf.Code[j - 1]) & ((newdf[Entity][j] != newdf[Entity][j - 1])):
                tbl.append(j)

                newdf.Old_Item[j]= newdf[str(Entity)][j - 1]

    Final_tbl = newdf.iloc[tbl, :].reset_index(drop=True)
    Final_tbl['AbsTime'] = now - Final_tbl['EnterDateTime']


    Final_tbl['less_24h'] = Final_tbl['AbsTime'].apply(ddhhmmss)

    Final_tbl = Final_tbl[Final_tbl['less_24h'] < duration].reset_index(drop=True)

    #step1-2: send email

    for n in range(len(list1)):
        m = list1[n]
        filterdata = Final_tbl[Final_tbl['CompanyCode_Code'] == str(m)].reset_index(drop=True)
        recipient = recipients[n]

        if len(filterdata) == 0:
            continue

        emaillist = [elem.strip().split(',') for elem in recipient]
        for num in range(0, len(filterdata)):
            msg = MIMEMultipart()
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = 'changes.notification.gig@gmail.com'
            body = '''
            <html dir="rtl" lang="fa-IR">
            <head>
             <meta charset="utf-8">
            </head>

            <body style="direction: rtl;">
             <p style="font-size:120%">با سلام و احترام،</p>
             <p style="font-size:140%">به استحضار می‌رساند:</p>
             <p style="font-size:140%">کالا با نام {0}، با کد رجیستر {1}، از {2} به {3} تغییر پیدا کرد.</p>
             <p style="font-size:120%">با تشکر</p>
             <p>تیم مهندسی و تحلیل داده گلرنگ سیستم (Golrang System Analytics team)</p>
            </body> 
            </html>'''.format(filterdata['Name'][num], filterdata['Code'][num]
                              , filterdata['Old_Item'][num], filterdata[str(Entity)][num])
            body = ("<div style='direction:rtl'>" + body + "</div>")
            msg.attach(MIMEText(body, 'html', _charset='UTF-8'))

            try:
                """Checking for connection errors"""
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()  # NOT NECESSARY
                server.starttls()
                server.ehlo()  # NOT NECESSARY
                server.login('changes.notification.gig@gmail.com', 'bkxckcoyajmeigve')
                server.sendmail(msg['From'], emaillist, msg.as_string())
                server.close()

            except Exception as e:
                print("Error for connection: {}".format(e))

    return Final_tbl







# step3 Item ===========================================================================================================================

def transaction_Item(Item_df,Entity,now,duration,list1,recipients,subject):
    data = Item_df.dropna(subset=[Entity])  # remove null
    newdf = data.drop_duplicates(subset=["Code", "CompanyCode_Code", Entity]).reset_index(drop=True)  # remove duplicate
    newdf.sort_values(by=['Code', 'EnterDateTime'], ascending=[True, True], ignore_index=True, inplace=True)
    newdf['Old_Item'] = ''  # Create empty Col
    newdf = newdf[newdf.duplicated(subset=['Code'], keep=False)].reset_index(drop=True)

    # Step1_1
    df = newdf.drop_duplicates(subset=['Code'], keep='first', inplace=False).reset_index(drop=True)
    dfcount = newdf.groupby(by=['Code'], sort=False).count()

    b = 0
    tbl = []
    for i in range(0, len(df)):
        b = (dfcount[Entity].iloc[i]) + b
        t = (dfcount[Entity].iloc[i])

        for j in range(b - t + 1, b, 1):
            if (newdf.Code[j] == newdf.Code[j - 1]) & ((newdf[Entity][j] != newdf[Entity][j - 1])):
                tbl.append(j)

                newdf.Old_Item[j]= newdf[str(Entity)][j - 1]

    Final_tbl = newdf.iloc[tbl, :].reset_index(drop=True)
    Final_tbl['AbsTime'] = now - Final_tbl['EnterDateTime']


    Final_tbl['less_24h'] = Final_tbl['AbsTime'].apply(ddhhmmss)

    Final_tbl = Final_tbl[Final_tbl['less_24h'] < duration].reset_index(drop=True)

    #step1-2: send email

    for n in range(len(list1)):
        m = list1[n]
        filterdata = Final_tbl[Final_tbl['CompanyCode_Code'] == str(m)].reset_index(drop=True)
        recipient = recipients[n]

        if len(filterdata) == 0:
            continue

        emaillist = [elem.strip().split(',') for elem in recipient]

        for num in range(0, len(filterdata)):
            msg = MIMEMultipart()
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = 'changes.notification.gig@gmail.com'
            body ='''
            <html dir="rtl" lang="fa-IR">
            <head>
             <meta charset="utf-8">
            </head>
             
            <body style="direction: rtl;">
             <p style="font-size:120%">با سلام و احترام،</p>
             <p style="font-size:140%">به استحضار می‌رساند:</p>
             <p style="font-size:140%">کالا با نام {0}، با کد رجیستر {1}، از {2} به {3} تغییر پیدا کرد.</p>
             <p style="font-size:120%">با تشکر</p>
             <p>تیم مهندسی و تحلیل داده گلرنگ سیستم (Golrang System Analytics team)</p>
            </body> 
            </html>'''.format(filterdata['Name'][num], filterdata['Code'][num]
                       , filterdata['Old_Item'][num], filterdata[str(Entity)][num])
            body = ("<div style='direction:rtl'>" + body + "</div>")
            msg.attach(MIMEText(body, 'html', _charset='UTF-8'))
            try:
                """Checking for connection errors"""
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()  # NOT NECESSARY
                server.starttls()
                server.ehlo()  # NOT NECESSARY
                server.login('changes.notification.gig@gmail.com', 'bkxckcoyajmeigve')
                server.sendmail(msg['From'], emaillist, msg.as_string())
                server.close()

            except Exception as e:
                print("Error for connection: {}".format(e))

    return Final_tbl
