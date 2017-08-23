# Flat HN
*November 23, 2014*

[Flat HN](https://github.com/s-gv/flat-hackernews) is a bookmarklet that hides threaded conversations on Hacker News.

## How to use

Drag this link, [Flat/Threaded HN](javascript:%7Bif%28%22news.ycombinator.com%22%3D%3Dlocation.hostname%29%7Bvar%20spacerImages%3Ddocument.getElementsByTagName%28%22img%22%29%2Ccomments%3DArray.prototype.slice.call%28spacerImages%29.filter%28function%28e%29%7Breturn%22https%3A%2F%2Fnews.ycombinator.com%2Fs.gif%22%3D%3De.src%26%26e.width%2540%3D%3D0%26%26%281%3D%3De.height%7C%7C2%3D%3De.height%29%7D%29%2CsearchChildrenByClassName%3Dfunction%28e%2Ct%29%7Bif%28e.className%3D%3Dt%29return%20e%3Bfor%28var%20n%3D0%3Bn%3Ce.children.length%3Bn%2B%2B%29%7Bvar%20m%3DsearchChildrenByClassName%28e.children%5Bn%5D%2Ct%29%3Bif%28null!%3Dm%29return%20m%7Dreturn%20null%7D%3Bif%28comments%3Dcomments.map%28function%28e%29%7Bvar%20t%3De.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement%2Cn%3DsearchChildrenByClassName%28t%2C%22reply%22%29%2Cm%3Dnull%3Breturn%20null!%3Dn%26%26null!%3Dn.lastChild%26%26%28m%3Dn.lastChild.children%5B0%5D%29%2C%7Bdepth%3Ae.width%2F40%2Crowele%3At%2Creplyparent%3Am%2Cmorelessele%3Anull%7D%7D%29%2C%22undefined%22%3D%3Dtypeof%20__flathn__%29%7B__flathn__%3D!0%3Bfor%28var%20i%3D0%3Bi%3Ccomments.length%3Bi%2B%2B%29if%28comments%5Bi%5D.depth%3E1%26%26%28comments%5Bi%5D.rowele.style.display%3D%22none%22%29%2Ccomments%5Bi%5D.depth%3E%3D1%29%7Bvar%20uTag%3Ddocument.createElement%28%22u%22%29%3BuTag.setAttribute%28%22class%22%2C%22showmore%22%29%3Bvar%20aTag%3Ddocument.createElement%28%22a%22%29%3BaTag.setAttribute%28%22href%22%2C%22%23%22%2BMath.round%281e9*Math.random%28%29%29%29%2CaTag.innerHTML%3D%22more%22%2CaTag.addEventListener%28%22click%22%2Cfunction%28e%2Ct%29%7Breturn%20function%28n%29%7Bif%28%22more%22%3D%3Dt.firstChild.innerHTML%29%7Bfor%28var%20m%3De%2B1%3Bm%3Ccomments.length%26%26!%28comments%5Bm%5D.depth%3Ccomments%5Be%5D.depth%2B1%29%3Bm%2B%2B%29comments%5Bm%5D.depth%3D%3Dcomments%5Be%5D.depth%2B1%26%26%28comments%5Bm%5D.rowele.style.display%3D%22%22%29%3Bt.firstChild.innerHTML%3D%22less%22%7Delse%7Bfor%28var%20m%3De%2B1%3Bm%3Ccomments.length%26%26!%28comments%5Bm%5D.depth%3Ccomments%5Be%5D.depth%2B1%29%3Bm%2B%2B%29comments%5Bm%5D.depth%3E%3Dcomments%5Be%5D.depth%2B1%26%26%28comments%5Bm%5D.rowele.style.display%3D%22none%22%2Cnull!%3Dcomments%5Bm%5D.morelessele%26%26%28comments%5Bm%5D.morelessele.innerHTML%3D%22more%22%29%29%3Bt.firstChild.innerHTML%3D%22more%22%7Dn.preventDefault%28%29%7D%7D%28i%2CuTag%29%2C!0%29%2CuTag.appendChild%28aTag%29%2Ci%3Ccomments.length-1%26%26comments%5Bi%2B1%5D.depth%3Ecomments%5Bi%5D.depth%26%26null!%3Dcomments%5Bi%5D.replyparent%26%26%28comments%5Bi%5D.replyparent.appendChild%28uTag%29%2Ccomments%5Bi%5D.morelessele%3Dcomments%5Bi%5D.replyparent.lastChild.lastChild%29%7D%7Delse%7Bdelete%20__flathn__%3Bfor%28var%20showmores%3Ddocument.getElementsByClassName%28%22showmore%22%29%3Bshowmores.length%3E0%3B%29showmores%5B0%5D.parentElement.removeChild%28showmores%5B0%5D%29%3Bfor%28var%20i%3D0%3Bi%3Ccomments.length%3Bi%2B%2B%29comments%5Bi%5D.rowele.style.display%3D%22%22%7D%7Delse%20alert%28%22This%20works%20with%20only%20Hacker%20News.%20Open%20a%20discussion%20at%20news.ycombinator.com%20and%20try%20again.%22%29%3B%7Dvoid%280%29%3B), to your bookmarks. Open a discussion on [HN](https://news.ycombinator.com/) and click on the newly created "Flat/Threaded HN" bookmark to hide nested comments. Clicking on the bookmarklet again will revert the page back to the threaded view.

![Demonstrating Flat HN](3.jpg)

## Why Flat HN?

Threaded conversations in [Hacker News](https://news.ycombinator.com/) (HN) can
be a pain at times. It's easy to lose context as you scroll down a long discussion;
see the screenshot below. Jeff Atwood has [written](http://blog.codinghorror.com/web-discussions-flat-by-design/)
at length about the issues with threaded discussions and suggests limiting the
level of replies allowed.

![Threaded Conversations in HN](1.jpg)

## How does it work?

HN's html suggests hiding deeply threaded comments should be simple. A spacer
GIF appears to be used to indent comments, and those spacers used for indentation
seem to have width in multiples of 40 in proportion to the depth of the comment.
The idea is to have some javascript as a bookmark, and this script gets executed
in the context of the page that is open when you click on the bookmarklet.

![How Flat HN works](2.jpg)
