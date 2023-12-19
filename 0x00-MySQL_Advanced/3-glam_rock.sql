-- List Glam rock bands ranked by longevity
SELECT
    band_name,
    IFNULL(SUBSTRING_INDEX(SUBSTRING_INDEX(lifespan, ' - ', -1), ' ', 1), 2022 - FORMED) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan
DESC;
