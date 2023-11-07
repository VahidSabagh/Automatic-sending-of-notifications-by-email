import datetime

from Input_data import Input_data
from transaction import transaction_ItemPack, transaction_ItemRegister, transaction_Item
from datagathering_from_DataBase import datagathering

now = datetime.datetime.now()
print('now1:',now)
duration,list1,recipients,Entity_dict_ItemPack,Entity_dict_ItemRegister,Entity_dict_Item=Input_data()
print('now2:',datetime.datetime.now())
Item_df,ItemPack_df,ItemRegister_df=datagathering('172.31.2.18','Test','hz','hz')

print('ItemRegister_df:',len(ItemRegister_df))
print('now3:',datetime.datetime.now())
for n1 in range(len(Entity_dict_ItemPack)):
    transaction_ItemPack(ItemPack_df,list(Entity_dict_ItemPack.keys())[n1],now,duration,list1,recipients,list(Entity_dict_ItemPack.values())[n1])

for m1 in range(len(Entity_dict_ItemRegister)):
    transaction_ItemRegister(ItemRegister_df, list(Entity_dict_ItemRegister.keys())[m1], now, duration, list1, recipients, list(Entity_dict_ItemRegister.values())[m1])

for t1 in range(len(Entity_dict_Item)):
    transaction_Item(Item_df,list(Entity_dict_Item.keys())[t1],now,duration,list1,recipients,list(Entity_dict_Item.values())[t1])
print('now4:',datetime.datetime.now())
print('Success')