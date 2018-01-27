from mysql import connector
from pprint import pprint
import mysql

class table1:

 mySqlConnector = mysql.connector.connect(user="root", password="", host="127.0.0.1", database="pytest")

 def __init__(self):
  self.ValueList = list()
  self.tableName = ""
  self.ParameterList = []
  self._select()
    
 def _insert(self, list):
  if isinstance(list, tuple):
   cursor = self.mySqlConnector.cursor()
   Question="INSERT INTO `table1` (`option1`,`option2`,`option3`,`option4`) VALUES (NULL,%s,%s,%s)"
   cursor.execute(Question, list)
   self.mySqlConnector.commit()
   cursor.close()
   self._select()

 def _update(self, list):
  if isinstance(list, tuple):
   cursor = self.mySqlConnector.cursor()
   Question="UPDATE `table1` SET `option2`=%s,`option3`=%s,`option4`=%s WHERE `option1`=%s"
   cursor.execute(Question, list)
   self.mySqlConnector.commit()
   cursor.close()
   self._select()

 def _delete(self, list):
  if isinstance(list, tuple):
   cursor = self.mySqlConnector.cursor()
   Question="DELETE FROM `table1` WHERE `option1`=%s"
   cursor.execute(Question, list)
   self.mySqlConnector.commit()
   cursor.close()
   self._select()

 def _select(self):
   cursor = self.mySqlConnector.cursor()
   Question="SELECT `option1`,`option2`,`option3`,`option4` FROM `table1`"
   cursor.execute(Question)
   self.ValueList = cursor.fetchall()
   cursor.close()
   return self.ValueList

 """
	only for "User" table....
 """
 def isRegestrated(self, login, passwd):
   passwd1 = str(passwd).lower()
   cursor = self.mySqlConnector.cursor()
   Question="SELECT * FROM `User` WHERE `login`=%s AND `password`=%s"
   cursor.execute(Question, tuple((login, passwd1)))
   self.ValueList = cursor.fetchall()
   cursor.close()
   return self.ValueList


 def add(self, option2, option3, option4):
  return self._insert(tuple((option2, option3, option4)))

 def change(self, option2, option3, option4, option1):
  return self._update(tuple((option2, option3, option4, option1)))

 def remove(self, option1):
  return self._delete(tuple((option1,)))

 def view(self):
  return self.ValueList

 def __iter__(self):
  self.index_of_element = -1
  return self

 def __next__(self):
  self.index_of_element += 1
  if(len(self.ValueList)-1 < self.index_of_element):
   raise StopIteration
  else:
   return [self.ValueList[self.index_of_element], self.index_of_element]



pprint(globals())
MyComp = compile(sssss, '', 'exec')
exec(MyComp)

