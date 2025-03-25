select to_char(date, 'YYYYMMDD')             as date,
       0                                     as inn,
       true                                  as onlyinvoice,
       'Медицинские услуги физическим лицам' as name,
       sum(patient_pay)                      as price,
       1                                     as quantity,
       sum(patient_pay)                      as sum,

       (case
          when organization_abbreviation in ('MC', 'УЦ', 'DOC') then 'e884414e-345f-11e2-9222-f23cea8074d9'
        end)                                 as store_uuid,
       (case
          when organization_abbreviation in ('MC', 'DOC', 'УЦ')
            then '4d0460ff-a0cb-11e2-9494-91acf06830ea'
        end)
                                             as company_uuid
  from insurers_revenue
  where date >= '2025-02-01' and
        date < '2025-03-01' and
        organization_abbreviation in ('MC', 'DOC', 'УЦ')
  group by date, store_uuid, company_uuid
  order by date