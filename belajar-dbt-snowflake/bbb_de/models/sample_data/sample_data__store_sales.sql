WITH source_store_sales AS (
    SELECT *
    FROM {{ source('sample_data', 'store_sales') }}
	LIMIT 1000
),

final AS (
    SELECT *
    FROM source_store_sales
)

SELECT *
FROM final