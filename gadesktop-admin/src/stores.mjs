import { writable } from 'svelte/store'

const is_logged = writable(false);
const page_index = writable(0);
const user_data = writable({})

export {is_logged, page_index, user_data }