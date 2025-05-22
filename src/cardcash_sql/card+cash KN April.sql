select id,
       to_char(date, 'YYYYMMDD')                                                as date,
       float4(amount * case when operation = 'refund' then -1 else 1 end) / 100 as sum,
       case
         when t1.type = 'merchant-acquiring'  then 'card'
         when t1.type = 'raiffeisen_terminal' then 'card'
         when t1.type = 'cash'                then 'cash'
       end                                                                      as type,
       case
         when le.abbreviation = 'Чайка Кунцево' then '823cd454-cab4-11eb-a20a-00155dc42e00'
       end                                                                      as store_uuid,
       case
         when le.abbreviation = 'Чайка Кунцево' then '7dbfb2a3-6721-11ed-a221-00155d59dd05'
       end                                                                      as company_uuid

  from (select fp.payment_id              as id,
               fp.method::json ->> 'type' as type,
               fp.amount                  as amount,
               fpp.legal_entity_id        as le_id,
               fp.created_at              as date,
               fp.status                  as status,
               fp.operation               as operation

          from finance.payment                  fp
               left join finance.payment_method fpp on fpp.payment_method_id = fp.payment_method_id
               left join rendered_service_view  rsv on rsv.rendered_service_id = any (fp.rendered_service_ids)
               left join service                s
                           on rsv.value::json ->> 'serviceId' = text(s.service_id) and s.category != '1CProduct'
       ) as                   t1

       left join legal_entity le on le.legal_entity_id = t1.le_id

  where date >= '2025-04-01'
    and date < '2025-05-01'
    and t1.status in ('completed', 'receipt_failed', 'waiting_for_receipt')
    and t1.operation in ('payment', 'account_replenishment', 'refund')
    and le.abbreviation in ('Чайка Кунцево')
    and t1.type in ('merchant-acquiring', 'raiffeisen_terminal', 'cash')

  group by id, date, sum, t1.type, store_uuid, company_uuid

  order by date
