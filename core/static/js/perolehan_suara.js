// todo.js
const data = document.currentScript.dataset
const csrftoken = data.csrf

const getPerolehan = () => ({
  url: '/caleg/perolehan/api/',
  perolehan: [],
  tps: '',
  required: false,

  init() {
    this.getData()
  },

  getData() {
    // Pega os dados no backend com fetch.
    fetch(this.url)
      .then(response => response.json())
      .then(data => {
        this.perolehan = data
      })
  },

})