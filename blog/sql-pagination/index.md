# Pagination in SQL
*Aug 27, 2017*

Here are two ways to paginate the results of a SQL query that work across all
the popular SQL databases.

## Truncate the results
Silly though it sounds, this might be a reasonable strategy. Suppose you want
to show 15 results per page. Then, show up to 20 pages, and stop there. This works
well when it's unlikely that anyone would want to see past the first few pages.
Incidentally, Google does something like this for web search results.

```
SELECT * FROM users ORDER BY creation_date LIMIT 15 OFFSET 45;
```

This query is not efficient for large offsets because rows up to the offset have
to be read and discarded. But that's OK since the offset is limited to a few
hundred rows at most. It's a net win if only the first few pages are read most
of the time.

## Keep track of the first and last result in a page
This is based on the idea that random access is not really needed and that it's often
necessary to only access the next page and the previous page from any given page.
When you're on the fourth page, accessing a random page, say page 3124, might
be inefficient. But, accessing the third and fifth pages are efficient if the
right indexes have been setup. This is accomplished by keeping track of the first
and last values of the column on which the results are ordered.

```
SELECT * FROM users WHERE creation_date > ? ORDER BY creation_date LIMIT 15;
```

When the next page is requested, the query is executed with the `creation_date`
of the last user in the current page. For the previous page, the `creation_date`
of the first user in the current page is used:

```
SELECT * FROM users WHERE creation_date < ? ORDER BY creation_date DESC LIMIT 15;
```

If the column by which the results are sorted is not unique, add additional columns or
the primary key to `ORDER BY` and keep track of the first and last values of those columns as well.

Another example of using this method for pagination is in the [SQLite wiki](http://www.sqlite.org/cvstrac/wiki?p=ScrollingCursor).
