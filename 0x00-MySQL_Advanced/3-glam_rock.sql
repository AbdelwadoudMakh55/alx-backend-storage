-- Computing lifespan of metal bands
SELECT band_name, IF(split is NOT NULL, split, 2022) - formed AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
