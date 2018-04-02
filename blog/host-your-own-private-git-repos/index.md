# Host Your Own Private Git Repos
*Mar 25, 2018*

Hosting git repos on your own server is actually quite easy.
Login to the server, create a new directory, and initialize a bare repo:

```
mkdir foo.git
cd foo.git
git init --bare
```

That's it! Now, from the client, clone this repo with:

```
git clone username@example.com:path/to/foo.git
```

Having a dedicated user for git repos on the server makes it easier share access to the repo.
Create a new user `git` with a login shell restricted to git commands:

```
sudo adduser --shell $(which git-shell) git
```

Now create a repo in the home directory of the `git` user:

```
cd /home/git
sudo -u git mkdir bar.git
cd bar.git
sudo -u git git init --bare
```

As before, clone the new repo from the client using:

```
git clone git@example.com:bar
```

## Backup the repos

This is my script to take daily backups of all the git repos on the server to Amazon S3.

```
#!/bin/bash

set -e

GITDIR=/home/git
TMPDIR=/tmp/gitbackup

renice -n 15 $$

trap "rm -f /tmp/gitbackup/*.git.tar.gz" EXIT

mkdir -p ${TMPDIR}
cd ${TMPDIR}

for proj in ${GITDIR}/*.git; do
    base=$(basename $proj)
    tar -C $GITDIR -zcf ${base}.tar.gz $base
done

export AWS_ACCESS_KEY_ID=xxxxx
export AWS_SECRET_ACCESS_KEY=yyyyy
export AWS_DEFAULT_REGION=us-west-2

aws s3 cp ${TMPDIR}/*.git.tar.gz s3://mygitbucket/
```

If the repos are large, it might be worthwhile checking whether
the hash of the gzipped repo has changed before uploading.
It's also good idea to use `envdir` to manage the access keys rather
than putting them in the backup script.

## Web front-end using cgit and nginx

Sometimes it's useful to view source code and commits on a
web browser. `cgit` is an awesome light-weight webapp for this.
Unlike heavy apps like GitLab, `cgit` needs no database, which
reduces the administrative burden.

Install cgit, nginx, fcgiwrap, and apache-tools (to create a `.htpasswd` file).

```
sudo apt install cgit nginx fcgiwrap apache2-utils
```

Specify the location of the git repos and static assets in the 
`cgit` config at `/etc/cgitrc`.

```
css=/cgit-static/cgit.css
logo=/cgit-static/cgit.png
favicon=/cgit-static/favicon.ico

#source-filter=/usr/lib/cgit/filters/syntax-highlighting.py

scan-path=/home/git/
```

To get syntax highlighting, install `python-pygments` and uncomment the source-filter option.

If you'd like to password protect access to `www.example.com/git/`, create a `.htpasswd` file:

```
sudo htpasswd /etc/nginx/.htpasswd <username>
```

This is my `nginx` conf file to serve `cgit` from `www.example.com/git/`.

```
server {
	listen 80;
	listen [::]:80;

	server_name www.example.com;
    
	location /.well-known/acme-challenge/ {
		root /var/www/www.example.com;
	}
	location / {
		return 301 https://www.example.com$request_uri;
	}
}

server {
	listen 443 ssl;
	listen [::]:443 ssl;

	server_name www.example.com;
	
	ssl_certificate /etc/letsencrypt/live/www.example.com/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/www.example.com/privkey.pem;

    location /cgit-static/ {
        alias /usr/share/cgit/;
    }
    
    location /cgit/ {
        auth_basic "Restricted";
        auth_basic_user_file /etc/nginx/.htpasswd;

        include fastcgi_params;
        fastcgi_split_path_info ^(/cgit)(.*)$;
        fastcgi_param   PATH_INFO        $fastcgi_path_info;
        fastcgi_param   SCRIPT_FILENAME  /usr/lib/cgit/cgit.cgi;
        fastcgi_param   QUERY_STRING     $args;
        fastcgi_param   HTTP_HOST        $server_name;
        fastcgi_pass    unix:/var/run/fcgiwrap.socket;
    }

	location / {
		root /var/www/www.example.com;
	}
}
```

You might also want to restrict repo access to only whitelisted IPs.
