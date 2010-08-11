##################################################################
#
# Ratemap
# map-rating plugin for B3 (www.bigbrotherbot.com)
# (c) 2010 Brian Markland (ttlogic@xlr8or.com)
#
# This program is free software and licensed under the terms of
# the GNU General Public License (GPL), version 2.
#
# Ratings are stored in two tables and maplist is refreshed
# on map change so a list of all maps used is available
#
# More functions to come soon, including
#       topmap, top 10, worstmap among others
#
##################################################################
# CHANGELOG
# 2010/08/10 - Initial Release
# 2010/08/11 - Help descritions corrected
# Ratemap plugin

__version__ = '1.0.0'
__author__  = 'Rhidain_Bytes'
__python__ = '2.6'

import b3
import b3.events
from string import capitalize

class RatemapPlugin(b3.plugin.Plugin):
    _adminPlugin = None
    mapreportfile = None

    _MAP_SELECT_QUERY = "SELECT id, mapname from ratemap WHERE mapname='%s'"
    _MAP_SELECTLIKE_QUERY = "SELECT id, mapname from ratemap WHERE mapname LIKE '%s'"
    _MAP_ADD_QUERY = "INSERT INTO ratemap (id, mapname) VALUES (NULL, '%s')"
    _RATE_QUERY = "INSERT INTO rating (id, map, rating) VALUES (NULL, '%s', '%s')"
    _GETRATE_QUERY = "SELECT rating from rating WHERE map='%s'"
    _RESETRATE_QUERY = "DELETE FROM rating WHERE map='%s'"
    _RESETALLRATE_QUERY = "TRUNCATE TABLE rating"
    _MAP_SELECTALL_QUERY = "SELECT * from ratemap"
    _REPORT_QUERY = "SELECT ratemap.mapname, AVG(rating.rating) AS ratings, MIN(rating.rating) AS mins, MAX(rating.rating) AS maxs FROM rating, ratemap WHERE rating.map = ratemap.id GROUP BY ratemap.mapname ORDER BY ratings DESC"
    _MAP_REPORT_QUERY = "SELECT ratemap.mapname, AVG(rating.rating) AS ratings, MIN(rating.rating) AS mins, MAX(rating.rating) AS maxs FROM rating, ratemap WHERE rating.map = ratemap.id AND ratemap.mapname = '%s' GROUP BY ratemap.mapname ORDER BY ratings DESC"
    def startup(self):
        """\
        Initialize plugin settings
        """
        self.registerEvent(b3.events.EVT_GAME_EXIT)

        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return False
    
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = self.getCmd(cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)
        try:
            self.console.storage.query(self._MAP_SELECT_QUERY % 'test')
        except:
            self.debug('Error loading SQL, did you install the table?')
        
        self.mapreportfile = self.config.get('settings', 'mapreportfile')
        
        self.debug('Saving report to %s' % self.mapreportfile)
        
        self.debug('Started')


    def getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func

        return None
    
    def handle(self, event):
        if event.type == b3.events.EVT_GAME_EXIT:
            checkratemap(mapnow())
        self.debug('ran event')

    def cmd_ratemap(self, data, client=None, cmd=None):
        """\
        <1 - 10> - Rate the current map
        """
        m = self._adminPlugin.parseUserCmd(data)
        if not m:
            client.message('^7You must enter a number 1 to 10')
            return False
        if m[0] <= 0 and m[0] > 10:
            client.message('^7You must enter a number 1 to 10')
            return False
        map = self.mapnow()
        # made variable in case map changes mid command
        self.checkratemap(map)
        mule = self.console.storage.query(self._MAP_SELECT_QUERY % map)
        saddle = mule.getRow()
        rider = self.console.storage.query(self._RATE_QUERY % (saddle['id'], m[0]))
        rider.close()
        mule.close()
        client.message('Thank you for rating %s' % map)
        return True
        
    def cmd_maprating(self, data, client=None, cmd=None): #<mapname optional>
        """\
        <mapname> Enter mapname or leave blank for current map rating
        """
        m = self._adminPlugin.parseUserCmd(data)
        if not m:
            map = self.mapnow()
        else:
            map = m[0]
        mapi = self.findmap(map)
        if mapi:
            report = self.getreport(map)
            cmd.sayLoudOrPM(client, '%s' % report[0])
            return True
        else:
            client('There was a problem finding the map')
            return False
                
    def cmd_resetrating(self, data, client=None, cmd=None):# <mapname or all>
        """\
        <mapname> Enter mapname or leave blank for current map
        """
        m = self._adminPlugin.parseUserCmd(data)
        if not m:
            map = self.mapnow()
        elif m == 'all':
            rider = self.console.storage.query(self._RESETALLRATE_QUERY)
            rider.close()
            client.message('All map ratings have been reset')
            return True
        else:
            map = m[0]
        mapi = findmap(map)
        if mapi:
            cursor = self.console.storage.query(self._RESETRATE_QUERY % mapi)
            client.message('Map %s rating reset')
            return True
    
    def cmd_mapreport(self, data=None, client=None, cmd=None):# <filename>                
        """\
        <filename> Enter filename (limited) or leave blank if set
        """    
        m = self._adminPlugin.parseUserCmd(data)
        if not m and not self.mapreportfile:
            client.message('You must specify a filename here or in config')
            return False
        elif m:
            mapreportfile = m[0]
        else:
            mapreportfile = self.mapreportfile
        report = self.getreport()
        if report:
            self.savereport(mapreportfile, report)
            if client:
                client.message('Report generated')
            return True
        else:
            if client:
                client.message('There was a problem generating the report')
            return False

# Internal functions            
    def mapnow(self):
        map = self.console.getMap()
        map = map.strip().lower()
        if map[:3] == 'mp_': map = map[3:]
        return map

    def checkratemap(self, map):
        mule = self.console.storage.query(self._MAP_SELECT_QUERY % map)
        if mule.rowcount == 0:
            cursor = self.console.storage.query(self._MAP_ADD_QUERY % (map))
            cursor.close()
            self.debug("map %s added to sql" % map)
        mule.close()
        
    def findmap(self, map, client=None, cmd=None):
        cursor = self.console.storage.query(self._MAP_SELECT_QUERY % map)
        if cursor.rowcount==0:
            cursor.close()
            cursor.execute(self._MAP_SELECTLIKE_QUERY % map)
            if cursor.rowcount==0:
                client.message('Unable to find %s' % map)
                return False
            elif cursor.rowcount==1:
                mapi = cursor.getRow()
                cursor.close()
                return mapi['id']
            else:
                while 1:
                    mapi = cursor.getRow()
                    if mapi:
                        l.append(mapi['mapname'])
                        cursor.moveNext()
                    else:
                        break
                client.message('Found %s maps, please select one' % (len(l)))
                client.message('%s' % (join(l)))
                cursor.close()
                return False
        else:
            mapi = cursor.getRow()
            cursor.close()
            return mapi['id']
            
    def getreport(self, map=None, client=None, cmd=None):  
        report = []
        # get all mapnames
        if not map:
            sheep = self.console.storage.query(self._REPORT_QUERY)
        else:
            sheep = self.console.storage.query(self._MAP_REPORT_QUERY % map)
        n = 0
        mapreport = []
        self.debug('sheep.rowcount %s'% sheep.rowcount)
        self.debug('sheep.getRow() %s'% sheep.getRow())
        if sheep.rowcount==0:
            self.debug('There was error reading the database.')
            return False
        else:
            while 1:
                mapi = sheep.getRow()
                # {'mapname': 'harbor', 'ratings': Decimal('10.0000'), 'mins': 10L, 'maxs': 10L}
                if mapi:
                    mapname = mapi['mapname']
                    rating = mapi['ratings']
                    min = mapi['mins']
                    max = mapi['maxs']
                    self.debug('%s rates a %s with low score %s and high score %s' % (mapname, rating, min, max))
                    report.append('%s rates a %s with low score %s and high score %s \n' % (capitalize(mapname), rating, min, max))
                    sheep.moveNext()
                else:
                    sheep.close()
                    break
        return report
        
    def savereport(self, mapreportfile, report):
        f = open(mapreportfile, 'w')
        f.writelines(report)
        f.close()
