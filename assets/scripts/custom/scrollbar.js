// perfect scrollbar
const initPerfectScrollbar = () => {
	const container = document.querySelectorAll(".perfect-scrollbar");
	for (let i = 0; i < container.length; i++) {
		new PerfectScrollbar(container[i], {
			wheelPropagation: true,
			// suppressScrollX: true,
		});
	}
};
initPerfectScrollbar();
