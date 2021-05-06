# Rounding solution from: https://gis.stackexchange.com/questions/321518/rounding-coordinates-to-5-decimals-in-geopandas
import copy
import re
import geopandas as gpd
from db.db import Database
from shapely.wkt import loads

db = Database()


class Profiles():
    def __init__(self):
        self.batch_size = 1000
        self.output_format = 'GeoJSON'
        self.out_dir = '/opt/data/'
        self.filename = self.out_dir + 'ways_profile_points.geojson'
        self.trim_decimals = True
        self.decimals = 5
        self.simpledec = re.compile(r"\d*\.\d+")
        self.check_drivers
        self.enable_driver=False

    def check_drivers(self):
        from fiona import supported_drivers
        from fiona._env import GDALEnv        

        # Check default Geopandas against FIONA drivers
        if self.output_format not in supported_drivers:
            self.enable_driver=True        
            drv = GDALEnv().drivers()
            if self.output_format not in drv:
                print('GDAL Driver {0} not present or misspelled'.format(self.output_format))
                exit(1)

    @staticmethod
    def ways2sql(ways):
        lsql = '('
        for w in ways:
            lsql = lsql + '{0},'.format(w)
        lsql = lsql[:-1] + ')'
        return lsql

    def mround(self, match):        
        return "{:.{}f}".format(float(match.group()), self.decimals)

    def trim(self, gdf):
        return gdf.geometry.apply(lambda x: loads(re.sub(self.simpledec, self.mround, x.wkt)))

    def get_chunks(self, table='ways'):
        r = db.select(query='SELECT count(*) FROM ways;')
        chunks = range(int(r[0][0] / self.batch_size)+1)
        return chunks

    def get_slope(self, way_list=None):
        if way_list is None:
            gdf_master = None
            batches = self.get_chunks()
            for b in batches:
                sql = """
                    WITH segments AS (
                        SELECT id FROM ways LIMIT {0} OFFSET {1}
                    )                                
                    
                    SELECT seg.return_id as way_id, seg.elevs as elevation, seg.return_geom as geom                         
                    FROM segments s,
                    LATERAL get_slope_profile_precompute(s.id) seg;        
                """.format(self.batch_size, b*self.batch_size)
                gdf = db.select(query=sql, return_type='geodataframe')                
                if gdf_master is None:
                    gdf_master = copy.deepcopy(gdf)
                else:
                    t = gdf_master.append(gdf)
                    gdf_master = copy.deepcopy(t)
            if self.trim_decimals:
                gdf_master.geometry = self.trim(gdf_master)
            return gdf_master
        else:
            ways = self.ways2sql(way_list)
            sql = """
                    WITH segments AS (
                        SELECT id FROM ways WHERE id IN {0}
                    )                                
                    
                    SELECT seg.return_id as way_id, seg.elevs as elevation, seg.return_geom as geom                         
                    FROM segments s,
                    LATERAL get_slope_profile_precompute(s.id) seg;        
                """.format(ways)
            gdf = db.select(query=sql, return_type='geodataframe')
            if self.trim_decimals:
                gdf.geometry = self.trim(gdf)
            return gdf

    def write_file(self, df):
        # Enable not default FIONA drivers
        if self.enable_driver:
            gpd.io.file.fiona.drvsupport.supported_drivers[self.output_format] = 'rw'
        df.to_file(self.filename, driver=self.output_format)


# Test...
# p = Profiles()
# df = p.get_slope(way_list=[31,47,48,49,9,15,20,11,16,17])
# p.output_format='PGDUMP'
# p.check_drivers()
# p.filename='/opt/data/ways_profile_test.sql'
# p.write_file(df)
# p.output_format='GeoJSON'
# p.check_drivers()
# p.filename='/opt/data/ways_profile_test.geojson'
# p.write_file(df)
