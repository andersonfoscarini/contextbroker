__author__ = 'anderson'

import xml.etree.ElementTree as ET
import MySQLdb
import sys


def context_update(xml_string):

    root = ET.fromstring(xml_string)

    try:
        con = MySQLdb.connect(host='localhost', user='root', passwd='showtime', db='broker')
        for ctxEl in root.find('ctxEls').findall('ctxEl'):
            try:
                nameProv = ctxEl.find('contextProvider').get('id')
                version = ctxEl.find('contextProvider').get('v')
                entityType = ctxEl.find('entity').get('type')
                entityId = ctxEl.find('entity').get('id')
                scope = ctxEl.find('scope').text
                timestamp = ctxEl.find('timestamp').text
                expires = ctxEl.find('expires').text
                dataPart = []
                for data in ctxEl.find('dataPart').findall('par'):
                    namePar = data.get('n')
                    valuePar = data.text
                    dataPart.append(namePar+";"+valuePar)
                print nameProv, version, entityType, entityId, scope, timestamp, expires, dataPart
            except: # catch *all* exceptions
                e = sys.exc_info()[0]
                error_message = "<p>Erro no Update: %s</p>" % e
                return error_message
        return "Sucesso"
    except MySQLdb.Error, e:
        error_message = "<p>Erro ao conectar a base de Dados [%d]: %s</p>" % (e.args[0], e.args[1])
        return error_message