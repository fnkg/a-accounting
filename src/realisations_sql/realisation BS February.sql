select to_char(date, 'YYYYMMDD')             as date,
       0                                     as inn,
       true                                  as onlyinvoice,
       'Медицинские услуги физическим лицам' as name,
       sum(patient_pay)                      as price,
       1                                     as quantity,
       sum(patient_pay)                      as sum,

       (case

          when organization_abbreviation = 'BS' then '28cd7fa6-1c65-11ef-a230-00155d59dd05'
        end)                                 as store_uuid,
       (case
          when organization_abbreviation = 'BS' then 'fe5547ce-3d84-11df-96f8-000c6ea69372'
        end)
                                             as company_uuid
  from insurers_revenue
  where date >= '2025-02-01' and
        date < '2025-03-01' and
        organization_abbreviation = 'BS'
  group by date, store_uuid, company_uuid
  order by date