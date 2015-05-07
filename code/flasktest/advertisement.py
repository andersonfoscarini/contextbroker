__author__ = 'anderson'

import xml.etree.ElementTree as ET
import MySQLdb
import sys


def register_broker(broker_info):
    root = ET.fromstring(broker_info)
    try:
        con = MySQLdb.connect(host='localhost', user='root', passwd='showtime', db='broker')
        for adv in root.find('ctxAdvs').findall('ctxAdv'):
            try:
                nameProv = adv.find('contextProvider').get('id')
                version = adv.find('contextProvider').get('v')
                urlRoot = adv.find('urlRoot').text
                lat, lon, location = '', '', ''
                if adv.find('providerLocation') is not None:
                    lat = adv.find('providerLocation').find('lat').text
                    lon = adv.find('providerLocation').find('lon').text
                    location = adv.find('providerLocation').find('location').text
                try:
                    c = con.cursor()
                    c.execute("INSERT INTO providers(name, url, version, location, location_desc) VALUES (%s, %s, %s, %s, %s)", (
                                                nameProv, urlRoot, version, lat+";"+lon, location))
                    c.close()
                    con.commit()
                except MySQLdb.Error, e:
                    error_message = "<p>Erro no registro do Provider %s [%d]: %s</p>" % (nameProv, e.args[0], e.args[1])
                    return error_message
                scopes=''
                for scope in adv.find('scopes').findall('scopeDef'):
                    nameScope = scope.get('n')
                    urlPath = scope.find('urlPath').text
                    entityTypes = scope.find('entityTypes').text
                    inputs=[]
                    for inputEl in scope.find('inputDef').findall('inputEl'):
                        name = inputEl.get('name')
                        type = inputEl.get('type')
                        inputs.append(name+";"+type)
                    c = con.cursor()
                    c.execute("SELECT provider_id FROM providers WHERE name = '%s'" % nameProv)
                    providerId = c.fetchone()[0]
                    c.close()
                    try:
                        c = con.cursor()
                        c.execute("INSERT INTO scopes (name, urlPath, entityTypes, inputs, provider_id)"
                                  "          VALUES (%s, %s, %s, %s, %s)", (nameScope, urlPath, entityTypes, str(inputs), providerId))
                        c.close()
                    except MySQLdb.Error, e:
                        con.commit()
                        con.close()
                        error_message = "<p>Erro no registro do Scope %s [%d]: %s</p>" % (nameScope, e.args[0], e.args[1])
                        return error_message
            except: # catch *all* exceptions
                con.commit()
                con.close()
                e = sys.exc_info()[0]
                error_message = "<p>Erro no Advertisement: %s</p>" % e
                return error_message
        con.commit()
        con.close()
        return "Sucesso"
    except MySQLdb.Error, e:
        con.commit()
        con.close()
        error_message = "<p>Erro ao conectar a base de Dados [%d]: %s</p>" % (e.args[0], e.args[1])
        return error_message