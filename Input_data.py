
def Input_data ():
    duration = 86400
    list1 = [15]
    recipients = [['eamilname@email.com']]

    Entity_dict_ItemPack = {'BarCode': "تغییر وضعیت بارکد کالا",
                            'KasbID_Name': "تغییر وضعیت گروه کسب و کار کالا",
                            'StandardID_Name': "تغییر وضعیت گروه استاندارد کسب وکار کالا",
                            'BrandId_Name': "تغییر وضعیت برند کالا",
                            'Vendor_Name': "تغییر وضعیت تأمین کننده کالا",
                            'BazCategoryID_Name': "تغییر وضعیت گروه بازار کالا",
                            'EstrategicId_Name': "تغییر وضعیت گروه استراتژی کالا"
                            }
    Entity_dict_ItemRegister = {'ProductCode': "تغییر وضعیت کد کالا (ProductCode)",
                                'PackCode_Code': "تغییر وضعیت شناسه کالا (PackCode)"
                                }
    Entity_dict_Item = {'ICB8_Name': "تغییر وضعیت گروهبندی کالا (ICB8)"}

    return duration,list1,recipients,Entity_dict_ItemPack,Entity_dict_ItemRegister,Entity_dict_Item
