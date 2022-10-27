create table customers (id serial not null, name varchar(250) not null, age_customer integer, primary key(id))

--create table billboard
create table public."Billboard" (
	"date" date null,
	"rank" int4 null,
	song varchar(300) null,
	artist varchar(300) null,
	"last-week" float8 null,
	"peak-rank" int4 null,
	"weeks-on-board" int4 null
);

select * from public."Billboard" b limit 100

select distinct artist, song from public."Billboard"
order by artist, song

-- COMPLETE QUERY WITHOUT CTE
select distinct b1.artist,
	b1.song
from public."Billboard" b1
left join (
	select artist, count(*) as artist_qtd
	from public."Billboard" b2
	group by b2.artist
	order by b2.artist
) as b2 on (b1.artist = b2.artist)
left join (
	select b1.song, count(*) song_qtd
	from public."Billboard" b1
	group by b1.song
	order by b1.song
) as b3 on (b1.song = b3.song)
order by b1.artist, b1.song

------------------------------------------------------------
-- BUILDING CTE
with cte_artist as (
	select artist, count(*) as artist_qtd
	from public."Billboard" b2
	group by b2.artist
	order by b2.artist
),
cte_song as (
	select b1.song, count(*) song_qtd
	from public."Billboard" b1
	group by b1.song
	order by b1.song
)

select distinct b1.artist,
	b1.song
from public."Billboard" b1
left join cte_artist as b2 on (b1.artist = b2.artist)
left join cte_song as b3 on (b1.song = b3.song)
order by b1.artist, b1.song
-- BUILDING WINDOW FUNCTION
with cte_billboard as (
	select b1.artist, b1.song
	from public."Billboard" b1
	order by b1.artist, b1.song
)
select *,
row_number() over(order by artist, song) as "row_number",
row_number() over(partition by artist order by artist , song) as "row_number_artist"
from cte_billboard
-- getting the row number of the first time a artist shows up
with cte_billboard as (
	select b1.artist, b1.song,
		row_number() over(order by artist, song) as "row_number",
	row_number() over(partition by artist order by artist , song) as "row_number_artist"
	from public."Billboard" b1
	order by b1.artist, b1.song
)
select *
from cte_billboard
where "row_number_artist" = 1;
-- Considering rank
with cte_billboard as (
	select b1.artist, b1.song
	from public."Billboard" b1
	order by b1.artist, b1.song
)
select *,
row_number() over(order by artist, song) as "row_number",
	row_number() over(partition by artist order by artist , song) as "row_number_artist",
	rank() over(partition by artist order by artist, song) as "rank"
from cte_billboard
-- Getting the first time (and table row number) that an artist appeared in the Billboard AND creating a table of results
create table tb_web_site as (
 with cte_dedup_artist as (
 	select t1."date",
 	t1."rank",
 	t1.artist,
 	row_number() over(partition by artist order by artist, "date") as dedup
 	from public."Billboard" t1
 	order by t1.artist, t1."date"
 )
 select t1."date",
 	t1."rank",
 	t1.artist
from cte_dedup_artist as t1
where t1.dedup = 1
)

select * from tb_web_site
-- view
create view view_web_site as (
 with cte_dedup_artist as (
 	select t1."date",
 	t1."rank",
 	t1.artist,
 	row_number() over(partition by artist order by artist, "date") as dedup
 	from public."Billboard" t1
 	order by t1.artist, t1."date"
 )
 select t1."date",
 	t1."rank",
 	t1.artist
from cte_dedup_artist as t1
where t1.dedup = 1
)

select * from view_web_site
