# How to read a query plan from Postgres EXPLAIN
*Dec 31, 2020*

Got a web app responding too slowly because of a database query?
The query plan is what you'd want to look at.
Let's look at the execution plan that Postgres shows you when you
use the EXPLAIN statement and see how to interpret that.

The [Postgres documentation on using EXPLAIN](https://www.postgresql.org/docs/9.4/using-explain.html)
is excellent, but I thought writing a concise version will serve as a note to my future self.
To start off, let's run with a simple schema of three tables: (a) Users,
(b) Articles, and (c) Orders.

```
users:
 id |      email
----+------------------
  1 | jon@example.com
  2 | Jane@example.com
```

```
articles:
 id |    name
----+-------------
  1 | Playstation
  2 | Xbox
```

```
orders:
 id | user_id | article_id | qty
----+---------+------------+-----
  1 |       1 |          1 |   2
  2 |       1 |          2 |   1
  3 |       2 |          1 |   4
  4 |       2 |          2 |   3
```

Suppose we want to query the `users` table by the email address, the plan that
postgres generates is:
```
EXPLAIN SELECT * FROM users WHERE email='jon@example.com';
---------------------------------------------------------------------------------
 Index Scan using users_email_index on users  (cost=0.15..8.17 rows=1 width=222)
   Index Cond: ((email)::text = 'jon@example.com'::text)
```
Since we have an index on the email column, postgres has decided to use that
to search the users table. If we didn't have that index, it would do a sequential
scan over the entire table:
```
EXPLAIN SELECT * FROM users WHERE email='jon@example.com';
----------------------------------------------------------
 Seq Scan on users  (cost=0.00..14.00 rows=2 width=222)
   Filter: ((email)::text = 'jon@example.com'::text)
```


To get all the orders of a user, the query plan is:
```
 EXPLAIN SELECT *
    FROM orders
    INNER JOIN users
        ON orders.user_id=users.id
    WHERE users.email='jon@example.com';
------------------------------------------------------------------------------------------
 Nested Loop  (cost=0.30..40.57 rows=6 width=238)
   ->  Index Scan using users_email_index on users  (cost=0.15..8.17 rows=1 width=222)
         Index Cond: ((email)::text = 'jon@example.com'::text)
   ->  Index Scan using orders_userid_index on orders  (cost=0.15..32.31 rows=9 width=16)
         Index Cond: (user_id = users.id)
```
What's going on here? First, postgres is using the index on the email column
to search the users table for users for email jon@example.com.
For each matching row (we expect a single matching row in this example),
an index scan is performed over the orders table get all orders for that user id.
Translated to pseudocode:
```
for user in users.filter(email='jon@example.com'): # uses the email index
    for order in orders.filter(user_id=user.id): # uses the userid index
        yield (user, order)
```

Now, let's try joining all the three tables to get the full details of all the orders of a user:

```
EXPLAIN SELECT *
    FROM orders
    INNER JOIN users
        ON orders.user_id=users.id
    INNER JOIN articles
        ON orders.article_id=articles.id
    WHERE users.email='jon@example.com';
------------------------------------------------------------------------------------------------
 Nested Loop  (cost=0.45..41.71 rows=6 width=460)
   ->  Nested Loop  (cost=0.30..40.57 rows=6 width=238)
         ->  Index Scan using users_email_index on users  (cost=0.15..8.17 rows=1 width=222)
               Index Cond: ((email)::text = 'jon@example.com'::text)
         ->  Index Scan using orders_userid_index on orders  (cost=0.15..32.31 rows=9 width=16)
               Index Cond: (user_id = users.id)
   ->  Index Scan using articles_pkey on articles  (cost=0.15..0.19 rows=1 width=222)
         Index Cond: (id = orders.article_id)
```
This is similar to joining the two tables, but we have another loop to join the third table.
In pseudocode, this is what's going on:
```
for user in users.filter(email='jon@example.com'): # uses the email index
    for order in orders.filter(user_id=user.id): # uses the userid index
        for article in articles.filter(id=order.article_id): # uses article_id primary key
            yield (user, order, article)
```

Instead of an index scan, you might come across a bitmap heap scan like this:
```
 EXPLAIN SELECT *
    FROM orders
    INNER JOIN users
        ON orders.user_id=users.id
    WHERE users.email='jon@example.com';
----------------------------------------------------------------------------------------
 Nested Loop  (cost=4.37..23.02 rows=6 width=238)
   ->  Index Scan using users_email_index on users  (cost=0.15..8.17 rows=1 width=222)
         Index Cond: ((email)::text = 'jon@example.com'::text)
   ->  Bitmap Heap Scan on orders  (cost=4.22..14.76 rows=9 width=16)
         Recheck Cond: (user_id = users.id)
         ->  Bitmap Index Scan on orders_userid_index  (cost=0.00..4.22 rows=9 width=0)
               Index Cond: (user_id = users.id)
```
In a plain index scan, postgres fetches a row pointer from the index and immediately
fetches that row from the table. But with a bitmap index scan, all the tuple pointers
that match the filtering condition are gathered and an in-memory bitmap data structure
is created. From this, the actual tuples in the table are visited in physical location order.
This improves locality of accesses to the table and matters a lot for spinning rust HDDs but
can also help with SSDs too. What's that "recheck condition"? If the bitmap gets large,
postgres converts it to a lossy bitmap that stores only physical pages instead of individual
tuples. So when the tuples are read from the physical pages, postgres has to recheck which
tuples in that page match the filtering condition. Bitmap scans also do well when there
are multiple filtering conditions using ORs and ANDs since the bitmap data structure supports
these operations efficiently.

Postgres collects statistics about the content of the tables. If it expects very few rows
to match the filtering condition, an index scan is preferred. If many rows are expected to
satisfy the filtering condition, a bitmap scan is preferred. If a substantial portion of the table
is likely to be fetched, the sequential scan wins. One of the authors of Postgres, Tom Lane, has
an email thread on [this topic](https://www.postgresql.org/message-id/12553.1135634231@sss.pgh.pa.us).

The [three types of joins](https://stackoverflow.com/a/49024533) you're likely to come across in a
query plan are: (a) Nested loop join, (b) Hash join, and (c) Merge join. For example, here is a hash join:
```
 EXPLAIN SELECT *
    FROM orders
    INNER JOIN users
        ON orders.user_id=users.id
    WHERE users.email='jon@example.com';
--------------------------------------------------------------------
 Hash Join  (cost=14.03..47.45 rows=12 width=238)
   Hash Cond: (orders.user_id = users.id)
   ->  Seq Scan on orders  (cost=0.00..28.50 rows=1850 width=16)
   ->  Hash  (cost=14.00..14.00 rows=2 width=222)
         ->  Seq Scan on users  (cost=0.00..14.00 rows=2 width=222)
               Filter: ((email)::text = 'jon@example.com'::text)
```
The hash join can be used only when the join condition is the equality operator.
Postgres constructs an in-memory hash table of the filtered users and scans the
orders table and retains those tuples which have a matching user id in the
constructed hash table.

The nested loop is the preferred option when at least one side of the join has very
few matching tuples. Hash join is used when both sides of the join have a large number of tuples.
Merge join is preferred when both sides of the join are large but can be sorted on the joining
condition using an index.

All the SQL statements used in this article are [here](explain.sql).