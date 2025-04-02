select id,
       to_char(date, 'YYYYMMDD')                                                as date,
       float4(amount * case when operation = 'refund' then -1 else 1 end) / 100 as sum,
       case
           when t1.type = 'merchant-acquiring' then 'card'
           when t1.type = 'raiffeisen_terminal' then 'card'
           when t1.type = 'cash' then 'cash'
           end                                                                  as type,
       case
           when le.abbreviation = 'ЧНР' then '80bc7e6d-3b3e-11ee-a22a-00155d59dd05'
           end                                                                  as store_uuid,
       case
           when le.abbreviation = 'ЧНР' then '4557b547-348d-11ef-a230-00155d59dd05'
           end                                                                  as company_uuid

from (select fp.payment_id              as id,
             fp.method::json ->> 'type' as type,
             fp.amount                  as amount,
             fpp.legal_entity_id        as le_id,
             -- fp.author_id               as user_id,
             fp.created_at              as date,
             fp.status                  as status,
             fp.operation               as operation

      from finance.payment fp

               -- корректно брать id Юрлица из метода оплаты
               left join finance.payment_method fpp on fpp.payment_method_id = fp.payment_method_id

              -- соединяем слева иначе по умолчанию будет Inner join
               left join rendered_service_view rsv on rsv.rendered_service_id = any (fp.rendered_service_ids)
               left join service s on rsv.value::json ->> 'serviceId' = text(s.service_id)
      where s.category != '1CProduct'

         -- учет чтобы попали и пополнения л.с.
         or rsv.rendered_service_id is null) as t1

         -- берем не клинику а Юрлицо
         left join legal_entity le on le.legal_entity_id = t1.le_id

     --  join users        u on u.user_id = t1.user_id

where date >= '2025-03-01'
  and date < '2025-04-01'
  and t1.status in ('completed',

    -- бывают и такие успешные оплаты
                    'receipt_failed', 'waiting_for_receipt')

  and t1.operation in ('payment', 'account_replenishment', 'refund')

  -- ориентируемся по названию Юрлица
  and le.abbreviation in ('ЧНР')

  -- чтобы сразу ограничить только нужные методы
  and t1.type in ('merchant-acquiring', 'raiffeisen_terminal', 'cash')

order by date