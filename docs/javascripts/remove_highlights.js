document.addEventListener("DOMContentLoaded", function () {
	const highlights = document.querySelectorAll("mark[data-md-highlight]");
	highlights.forEach((el) => {
		const text = el.textContent;
		const span = document.createTextNode(text);
		el.parentNode.replaceChild(span, el);
	});
});
