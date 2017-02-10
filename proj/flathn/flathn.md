# Flat HN

Flat HN is a bookmarklet that hides threaded conversations on Hacker News.

![github](https://github.com/s-gv/flat-hackernews)

## How to use

Drag this link, [Flat/Threaded HN](javascript:%7Bif(%22news.ycombinator.com%22%3D%3Dlocation.hostname)%7Bvar%20spacerImages%3Ddocument.getElementsByTagName(%22img%22)%2Ccomments%3DArray.prototype.slice.call(spacerImages).filter(function(e)%7Breturn%22https%3A%2F%2Fnews.ycombinator.com%2Fs.gif%22%3D%3De.src%26%26e.width%2540%3D%3D0%26%26(1%3D%3De.height%7C%7C2%3D%3De.height)%7D)%2CsearchChildrenByClassName%3Dfunction(e%2Ct)%7Bif(e.className%3D%3Dt)return%20e%3Bfor(var%20n%3D0%3Bn%3Ce.children.length%3Bn%2B%2B)%7Bvar%20m%3DsearchChildrenByClassName(e.children%5Bn%5D%2Ct)%3Bif(null!%3Dm)return%20m%7Dreturn%20null%7D%3Bif(comments%3Dcomments.map(function(e)%7Bvar%20t%3De.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement%2Cn%3DsearchChildrenByClassName(t%2C%22reply%22)%2Cm%3Dnull%3Breturn%20null!%3Dn%26%26null!%3Dn.lastChild%26%26(m%3Dn.lastChild.children%5B0%5D)%2C%7Bdepth%3Ae.width%2F40%2Crowele%3At%2Creplyparent%3Am%2Cmorelessele%3Anull%7D%7D)%2C%22undefined%22%3D%3Dtypeof%20__flathn__)%7B__flathn__%3D!0%3Bfor(var%20i%3D0%3Bi%3Ccomments.length%3Bi%2B%2B)if(comments%5Bi%5D.depth%3E1%26%26(comments%5Bi%5D.rowele.style.display%3D%22none%22)%2Ccomments%5Bi%5D.depth%3E%3D1)%7Bvar%20uTag%3Ddocument.createElement(%22u%22)%3BuTag.setAttribute(%22class%22%2C%22showmore%22)%3Bvar%20aTag%3Ddocument.createElement(%22a%22)%3BaTag.setAttribute(%22href%22%2C%22%23%22%2BMath.round(1e9*Math.random()))%2CaTag.innerHTML%3D%22more%22%2CaTag.addEventListener(%22click%22%2Cfunction(e%2Ct)%7Breturn%20function(n)%7Bif(%22more%22%3D%3Dt.firstChild.innerHTML)%7Bfor(var%20m%3De%2B1%3Bm%3Ccomments.length%26%26!(comments%5Bm%5D.depth%3Ccomments%5Be%5D.depth%2B1)%3Bm%2B%2B)comments%5Bm%5D.depth%3D%3Dcomments%5Be%5D.depth%2B1%26%26(comments%5Bm%5D.rowele.style.display%3D%22%22)%3Bt.firstChild.innerHTML%3D%22less%22%7Delse%7Bfor(var%20m%3De%2B1%3Bm%3Ccomments.length%26%26!(comments%5Bm%5D.depth%3Ccomments%5Be%5D.depth%2B1)%3Bm%2B%2B)comments%5Bm%5D.depth%3E%3Dcomments%5Be%5D.depth%2B1%26%26(comments%5Bm%5D.rowele.style.display%3D%22none%22%2Cnull!%3Dcomments%5Bm%5D.morelessele%26%26(comments%5Bm%5D.morelessele.innerHTML%3D%22more%22))%3Bt.firstChild.innerHTML%3D%22more%22%7Dn.preventDefault()%7D%7D(i%2CuTag)%2C!0)%2CuTag.appendChild(aTag)%2Ci%3Ccomments.length-1%26%26comments%5Bi%2B1%5D.depth%3Ecomments%5Bi%5D.depth%26%26null!%3Dcomments%5Bi%5D.replyparent%26%26(comments%5Bi%5D.replyparent.appendChild(uTag)%2Ccomments%5Bi%5D.morelessele%3Dcomments%5Bi%5D.replyparent.lastChild.lastChild)%7D%7Delse%7Bdelete%20__flathn__%3Bfor(var%20showmores%3Ddocument.getElementsByClassName(%22showmore%22)%3Bshowmores.length%3E0%3B)showmores%5B0%5D.parentElement.removeChild(showmores%5B0%5D)%3Bfor(var%20i%3D0%3Bi%3Ccomments.length%3Bi%2B%2B)comments%5Bi%5D.rowele.style.display%3D%22%22%7D%7Delse%20alert(%22This%20works%20with%20only%20Hacker%20News.%20Open%20a%20discussion%20at%20news.ycombinator.com%20and%20try%20again.%22)%3B%7Dvoid(0)%3B), to your bookmarks. Open a discussion on [HN](https://news.ycombinator.com/) and click on the newly created "Flat/Threaded HN" bookmark to hide nested comments. Clicking on the bookmarklet again will revert the page back to the threaded view.

![Demonstrating Flat HN](/proj/flathn/3.jpg)

## Why Flat HN?

Threaded conversations in [Hacker News](https://news.ycombinator.com/) (HN) can
be a pain at times. It's easy to lose context as you scroll down a long discussion;
see the screenshot below. Jeff Atwood has [written](http://blog.codinghorror.com/web-discussions-flat-by-design/)
at length about the issues with threaded discussions and suggests limiting the
level of replies allowed.

![Threaded Conversations in HN](/proj/flathn/1.jpg)

## How does it work?

HN's html suggests hiding deeply threaded comments should be simple. A spacer
GIF appears to be used to indent comments, and those spacers used for indentation
seem to have width in multiples of 40 in proportion to the depth of the comment.
The idea is to have some javascript as a bookmark, and this script gets executed
in the context of the page that is open when you click on the bookmarklet.

![How Flat HN works](/proj/flathn/2.jpg)