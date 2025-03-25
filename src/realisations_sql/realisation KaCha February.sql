select to_char(date, 'YYYYMMDD')             as date,
       0                                     as inn,
       true                                  as onlyinvoice,
       'Медицинские услуги физическим лицам' as name,
       sum(patient_pay)                      as price,
       1                                     as quantity,
       sum(patient_pay)                      as sum,

       (case
          when organization_abbreviation = 'KN' then '823cd454-cab4-11eb-a20a-00155dc42e00'
        end)                                 as store_uuid,
       (case
          when organization_abbreviation = 'KN' then '7dbfb2a3-6721-11ed-a221-00155d59dd05'
        end)
                                             as company_uuid
  from insurers_revenue
  where date >= '2025-02-01' and
        date < '2025-03-01' and
        organization_abbreviation = 'KN'
  group by date, store_uuid, company_uuid
  order by date