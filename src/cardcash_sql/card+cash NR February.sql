select id,
       to_char(date, 'YYYYMMDD') as date,
       float4(amount) / 100 as sum,
case
    when t1.type = 'merchant-acquiring' then 'card'
    when t1.type = 'raiffeisen_terminal' then 'card'
    when t1.type = 'cash' then 'cash'
    end as type,
case
    when o.name = 'Клиника в RigaLand' then '80bc7e6d-3b3e-11ee-a22a-00155d59dd05' end as store_uuid,
'4557b547-348d-11ef-a230-00155d59dd05' as company_uuid

from

(select fp.payment_id as id,
        fp.method::json->>'type' as type,
        fp.amount as amount,
        fp.organization_id as org_id,
        fp.author_id as user_id,
        fp.created_at as date,
        fp.status as status,
        fp.operation as operation
 from finance.payment fp) as t1

join organization o on o.organization_id = t1.org_id
join users u on u.user_id = t1.user_id

where
date >= '2025-02-01' and date < '2025-03-01' and
t1.status = 'completed' and
t1.operation in ('payment', 'account_replenishment') and
o.name in ('Клиника в RigaLand') and
t1.type not in ('personal-account', 'internet-acquiring', 'raiffeisen_sbp_link', 'manual_without_receipt', 'raiffeisen_qr_plate', 'arca_link')



union



select id,
       to_char(date, 'YYYYMMDD') as date,
       float4(-amount) / 100 as sum,
case
    when t1.type = 'merchant-acquiring' then 'card'
    when t1.type = 'raiffeisen_terminal' then 'card'
    when t1.type = 'cash' then 'cash'
    end as type,
case
    when o.name = 'Клиника в RigaLand' then '80bc7e6d-3b3e-11ee-a22a-00155d59dd05' end as store_uuid,
'4557b547-348d-11ef-a230-00155d59dd05' as company_uuid

from

(select fp.payment_id as id,
        fp.method::json->>'type' as type,
        fp.amount as amount,
        fp.organization_id as org_id,
        fp.author_id as user_id,
        fp.created_at as date,
        fp.status as status,
        fp.operation as operation
 from finance.payment fp) as t1

join organization o on o.organization_id = t1.org_id
join users u on u.user_id = t1.user_id

where
date >= '2025-02-01' and date < '2025-03-01' and
t1.status = 'completed' and
t1.operation in ('refund') and
o.name in ('Клиника в RigaLand') and
t1.type not in ('personal-account', 'internet-acquiring', 'raiffeisen_sbp_link', 'manual_without_receipt', 'raiffeisen_qr_plate', 'arca_link')

order by date asc