document.querySelector("#headerChangeTheme").onclick = () => {
    if (document.body.classList.contains("dark")) {
        document.body.classList.remove("dark");
    } else {
        document.body.classList.add("dark");
    }
}

// Temp
let url = new URL(location.href);
let sp = new URLSearchParams(url.search);
let post = 73735;
let cat = post.toString().substr(0, 2);

if(sp.has("post")){
    post = sp.get("post");
}

fetch(`./d/${cat}/${post}.json`).then(r => r.json()).then(r => {
    document.querySelector("#backupUrl").innerText = r.baseUrl;
    document.querySelector("#backupTitle").innerText = r.title;
    document.querySelector("#backupPostsCount").innerText = r.content.length;

    let posts = "";
    r.content.forEach(p => {
        let author = p.author;
        let body = p.body;

        posts += `
            <div class="PostStream-item" data-type="comment">
                <article class="CommentPost Post">
                    <div>
                        <header class="Post-header">
                            <ul>
                                <li class="item-user">
                                    <div class="PostUser History">
                                        <h3>
                                            <img class="Avatar PostUser-avatar" src="./img/favicon.png">
                                            <span class="username">${author}</span>
                                        </h3>
                                    </div>
                                </li>
                            </ul>
                        </header>
                        <div class="Post-body">${body}<div>
                    </div>
                </article>
            </div>
        `;
    });

    document.querySelector("#backupPosts").insertAdjacentHTML("afterbegin", posts);
});