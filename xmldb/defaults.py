# -*- coding: utf-8 -*-

from sqlalchemy import MetaData, Table, Column, Integer, String, \
                       UniqueConstraint, ForeignKey

DEFAULT_PREFIX = 'default_'
RESOURCE_TABLE = 'data'
INDEX_TABLE = 'index'
INDEX_DEF_TABLE = 'index_def'
#METADATA_TABLE = 'meta'
#METADATA_INDEX_TABLE = 'meta_idx'
URI_TABLE = 'uri'

# xmldbms tables:
metadata = MetaData()
resource_tab = Table(DEFAULT_PREFIX + RESOURCE_TABLE, metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('data', String),
)

uri_tab = Table(DEFAULT_PREFIX + URI_TABLE, metadata,
    Column('uri', String, primary_key = True),
    Column('res_id', Integer, ForeignKey(DEFAULT_PREFIX + RESOURCE_TABLE +
                                         '.id')),
    Column('res_type', String),
)

# xmlindexcatalog tables:
index_def_tab = Table(DEFAULT_PREFIX + INDEX_DEF_TABLE, metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('key_path', String),
    Column('value_path', String),
    Column('data_type', String(20)),
    UniqueConstraint('key_path', 'value_path')
)

index_tab = Table(DEFAULT_PREFIX + INDEX_TABLE, metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('index_id', Integer, ForeignKey(DEFAULT_PREFIX + INDEX_DEF_TABLE +
                                           '.id')),
    Column('key', String),
    Column('value', String),
)

#QUERY_STR_MAP={'res_tab':DEFAULT_PREFIX + RESOURCE_TABLE,
#               'uri_tab':DEFAULT_PREFIX + URI_TABLE,
#               'idx_def_tab':DEFAULT_PREFIX + INDEX_DEF_TABLE
#               }
#
##ADD_RESOURCE_QUERY="""INSERT INTO %s_%s (id,xml_data) values (%s,%s)"""
#DELETE_RESOURCE_QUERY="""DELETE FROM %(res_tab)s WHERE (id = '%(res_id)s')"""
#REGISTER_URI_QUERY="""INSERT INTO %s_%s (res_id,uri,res_type) values (%s,%s,%s)"""
#REMOVE_URI_QUERY="""DELETE FROM %(uri_tab)s WHERE (uri='%(uri)s')"""
#ADD_INDEX_QUERY="""INSERT INTO %(prefix)s_%(table)s (id,key_path,value_path,data_type) 
#                values (%(id)s,%(key_path)s,%(value_path)s,%(data_type)s)"""               
#DELETE_INDEX_BY_KEY_QUERY="""DELETE FROM %(prefix)s_%(table)s WHERE 
#                (value_path=%(value_path)s AND key_path=%(key_path)s)"""
#DELETE_INDEX_BY_ID_QUERY="DELETE FROM %(prefix)s_%(table)s WHERE (id=%(id)s)"
#GET_INDEX_BY_ID_QUERY="""SELECT id,key_path, value_path,data_type FROM %(prefix)s_%(table)s
#                      WHERE (id=%(id)s)"""
#GET_INDEX_BY_KEY_QUERY="SELECT id,key_path,value_path, data_type FROM %(prefix)s_%(table)s " + \
#                "WHERE (key_path=%(key_path)s AND value_path=%(value_path)s)"
#ADD_INDEX_DATA_QUERY="INSERT INTO %(prefix)s_%(table)s (id,index_id,key,value) " + \
#                "values (%(id)s,%(index_id)s,%(key)s,%(value)s)"
#REMOVE_INDEX_DATA_BY_ID_QUERY="DELETE FROM %(prefix)s_%(table)s " + \
#                              "WHERE (index_id=%(index_id)s)"
#REMOVE_INDEX_DATA_BY_KEY_QUERY="DELETE FROM %(prefix)s_%(table)s " + \
#                "WHERE index_id IN (SELECT id FROM default_index_def " + \
#                "WHERE (key_path=%(key_path)s AND value_path=%(value_path)s))"
#GET_INDEXES_QUERY="SELECT * FROM %(idx_def_tab)s"
#WHERE_TYPE="data_type=%(data_type)s"
#WHERE_KEY_PATH="key_path=%(key_path)s"
#WHERE_VALUE_PATH="value_path=%(value_path)s"
## XXX: nextval is PostgreSQL only!!!!!
#GET_NEXT_ID_QUERY="SELECT nextval('%s_%s_id_seq')"
#GET_ID_BY_URI_QUERY="SELECT res_id FROM %(uri_tab)s WHERE (uri='%(uri)s')"
#GET_RESOURCE_BY_URI_QUERY="""SELECT xml_data FROM %(res_tab)s,%(uri_tab)s
#    WHERE(%(res_tab)s.id=%(uri_tab)s.res_id
#    AND %(uri_tab)s.uri='%(uri)s')"""
#GET_URIS="SELECT uri FROM %(uri_tab)s"
#GET_URIS_BY_TYPE="SELECT uri FROM %(uri_tab)s WHERE (res_type='%(res_type)s')"

