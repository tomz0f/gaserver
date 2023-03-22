import { is_logged, page_index } from './stores'

function load_page_index() {
    let page;
    page_index.subscribe((val) => {
        page = val;
    })
    return page
}

function isLogged() {
    let logged;
    is_logged.subscribe((val) => {
        logged = val;
    })
    return logged
}


export { isLogged, load_page_index }
