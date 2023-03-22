const { writable } = require('svelte/store');

const is_logged = writable(false);
const page_index = writable(0);

module.exports = { is_logged, page_index };
