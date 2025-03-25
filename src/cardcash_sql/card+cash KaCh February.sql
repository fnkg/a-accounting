select id,
       to_char(date, 'YYYYMMDD')              as date,
       float4(amount) / 100                   as sum,
       case
         when t1.type = 'merchant-acquiring'  then 'card'
         when t1.type = 'raiffeisen_terminal' then 'card'
         when t1.type = 'cash'                then 'cash'
       end                                    as type,
       case
         when o.name = 'Клиника Кунцево Плаза' then '823cd454-cab4-11eb-a20a-00155dc42e00'
       end                                    as store_uuid,
       '7dbfb2a3-6721-11ed-a221-00155d59dd05' as company_uuid
  
  from (select fp.payment_id              as id,
               fp.method::json ->> 'type' as type,
               fp.amount                  as amount,
               fp.organization_id         as org_id,
               fp.author_id               as user_id,
               fp.created_at              as date,
               fp.status                  as status,
               fp.operation               as operation
          from finance.payment            fp
               
               join rendered_service_view rsv on rsv.rendered_service_id = any (fp.rendered_service_ids)
               join service               s on rsv.value::json ->> 'serviceId' = text(s.service_id)
          where s.category != '1CProduct'
       ) as              t1
       
       join organization o on o.organization_id = t1.org_id
       join users        u on u.user_id = t1.user_id
  
  where date >= '2025-02-01' and
        date < '2025-03-01' and
        t1.status = 'completed' and
        t1.operation in ('payment', 'account_replenishment') and
        o.name in ('Клиника Кунцево Плаза') and
        t1.type not in ('personal-account', 'internet-acquiring', 'raiffeisen_sbp_link', 'manual_without_receipt',
                        'raiffeisen_qr_plate', 'arca_link')


union


select id,
       to_char(date, 'YYYYMMDD')              as date,
       float4(-amount) / 100                  as sum,
       case
         when t1.type = 'merchant-acquiring'  then 'card'
         when t1.type = 'raiffeisen_terminal' then 'card'
         when t1.type = 'cash'                then 'cash'
       end                                    as type,
       case
         when o.name = 'Клиника Кунцево Плаза' then '823cd454-cab4-11eb-a20a-00155dc42e00'
       end                                    as store_uuid,
       '7dbfb2a3-6721-11ed-a221-00155d59dd05' as company_uuid
  
  from (select fp.payment_id              as id,
               fp.method::json ->> 'type' as type,
               fp.amount                  as amount,
               fp.organization_id         as org_id,
               fp.author_id               as user_id,
               fp.created_at              as date,
               fp.status                  as status,
               fp.operation               as operation
          from finance.payment            fp
               
               join rendered_service_view rsv on rsv.rendered_service_id = any (fp.rendered_service_ids)
               join service               s on rsv.value::json ->> 'serviceId' = text(s.service_id)
          where s.category != '1CProduct'
       ) as              t1
       
       join organization o on o.organization_id = t1.org_id
       join users        u on u.user_id = t1.user_id
  
  where date >= '2025-02-01' and
        date < '2025-03-01' and
        t1.status = 'completed' and
        t1.operation in ('refund') and
        o.name in ('Клиника Кунцево Плаза') and
        t1.type not in ('personal-account', 'internet-acquiring', 'raiffeisen_sbp_link', 'manual_without_receipt',
                        'raiffeisen_qr_plate', 'arca_link')

order by date asc