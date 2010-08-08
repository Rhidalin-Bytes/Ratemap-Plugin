# Ratemap plugin

# By storing ratings in this two table manner, we have a cumulative list of all maps being created
# a simple b3.event added to this could get a list of all maps both for the report as well as 
# for other functions within B3.
__version__ = '1.0'
__author__  = 'Rhidain_Bytes'

import b3, re
import b3.events

class RatemapPlugin(b3.plugin.Plugin):
    _adminPlugin = None
    mapreportfile = None

    _MAP_SELECT_QUERY = "SELECT id, mapname from ratemap WHERE mapname='%s'"
    _MAP_SELECTLIKE_QUERY = "SELECT id, mapname from ratemap WHERE mapname LIKE '%s'"
    _MAP_ADD_QUERY = "INSERT INTO ratemap (id, mapname) VALUES (NULL, '%s')"
    _RATE_QUERY = "INSERT INTO rating (id, ratemap.id, rating) VALUES (NULL, '%s', '%s')"
    _GETRATE_QUERY = "SELECT rating from rating WHERE ratemap.id='%s'"
    _RESETRATE_QUERY = "DELETE FROM rating WHERE ratemap.id='%s'"
    _RESETALLRATE_QUERY = "TRUNCATE TABLE rating"
    _MAP_SELECTALL_QUERY = "SELECT * from ratemap"
    
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
    
        self.debug('Started')


    def getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func

        return None
    
    def onEvent(self, event):
        if event.type == b3.events.EVT_GAME_EXIT:
            checkratemap(mapnow())

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
        else:
        map = mapnow()
        # made variable in case map changes mid command
        checkratemap(map)
        mule = self.console.storage.query(self._MAP_SELECT_QUERY % map)
        rider = self.console.storage.query(self._RATE_QUERY % (m[0], mule[0]))
        rider.close()
        mule.close()
        client.message('Thank you for rating %s' %s map)
        return True
        
    def cmd_maprating(self, data, client=None, cmd=None): #<mapname optional>
        """\
        <mapname> Enter mapname or leave blank for current map rating
        """
        m = self._adminPlugin.parseUserCmd(data)
        if not m:
            map = mapnow()
        else:
            map = m[0]
        # okay, do we have a matching map?
        mapi = findmap(map)
        if mapi:
            report = getreport(map)
            for n in report
                client.message(n)
            return True
        else:
            return False
                
    def cmd_resetrating(self, data, client=None, cmd=None):# <mapname or all>
        """\
        <mapname> Enter mapname or leave blank for current map rating
        """
        m = self._adminPlugin.parseUserCmd(data)
        if not m:
            map = self.console.getmapname
        elif m = 'all':
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
        <mapname> Enter mapname or leave blank for current map rating
        """    
        m = self._adminPlugin.parseUserCmd(data)
        if not m and not self.mapreportfile:
            client.message('You must specify a filename here or in config)
            return False
        elif self.mapreportfile:
            mapreportfile = self.mapreportfile
        else:
            mapreportfile = m[0]
        generate(report)
        
        write(report) to mapreportfile

# Internal functions            
    def mapnow(self)
        map = self.console.getMap()
        map = map.strip().lower()
        if map[:3] == 'mp_': map = map[3:]
        return map

    def checkratemap(self, map)
        mule = self.console.storage.query(self._MAP_SELECT_QUERY % map)
        if mule.rowcount == 0:
            cursor = self.console.storage.query(self._MAP_ADD_QUERY % (map))
            cursor.close()
            self.debug("map %s added to sql" % map)
        mule.close()
        
    def findmap(self, map, client=None, cmd=None):
        cursor=self.console.storage.query(self._MAP_SELECT_QUERY % map)
        if cursor.rowcount==0:
            cursor.close()
            cursor=self.console.storage.query(self._MAP_SELECTLIKE_QUERY % map)
            if cursor.rowcount==0:
                client.message('Unable to find %s' % map)
                return False
            elif cursor.rowcount==1:
                mapi = cursor[0]
                cursor.close()
                return mapi
            else:
                for line in cursor:
                    l.append(cursor[1])
                    cursor.nextrow()
                client.message('Found %s maps, please select one' %s (len(l)))
                client.message('%s' % (.join(l)))
                cursor.close()
                return False
        else:
            mapi = cursor[0]
            cursor.close()
            return mapi
            
     def getreport(seq, map=None):  
        report = ''
        # get all mapnames
        if not map:
            map = '*'
        mapnames = self.console.storage.query(self._GET_SELECT_QUERY % map)
        for n in mapnames:
            mapi = n[0]
            #index set, now pull ratings to get average
            cursor = self.console.storage.query(self._GETRATE_QUERY % mapi)
            rate = ''
            for c in cursor:
                rate.append(cursor(rating))
            avg = float(sum(rate)) / len(rate)
            lo = min(rate)
            hi = max(rate)
            report.append('%s rates a %s with low score %s and high score %s' % (n[1], avg, lo, hi)
            cursor.close()
        return report