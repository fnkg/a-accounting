select to_char(date, 'YYYYMMDD')             as date,
       0                                     as inn,
       true                                  as onlyinvoice,
       'Медицинские услуги физическим лицам' as name,
       sum(patient_pay)                      as price,
       1                                     as quantity,
       sum(patient_pay)                      as sum,

       (case

          when organization_abbreviation = 'RG' then '80bc7e6d-3b3e-11ee-a22a-00155d59dd05'
        end)                                 as store_uuid,
       (case
          when organization_abbreviation = 'RG' then '4557b547-348d-11ef-a230-00155d59dd05'
        end)
                                             as company_uuid
  from insurers_revenue
  where date >= '2025-02-01' and
        date < '2025-03-01' and
        organization_abbreviation = 'RG'
  group by date, store_uuid, company_uuid
  order by date