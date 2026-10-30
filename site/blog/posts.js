// 博客文章列表。文章正文可以放在 /blog/<slug>.html，然后把 url 指向它。
// 新增文章：在数组开头加一项，例如 { title: '标题', date: 'YYYY-MM-DD', url: '/blog/slug.html' }
const POSTS = [];
function renderPosts(el, limit) { const list = limit ? POSTS.slice(0, limit) : POSTS; if (!list.length) { el.innerHTML = '<li class="empty">还没有文章。</li>'; return; } el.innerHTML = list.map(p => `<li><time datetime="${p.date}">${p.date}</time><a href="${p.url}">${p.title}<span aria-hidden="true">↗</span></a></li>`).join(''); }
