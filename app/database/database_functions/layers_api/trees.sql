CREATE OR REPLACE FUNCTION trees()
RETURNS TABLE (natural text, geom geometry) AS
$$
	SELECT way AS geom, "natural" 
    FROM planet_osm_point 
    WHERE "natural" IN ('tree','shrub');
$$
LANGUAGE sql;

COMMENT ON FUNCTION trees() 
IS '**FOR-API-FUNCTION** RETURNS col_names[natural,geom] **FOR-API-FUNCTION**';

