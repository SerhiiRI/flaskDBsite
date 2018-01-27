from mysql import connector
from pprint import pprint
import mysql


class Construct(object):

    def __init__(self, table_name, table_column):
        self.TableName = table_name
        self.TableColumn = table_column
        self.classString = "class "+self.TableName+":"
        self._dictionarySql = {"insert": ["INSERT INTO `{}` ({}) VALUES (NULL,{})".format(self.TableName, self._ParamList(),self._ParamHideList())],
            "update": ["UPDATE `{}` SET {} WHERE `{}`=%s".format(self.TableName, self._ParamListNoKey(wskaz="`=%s"),self.TableColumn[0])],
            "delete": ["DELETE FROM `{}` WHERE `{}`=%s".format(self.TableName, self.TableColumn[0])],
            "select": ["SELECT {} FROM `{}`".format(self._ParamList(), self.TableName)]}
        self._dictionaryAction = {
            "add": ["self, {}".format(self._optionListNoKey()), "self._insert(tuple(({})))".format(self._optionListNoKey())],
            "change": ["self, {}, {}".format(self._optionListNoKey(), self._optionKey()), "self._update(tuple(({}, {})))".format(self._optionListNoKey(), self._optionKey())],
            "remove": ["self, {}".format(self._optionKey()), "self._delete(tuple(({},)))".format(self._optionKey())],
            "view": ["self", "self.ValueList"]}
        if self.TableName=="user":
            self.classString = self.classString + """\n
 def isRegestrated(self, login, passwd):
  passwd1 = str(passwd).lower()
  cursor = self.mySqlConnector.cursor()
  Question="SELECT * FROM `User` WHERE `login`=%s AND `password`=%s"
  cursor.execute(Question, tuple((login, passwd1)))					
  return cursor.fetchall()"""

    def _ParamList(self, wskaz="`"):
        return ",".join("`" + x + wskaz for x in self.TableColumn)
    def _ParamListNoKey(self, wskaz="`"):
        return ",".join("`" + x + wskaz for x in self.TableColumn[1:])
    def _ParamHideList(self):
        return ",".join("%s" for x in self.TableColumn[1:])
    def _optionListNoKey(self):
        return ", ".join(self.TableColumn[1:])
    def _optionKey(self):
        return self.TableColumn[0]
    def _CreateInit(self):
        string = """\n
 mySqlConnector = mysql.connector.connect(user="root", password="", host="127.0.0.1", database="pytest")\n
 def __init__(self):
  self.ValueList = list()
  self.tableName = ""
  self.ParameterList = []
  self._select()
    """
        return string

    def _createSql(self):
        string = ""
        
        for key in self._dictionarySql:
            sting = (("\n\tdef _{}(self, list):\n\t\tif isinstance(list, tuple):\n".format(key)) if (key != "select") else ("\n\tdef _{}(self):\n".format(key)))
            sting = sting + '\t\t\tcursor = self.mySqlConnector.cursor()\n\t\t\tQuestion="{}"\n'.format(self._dictionarySql[key][0])
            sting = sting + (("\t\t\tcursor.execute(Question, list)\n") if (key != "select") else ("\t\t\tcursor.execute(Question)\n"))
            sting = sting + (("\t\t\tself.mySqlConnector.commit()\n\t\t\tcursor.close()\n\t\t\tself._select()\n") if (key != "select") else\
                ("\t\t\tself.ValueList = cursor.fetchall()\n\t\t\tcursor.close()\n\t\t\treturn self.ValueList"))
            string = string + sting
        return string

    def _createAction(self):
        string = "\n"
        for key in self._dictionaryAction:
            sting = "\n\tdef {}({}):\n".format(key, self._dictionaryAction[key][0])
            sting = sting + "\t\treturn {}\n".format(self._dictionaryAction[key][1])
            string = string + sting
        return string

    def _createIterator(self):
        return """
 def __iter__(self):
  self.index_of_element = -1
  return self

 def __next__(self):
  self.index_of_element += 1
  if(len(self.ValueList)-1 < self.index_of_element):
   raise StopIteration
  else:
   return [self.ValueList[self.index_of_element], self.index_of_element]
"""

    def Composer(self):
        self.classString = self.classString + self._CreateInit()
        self.classString = self.classString + self._createSql()
        self.classString = self.classString + self._createAction()
        self.classString = self.classString + self._createIterator()
        strr = str(self.classString).replace('\t',' ')
        return strr



class ClassGenerator:
    ''' class to construct Controller to DB with typical set'''
    mySqlConnector = mysql.connector.connect(user="root", password="", host="127.0.0.1", database="pytest")

    def __init__(self):
        self.__set_meta_data_to_db()
        self.__createTableClass()

    def __set_meta_data_to_db(self):
        cursor = self.mySqlConnector.cursor()
        query = ("SHOW TABLES")
        cursor.execute(query)
        DATABASE_TABLE = cursor.fetchall()
        self.dictionary = {}
        print(DATABASE_TABLE)
        for name in DATABASE_TABLE:
            query = ("DESCRIBE {}".format(name[0]))
            cursor.execute(query)
            TABLE_META_LIST = cursor.fetchall()
            self.dictionary.update(zip(name, [[x[0] for x in TABLE_META_LIST]]))
        print(self.dictionary)
        cursor.close()


    def __createTableClass(self):
        # print(Construct(self.dictionary[0], self.dictionary[self.dictionary[0]]).Composer())
        for table in self.dictionary:
            tempo = Construct(table, self.dictionary[table])
            some = tempo.Composer()
            myMod = compile(some, '', 'exec')
            exec(myMod, globals())
            setattr(self, table, globals()[table])


