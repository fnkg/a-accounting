select to_char(date, 'YYYYMMDD')             as date,
       0                                     as inn,
       true                                  as onlyinvoice,
       'Медицинские услуги физическим лицам' as name,
       sum(patient_pay)                      as price,
       1                                     as quantity,
       sum(patient_pay)                      as sum,

       (case

          when organization_abbreviation = 'UN' then 'f966000c-3c48-11dd-96d9-000c6e46fcad'
        end)                                 as store_uuid,
       (case
          when organization_abbreviation = 'UN' then 'c84cdf1b-6720-11ed-a221-00155d59dd05'
        end)
                                             as company_uuid
  from insurers_revenue
  where date >= '2025-04-01' and
        date < '2025-05-01' and
        organization_abbreviation = 'UN'
  group by date, store_uuid, company_uuid
  order by date