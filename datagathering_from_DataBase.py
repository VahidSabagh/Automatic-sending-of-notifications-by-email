import pyodbc
import time
import datetime
import numpy as np
import pandas as pd

def datagathering (server,database,username,password):
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' +
                          server+';DATABASE='+database+';UID='+username+';PWD=' + password)
    cnxn.autocommit = True
    cursor = cnxn.cursor()

    query1 = '''select r.Code,r.Name,r.CompanyCode_Code ,r.PackCode_Code,r.ProductCode,r.EnterDateTime
    from [MDM].[mdm].[ItemRegisterHistory] r 
    where  r.Name in
    (
    select  r.Name
    from [MDM].[mdm].[ItemRegisterHistory] r
    group by r.Name
    having COUNT(distinct r.Code) > 1) and r.ApplicationCode_Code=1 and r.CompanyCode_Code in (15,43,59)
    order by r.Code desc,r.RevisionID  
    '''

    ItemRegister_df = pd.read_sql_query(query1, cnxn)
    cnxn.commit()

    query2 = '''select  
     r.Code,p.Name,r.CompanyCode_Code ,r.PackCode_Code,p.EnterDateTime,p.NoInPack,p.BarCode,
     p.BazCategoryID_Name,p.BazCategoryID_Code,p.EstrategicId_Name,p.EstrategicId_Code,p.KasbID_Name,p.KasbID_Code,p.StandardID_Code
     ,p.StandardID_Name,
     p.Vendor_Name,p.Vendor_Code,p.BrandId_Name,p.BrandId_Code,p.RevisionID
    from [MDM].[mdm].[ItemPackHistory] p 
    join [MDM].[mdm].[ItemRegisterHistory] r on  p.Code=r.PackCode_Code
    where r.ApplicationCode_Code=1 
    and r.CompanyCode_Code in (15,43,59) 
    order by r.Code desc,p.RevisionID   
    '''

    ItemPack_df = pd.read_sql_query(query2, cnxn)
    cnxn.commit()

    query3 = '''select distinct 
     r.Code,t.Name,r.CompanyCode_Code ,r.PackCode_Code,t.EnterDateTime,t.ICB8_Name,t.ICB8_Code
    from [MDM].[mdm].[ItemHistory] t    
    join [MDM].[mdm].[ItemPackHistory] p on  p.ItemCode_Code=t.Code  
    join [MDM].[mdm].[ItemRegisterHistory] r on  p.Code=r.PackCode_Code
    where r.ApplicationCode_Code=1 and ICB8_Name is not null
     and r.CompanyCode_Code in (15,43,59)  
    '''

    Item_df = pd.read_sql_query(query3, cnxn)
    cnxn.commit()

    return Item_df,ItemPack_df,ItemRegister_df

